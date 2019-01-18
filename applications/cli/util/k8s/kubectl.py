#
# INTEL CONFIDENTIAL
# Copyright (c) 2018 Intel Corporation
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and treaty
# provisions. No part of the Material may be used, copied, reproduced, modified,
# published, uploaded, posted, transmitted, distributed, or disclosed in any way
# without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be express
# and approved by Intel in writing.
#

import subprocess
import time
import random
import socket
from enum import Enum

from typing import Optional, Tuple

import platform_resources.users as users_api
from util import system
from util.config import Config
from util.logger import initialize_logger
from util.exceptions import KubernetesError, KubectlConnectionError, LocalPortOccupiedError
from util.k8s.k8s_info import get_app_services, find_namespace, NamespaceStatus
from util.app_names import NAUTAAppNames
from util.system import check_port_availability
from cli_text_consts import UtilKubectlTexts as Texts
from util.k8s.k8s_proxy_context_manager import K8sProxy


logger = initialize_logger('util.kubectl')

MAX_NUMBER_OF_TRIES = 1000
START_PORT = 3000
END_PORT = 65535


class UserState(Enum):
    ACTIVE = "Active"
    TERMINATING = "Terminating"
    NOT_EXISTS = "Not_Exists"


def find_random_available_port() -> int:
    for port in random.sample(range(START_PORT, END_PORT), k=MAX_NUMBER_OF_TRIES):
        if check_port_availability(port):
            tunnel_port = port
            break
    else:
        error_msg = Texts.NO_AVAILABLE_PORT_ERROR_MSG
        logger.error(error_msg)
        raise LocalPortOccupiedError(error_msg)

    return tunnel_port


def start_port_forwarding(k8s_app_name: NAUTAAppNames, port: int = None, app_name: str = None,
                          number_of_retries: int = 0, namespace: str = None) -> (subprocess.Popen, Optional[int], int):
    """
    Creates a proxy responsible for forwarding requests to and from a
    kubernetes' local docker proxy. In case of any errors during creating the
    process - throws a RuntimeError exception with a short description of
    a cause of a problem.
    When proxy created by this function is no longer needed - it should
    be closed by calling kill() function on a process returned by this
    function.

    :param k8s_app_name: name of kubernetes application for tunnel creation
                         value taken from NAUTAAppNames enum
    :param port: if given - the system will try to use it as a local port. Random port will be used
     if that port is not available
    :return:
        instance of a process with proxy, tunneled port and container port
    """
    logger.debug("Start port forwarding")

    try:
        service_node_port = None
        service_container_port = None

        app_services = get_app_services(nauta_app_name=k8s_app_name, namespace=namespace, app_name=app_name)

        if app_services:
            service_node_port = app_services[0].spec.ports[0].node_port
            if service_node_port:
                logger.debug('Service node port pod has been found: {}'.
                             format(service_node_port))

            service_container_port = app_services[0].spec.ports[0].port
            if service_container_port:
                logger.debug('Service container port has been found: {}'.
                             format(service_container_port))
            service_name = app_services[0].metadata.name
            namespace = app_services[0].metadata.namespace

        if not service_node_port and not service_container_port:
            logger.error(f'Cannot find open ports for {k8s_app_name} app')
            raise KubernetesError(Texts.PROXY_CREATION_MISSING_PORT_ERROR_MSG)

        if port:
            if check_port_availability(port):
                tunnel_port = port
            else:
                tunnel_port = find_random_available_port()
        else:
            tunnel_port = find_random_available_port()

        if system.get_current_os() == system.OS.WINDOWS:
            port_forward_command = ['FOR', '/L', '%N', 'IN', '()', 'DO', 'kubectl', 'port-forward',
                                    f'--namespace={namespace}', f'service/{service_name}',
                                    f'{tunnel_port}:{service_container_port}']
        else:
            port_forward_command = ['while', 'true;', 'do', 'kubectl', 'port-forward', f'--namespace={namespace} ',
                                    f'service/{service_name}', f'{tunnel_port}:{service_container_port};',
                                    'done']

        logger.debug(port_forward_command)

        process = None
        if number_of_retries:
            for i in range(number_of_retries-1):
                try:
                    process = system.execute_subprocess_command(port_forward_command, shell=True, join=True)
                except Exception:
                    logger.exception("Error during setting up proxy - retrying.")
                else:
                    break
                time.sleep(5)

        if not process:
            process = system.execute_subprocess_command(port_forward_command, shell=True, join=True)

    except KubernetesError as exe:
        raise RuntimeError(exe)
    except LocalPortOccupiedError as exe:
        raise exe
    except Exception:
        raise RuntimeError(Texts.PROXY_CREATION_OTHER_ERROR_MSG)

    logger.info("Port forwarding - proxy set up")
    return process, tunnel_port, service_container_port


def check_users_presence(username: str) -> UserState:
    """
    Checks whether a user with a given name exists. It searches also for a namespace
    with a name equal to the given username

    :param username: username
    :return: returns a current state of user - as an item for UserState enum
    In case of problems during gathering user's data - it raises an exception.
    """
    namespace = find_namespace(username)

    if namespace != NamespaceStatus.NOT_EXISTS:
        logger.debug("Namespace {} already exists.".format(username))
        return UserState(namespace.value)

    try:
        user_data = users_api.get_user_data(username)

        if user_data and user_data.name == username:
            return UserState.ACTIVE
        else:
            return UserState.NOT_EXISTS

    except Exception as exe:
        error_message = Texts.USER_PRESENCE_CHECK_ERROR_MSG
        logger.error(error_message)
        raise KubernetesError(error_message) from exe


def delete_k8s_object(kind: str, name: str):
    delete_command = ['kubectl', 'delete', kind, name]
    logger.debug(delete_command)
    output, err_code, log_output = system.execute_system_command(delete_command)
    logger.debug(f"delete_k8s_object - output : {err_code} - {log_output}")
    if err_code:
        raise RuntimeError(Texts.K8S_OBJECT_DELETE_ERROR_MSG.format(output=log_output))


def check_connection_to_cluster():
    check_connection_cmd = ['kubectl', 'get', 'pods']
    logger.debug(check_connection_cmd)
    output, err_code, log_output = system.execute_system_command(check_connection_cmd)
    logger.debug(f"check_connection_to_cluster - output : {err_code} - {log_output}")
    if err_code:
        raise KubectlConnectionError(Texts.K8S_CLUSTER_NO_CONNECTION_ERROR_MSG.format(output=log_output))


def check_port_forwarding():
    config = Config()
    with K8sProxy(NAUTAAppNames.DOCKER_REGISTRY, port=config.local_registry_port) as proxy:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = "127.0.0.1", proxy.tunnel_port
        if sock.connect_ex(address) != 0:
            raise KubectlConnectionError(Texts.K8S_PORT_FORWARDING_ERROR_MSG)


def get_top_for_pod(name: str, namespace: str) -> Tuple[str, str]:
    """
    Returns cpu and memory usage for a pod with a given name located in a given namespace
    :param name: name of a pod
    :param namespace:  namespace where the pod resided. Optional - if not given, function searches the pod in
                        current namespace
    :return: tuple containing two values - cpu and memory usage expressed in k8s format
    """
    top_command = ["kubectl", "top", "pod", name]

    if namespace:
        top_command.extend(["-n", namespace])
    output, err_code, log_output = system.execute_system_command(top_command)
    if err_code:
        raise KubectlConnectionError(Texts.K8S_CLUSTER_NO_CONNECTION_ERROR_MSG.format(output=log_output))

    if output:
        lines = output.split("\n")

        if lines and len(lines) > 1:
            second_line = lines[1]
            if second_line:
                split_second_line = second_line.split()
                if split_second_line and len(split_second_line) > 2:
                    return (split_second_line[1], split_second_line[2])

    logger.error(Texts.TOP_COMMAND_ERROR_LOG.format(output=log_output))
    raise KubernetesError(Texts.TOP_COMMAND_ERROR)
