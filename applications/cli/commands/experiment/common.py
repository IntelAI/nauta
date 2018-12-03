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

from collections import namedtuple
from distutils.dir_util import copy_tree
import itertools
import os
import re
import shutil
from sys import exit
import textwrap
import yaml

import click
from typing import Tuple, List
from pathlib import Path
from tabulate import tabulate
from marshmallow import ValidationError

import draft.cmd as cmd
from packs.tf_training import update_configuration, get_pod_count
import platform_resources.experiments as experiments_api
import platform_resources.experiment_model as experiments_model
from platform_resources.run_model import Run, RunStatus, RunKinds
import platform_resources.runs as runs_api
from util.config import EXPERIMENTS_DIR_NAME, FOLDER_DIR_NAME, Config
from util.k8s.kubectl import delete_k8s_object
from util.logger import initialize_logger
from util.spinner import spinner
from util.system import get_current_os, OS
from util import socat
from util.exceptions import K8sProxyOpenError, K8sProxyCloseError, LocalPortOccupiedError, \
    SubmitExperimentError
from util.app_names import DLS4EAppNames
from util.k8s.k8s_proxy_context_manager import K8sProxy
from util.k8s.k8s_info import get_app_service_node_port, get_kubectl_current_context_namespace
from platform_resources.custom_object_meta_model import validate_kubernetes_name
from util.jupyter_notebook_creator import convert_py_to_ipynb
from util.system import handle_error
from cli_text_consts import ExperimentCommonTexts as Texts

# definitions of headers content for different commands
# run name table header should be displayed as "Experiment" to hide term "Run" from the user
RUN_NAME = "Experiment"
RUN_INFERENCE_NAME = "Prediction instance"
RUN_STATUS = "State"
RUN_MESSAGE = "Message"
RUN_PARAMETERS = "Parameters"
RUN_METRICS = "Metrics"
RUN_SUBMISSION_DATE = "Submission date"
RUN_START_DATE = "Start date"
RUN_END_DATE = "End date"
RUN_SUBMITTER = "Owner"
RUN_TEMPLATE_NAME = "Template name"

JUPYTER_NOTEBOOK_TEMPLATES_NAMES = ["jupyter", "jupyter-py2"]

EXP_SUB_SEMAPHORE_FILENAME = ".underSubmission"

EXPERIMENTS_LIST_HEADERS = [RUN_NAME, RUN_PARAMETERS, RUN_METRICS, RUN_SUBMISSION_DATE, RUN_START_DATE, RUN_END_DATE,
                            RUN_SUBMITTER, RUN_STATUS, RUN_TEMPLATE_NAME]

CHART_YAML_FILENAME = "Chart.yaml"
TEMPL_FOLDER_NAME = "templates"

log = initialize_logger('commands.common')


class RunSubmission(Run):
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message


PrepareExperimentResult = namedtuple('PrepareExperimentResult', ['folder_name', 'script_name', 'pod_count'])


def get_run_environment_path(run_name: str) -> str:
    return os.path.join(Config().config_path, EXPERIMENTS_DIR_NAME, run_name)


def check_run_environment(run_environment_path: str):
    """
    If Run environment is not empty, ask user if it should be deleted in order to proceed with Run environment creation.
    """
    if os.path.isdir(run_environment_path) and os.listdir(run_environment_path):
        log.debug("---------------------------------------")
        log.debug(run_environment_path)
        log.debug(os.listdir(run_environment_path))
        log.debug("---------------------------------------")
        # check whether experiment is not being submitted at the moment
        if os.path.isfile(os.path.join(run_environment_path, EXP_SUB_SEMAPHORE_FILENAME)):
            handle_error(user_msg=Texts.THE_SAME_EXP_IS_SUBMITTED)
            exit(1)

        if click.confirm(Texts.CONFIRM_EXP_DIR_DELETION_MSG.format(run_environment_path=run_environment_path)):
            delete_environment(run_environment_path)
        else:
            handle_error(user_msg=Texts.UNABLE_TO_CONTINUE_EXP_SUBMISSION_ERROR_MSG
                         .format(run_environment_path=run_environment_path))
            exit()


def create_environment(experiment_name: str, file_location: str, folder_location: str) -> str:
    """
    Creates a complete environment for executing a training using draft.

    :param experiment_name: name of an experiment used to create a folder
                            with content of an experiment
    :param file_location: location of a training script
    :param folder_location: location of a folder with additional data
    :return: (experiment_folder)
    experiment_folder - folder with experiment's artifacts
    In case of any problems during creation of an enviornment it throws an
    exception with a description of a problem
    """
    log.debug("Create environment - start")
    message_prefix = Texts.CREATE_ENV_MSG_PREFIX

    # create a folder for experiment's purposes
    run_environment_path = get_run_environment_path(experiment_name)
    folder_path = os.path.join(run_environment_path, FOLDER_DIR_NAME)

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception:
        log.exception("Create environment - creating experiment folder error.")
        raise SubmitExperimentError(message_prefix.format(reason=Texts.EXP_DIR_CANT_BE_CREATED))

    # create a semaphore saying that experiment is under submission
    Path(os.path.join(run_environment_path, EXP_SUB_SEMAPHORE_FILENAME)).touch()

    # copy training script - it overwrites the file taken from a folder_location
    if file_location:
        try:
            shutil.copy2(file_location, folder_path)
            if get_current_os() == OS.WINDOWS:
                os.chmod(os.path.join(folder_path, os.path.basename(file_location)), 0o666)
        except Exception:
            log.exception("Create environment - copying training script error.")
            raise SubmitExperimentError(message_prefix.format(reason=Texts.TRAINING_SCRIPT_CANT_BE_CREATED))

    # copy folder content
    if folder_location:
        try:
            copy_tree(folder_location, folder_path)
        except Exception:
            log.exception("Create environment - copying training folder error.")
            raise SubmitExperimentError(message_prefix.format(reason=Texts.DIR_CANT_BE_COPIED_ERROR_TEXT))

    log.debug("Create environment - end")

    return run_environment_path


def remove_sempahore(experiment_name: str):
    run_environment_path = get_run_environment_path(experiment_name)
    semaphore_file = os.path.join(run_environment_path, EXP_SUB_SEMAPHORE_FILENAME)
    if os.path.isfile(semaphore_file):
        os.remove(semaphore_file)


def delete_environment(experiment_folder: str):
    """
    Deletes draft environment located in a folder given as a paramater
    :param experiment_folder: location of an environment
    """
    try:
        shutil.rmtree(experiment_folder)
    except Exception as exe:
        log.error("Delete environment - i/o error : {}".format(exe))


def convert_to_number(s: str) -> int or float:
    """
    Converts string to number of a proper type.

    :param s: - string to be converted
    :return: number in a proper format - float or int
    """
    try:
        return int(s)
    except ValueError:
        return float(s)


def submit_experiment(template: str, name: str, run_kind: RunKinds = RunKinds.TRAINING,
                      script_location: str = None, script_parameters: Tuple[str, ...] = None,
                      pack_params: List[Tuple[str, str]] = None, parameter_range: List[Tuple[str, str]] = None,
                      parameter_set: Tuple[str, ...] = None,
                      script_folder_location: str = None,
                      env_variables: List[str] = None,
                      requirements_file: str = None) -> (List[RunSubmission], str):
    script_parameters = script_parameters if script_parameters else ()
    parameter_set = parameter_set if parameter_set else ()
    parameter_range = parameter_range if parameter_range else []

    log.debug("Submit experiment - start")
    try:
        namespace = get_kubectl_current_context_namespace()
    except Exception:
        message = Texts.GET_NAMESPACE_ERROR_MSG
        log.exception(message)
        raise SubmitExperimentError(message)

    try:
        with spinner(text=Texts.PREPARING_RESOURCE_DEFINITIONS_MSG):
            experiment_name, labels = experiments_api.generate_exp_name_and_labels(script_name=script_location,
                                                                                   namespace=namespace, name=name,
                                                                                   run_kind=run_kind)
            runs_list = prepare_list_of_runs(experiment_name=experiment_name, parameter_range=parameter_range,
                                             parameter_set=parameter_set, template_name=template)
    except SubmitExperimentError as exe:
        log.exception(str(exe))
        raise exe
    except Exception:
        message = Texts.SUBMIT_PREPARATION_ERROR_MSG
        log.exception(message)
        raise SubmitExperimentError(message)

    try:
        config = Config()

        # start port forwarding
        # noinspection PyBroadException
        with K8sProxy(DLS4EAppNames.DOCKER_REGISTRY, port=config.local_registry_port) as proxy:
            # Save port that was actually used in configuration
            if proxy.tunnel_port != config.local_registry_port:
                config.local_registry_port = proxy.tunnel_port

            experiment_run_folders = []  # List of local directories used by experiment's runs
            try:
                # run socat if on Windows or Mac OS
                if get_current_os() in (OS.WINDOWS, OS.MACOS):
                    # noinspection PyBroadException
                    try:
                        with spinner(text=Texts.CLUSTER_CONNECTION_MSG):
                            socat.start(proxy.tunnel_port)
                    except Exception:
                        error_msg = Texts.LOCAL_DOCKER_TUNNEL_ERROR_MSG
                        log.exception(error_msg)
                        raise SubmitExperimentError(error_msg)

                cluster_registry_port = get_app_service_node_port(dls4e_app_name=DLS4EAppNames.DOCKER_REGISTRY)

                # prepare environments for all experiment's runs
                for experiment_run in runs_list:
                    if script_parameters and experiment_run.parameters:
                        current_script_parameters = script_parameters + experiment_run.parameters
                    elif script_parameters:
                        current_script_parameters = script_parameters
                    elif experiment_run.parameters:
                        current_script_parameters = experiment_run.parameters
                    else:
                        current_script_parameters = ""

                    run_folder, script_location, pod_count = \
                        prepare_experiment_environment(experiment_name=experiment_name,
                                                       run_name=experiment_run.name,
                                                       local_script_location=script_location,
                                                       script_folder_location=script_folder_location,  # noqa: E501
                                                       script_parameters=current_script_parameters,
                                                       pack_type=template, pack_params=pack_params,
                                                       local_registry_port=proxy.tunnel_port,
                                                       cluster_registry_port=cluster_registry_port,
                                                       env_variables=env_variables,
                                                       requirements_file=requirements_file)
                    # Set correct pod count
                    if not pod_count or pod_count < 1:
                        raise SubmitExperimentError('Unable to determine pod count: make sure that values.yaml '
                                                    'file in your pack has podCount field with positive integer value.')
                    experiment_run.pod_count = pod_count

                    experiment_run_folders.append(run_folder)
                    script_name = None
                    if script_location is not None:
                        script_name = os.path.basename(script_location)

                    # Prepend script_name parameter to run description only for display purposes.
                    experiment_run.parameters = script_parameters if not experiment_run.parameters \
                        else experiment_run.parameters + script_parameters
                    if experiment_run.parameters and script_name:
                        experiment_run.parameters = (script_name, ) + experiment_run.parameters
                    elif script_name:
                        experiment_run.parameters = (script_name, )
            except SubmitExperimentError as e:
                log.exception(Texts.ENV_CREATION_ERROR_MSG)
                e.message += f' {Texts.ENV_CREATION_ERROR_MSG}'
                raise
            except Exception:
                # any error in this step breaks execution of this command
                message = Texts.ENV_CREATION_ERROR_MSG
                log.exception(message)
                # just in case - remove folders that were created with a success
                for experiment_run_folder in experiment_run_folders:
                    delete_environment(experiment_run_folder)

            # if ps or pr option is used - first ask whether experiment(s) should be submitted
            if parameter_range or parameter_set:
                click.echo(Texts.CONFIRM_SUBMIT_MSG)
                click.echo(tabulate({RUN_NAME: [run.name for run in runs_list],
                                     RUN_PARAMETERS: ["\n".join(run.parameters) if run.parameters
                                                      else "" for run in runs_list]},
                                    headers=[RUN_NAME, RUN_PARAMETERS], tablefmt="orgtbl"))

                if not click.confirm(Texts.CONFIRM_SUBMIT_QUESTION_MSG, default=True):
                    for experiment_run_folder in experiment_run_folders:
                        delete_environment(experiment_run_folder)
                    exit()

            # create Experiment model
            # TODO template_name & template_namespace should be filled after Template implementation
            parameter_range_spec = [f'-pr {param_name} {param_value}' for param_name, param_value in parameter_range]
            parameter_set_spec = [f'-ps {ps_spec}' for ps_spec in parameter_set]
            experiment_parameters_spec = list(script_parameters) + parameter_range_spec + parameter_set_spec
            experiment = experiments_model.Experiment(name=experiment_name, template_name=template,
                                                      parameters_spec=experiment_parameters_spec,
                                                      template_namespace="template-namespace")

            experiments_api.add_experiment(experiment, namespace, labels=labels)

            # submit runs
            submitted_runs = []
            for run, run_folder in zip(runs_list, experiment_run_folders):
                try:
                    run.state = RunStatus.QUEUED
                    with spinner(text=Texts.CREATING_RESOURCES_MSG.format(run_name=run.name)):
                        # Add Run object with runKind label and pack params as annotations
                        runs_api.add_run(run=run, namespace=namespace, labels={'runKind': run_kind.value},
                                         annotations={pack_param_name: pack_param_value
                                                      for pack_param_name, pack_param_value in pack_params})
                        submitted_runs.append(run)
                        submit_draft_pack(run_folder, namespace)
                except Exception as exe:
                    delete_environment(run_folder)
                    try:
                        run.state = RunStatus.FAILED
                        run.message = str(exe)
                        runs_api.update_run(run=run, namespace=namespace)
                    except Exception as rexe:
                        # update of non-existing run may fail
                        log.debug(Texts.ERROR_DURING_PATCHING_RUN.format(str(rexe)))

            # Delete experiment if no Runs were submitted
            if not submitted_runs:
                click.echo(Texts.SUBMISSION_FAIL_ERROR_MSG)
                delete_k8s_object("experiment", experiment_name)

            # Change experiment status to submitted
            experiment.state = experiments_model.ExperimentStatus.SUBMITTED
            experiments_api.update_experiment(experiment=experiment, namespace=namespace)

    except LocalPortOccupiedError as exe:
        click.echo(exe.message)
        raise SubmitExperimentError(exe.message)
    except K8sProxyCloseError:
        log.exception('Error during closing of a proxy for a {}'.format(DLS4EAppNames.DOCKER_REGISTRY))
        raise K8sProxyCloseError(Texts.PROXY_CLOSE_ERROR_MSG)
    except K8sProxyOpenError:
        error_msg = Texts.PROXY_OPEN_ERROR_MSG
        log.exception(error_msg)
        raise SubmitExperimentError(error_msg)
    except SubmitExperimentError:
        raise
    except Exception as exe:
        error_msg = Texts.SUBMIT_OTHER_ERROR_MSG
        log.exception(error_msg)
        raise SubmitExperimentError(error_msg) from exe
    finally:
        with spinner(text=Texts.CLUSTER_CONNECTION_CLOSING_MSG):
            # noinspection PyBroadException
            try:
                socat.stop()
            except Exception:
                log.exception("Error during closing of a proxy for a local docker-host tunnel")
                raise K8sProxyCloseError(Texts.DOCKER_TUNNEL_CLOSE_ERROR_MSG)
        # remove semaphores from all exp folders
        remove_sempahore(experiment_name)

    log.debug("Submit - finish")
    return runs_list, script_location


def prepare_list_of_runs(parameter_range: List[Tuple[str, str]], experiment_name: str,
                         parameter_set: Tuple[str, ...], template_name: str) -> List[RunSubmission]:

    run_list = []

    if not parameter_range and not parameter_set:
        run_list = [RunSubmission(name=experiment_name, experiment_name=experiment_name,
                                  pod_selector={'matchLabels': {'app': template_name,
                                                                'draft': experiment_name,
                                                                'release': experiment_name}})]
    else:
        list_of_range_parameters = [("", )]
        list_of_set_parameters = [("", )]

        if parameter_range:
            list_of_range_parameters = analyze_pr_parameters_list(parameter_range)

        if parameter_set:
            list_of_set_parameters = analyze_ps_parameters_list(parameter_set)

        run_index = 1
        for set_param in list_of_set_parameters:
            for range_param in list_of_range_parameters:
                current_run_name = experiment_name + "-" + str(run_index)
                current_params = ()

                if len(set_param) >= 1 and set_param[0]:
                    current_params = set_param

                if len(range_param) >= 1 and range_param[0]:
                    current_params = current_params + range_param

                run_list.append(RunSubmission(name=current_run_name, experiment_name=experiment_name,
                                              parameters=current_params,
                                              pod_selector={'matchLabels': {'app': template_name,
                                                                            'draft': current_run_name,
                                                                            'release': current_run_name}}))
                run_index = run_index + 1
    return run_list


def prepare_experiment_environment(experiment_name: str, run_name: str, local_script_location: str,
                                   script_parameters: Tuple[str, ...],
                                   pack_type: str, local_registry_port: int, cluster_registry_port: int,
                                   script_folder_location: str = None,
                                   pack_params: List[Tuple[str, str]] = None,
                                   env_variables: List[str] = None,
                                   requirements_file: str = None) -> PrepareExperimentResult:
    """
    Prepares draft's environment for a certain run based on provided parameters
    :param experiment_name: name of an experiment
    :param run_name: name of an experiment run
    :param local_script_location: location of a script used for training purposes on local machine
    :param script_folder_location: location of an additional folder used in training
    :param script_parameters: parameters passed to a script
    :param pack_type: type of a pack used to start training job
    :param local_registry_port: port on which docker registry is accessible locally
    :param cluster_registry_port: port on which docker registry is accessible within dls4e cluster
    :param pack_params: additional pack params
    :param env_variables: environmental variables to be passed to training
    :param requirements_file: path to a file with experiment requirements
    :return: name of folder with an environment created for this run, a name of script used for training purposes
            and count of Pods
    In case of any problems - an exception with a description of a problem is thrown
    """
    log.debug(f'Prepare run {run_name} environment - start')
    run_folder = get_run_environment_path(run_name)
    try:
        # check environment directory
        check_run_environment(run_folder)
        with spinner(text=Texts.CREATING_ENVIRONMENT_MSG.format(run_name=run_name)):
            # create an environment
            create_environment(run_name, local_script_location, script_folder_location)
            # generate draft's data
            output, exit_code, log_output = cmd.create(working_directory=run_folder, pack_type=pack_type)

            # copy requirements file if it was provided, create empty requirements file otherwise
            dest_requirements_file = os.path.join(run_folder, 'requirements.txt')
            if requirements_file:
                shutil.copyfile(requirements_file, dest_requirements_file)
            else:
                Path(dest_requirements_file).touch()

        if exit_code:
            raise SubmitExperimentError(Texts.DRAFT_TEMPLATES_NOT_GENERATED_ERROR_MSG.format(reason=log_output))

        # Script location on experiment container
        remote_script_location = Path(local_script_location).name if local_script_location else ''

        if pack_type in JUPYTER_NOTEBOOK_TEMPLATES_NAMES and remote_script_location.endswith(".py"):
                # for interact (jupyter notebooks) try to convert .py file into .ipynb
                py_script_location = os.path.join(run_folder, FOLDER_DIR_NAME, remote_script_location)
                ipynb_file_name = convert_py_to_ipynb(py_script_location, os.path.join(run_folder, FOLDER_DIR_NAME))
                local_script_location = ipynb_file_name

        # reconfigure draft's templates
        update_configuration(run_folder=run_folder, script_location=remote_script_location,
                             script_parameters=script_parameters,
                             experiment_name=experiment_name, run_name=run_name,
                             local_registry_port=local_registry_port, cluster_registry_port=cluster_registry_port,
                             pack_type=pack_type, pack_params=pack_params,
                             script_folder_location=script_folder_location,
                             env_variables=env_variables)

        pod_count = get_pod_count(run_folder=run_folder, pack_type=pack_type)
    except Exception as exe:
        delete_environment(run_folder)
        raise SubmitExperimentError('Problems during creation of environments.') from exe
    log.debug(f'Prepare run {run_name} environment - finish')
    return PrepareExperimentResult(folder_name=run_folder, script_name=local_script_location, pod_count=pod_count)


def get_log_filename(log_output: str):
    logs_location = 'Inspect the logs with `draft logs '

    if logs_location in log_output:
        m = re.search(logs_location + '(.*)`', log_output)
        try:
            return m.group(1)
        except IndexError:
            pass

    return None


def submit_draft_pack(run_folder: str, namespace: str = None):
    """
    Submits one run using draft's environment located in a folder given as a parameter.
    :param run_folder: location of a folder with a description of an environment
    :param namespace: namespace where tiller used during deployment is located
    In case of any problems it throws an exception with a description of a problem
    """
    log.debug(f'Submit one run: {run_folder} - start')

    # run training
    output, exit_code, log_output = cmd.up(working_directory=run_folder, namespace=namespace)

    if exit_code:
        error_message = Texts.JOB_NOT_DEPLOYED_ERROR_MSG

        log_filename = get_log_filename(log_output)
        if log_filename:
            error_message = error_message + Texts.JOB_NOT_DEPLOYED_ERROR_MSG_LOGFILE.format(log_filename)
        log.error(log_output)
        delete_environment(run_folder)
        raise SubmitExperimentError(error_message)
    log.debug(f'Submit one run {run_folder} - finish')


def values_range(param_value: str) -> List[str]:
    """
    Returns a list containing values from start to stop with a step prepared based on
    a string representation of the "pr" parameter.
    :param param value: content of the "pr" parameter
    :return: list of values between start and stop with a given step
    """
    ret_range = []
    range_step = param_value.split(":")
    range_values = range_step[0]
    step = range_step[1]
    start, stop = range_values.split("...")

    current_value = convert_to_number(start)
    if "." in step:
        number_of_digits = len(step.split(".")[1])
    else:
        number_of_digits = 0
    step_n = convert_to_number(step)
    stop_n = convert_to_number(stop)
    while current_value <= stop_n:
        ret_range.append(str(current_value))
        current_value = round(current_value + step_n, number_of_digits)

    return ret_range


def prepare_list_of_values(param_name: str, param_values: str) -> List[str]:
    """
    Function converts content of -pr parameter to list of single values.

    :param param_name: name of a parameter which is analysed
    :param param_values: value of a parameter
    :return: list of all values of a parameter
    In case of any problems during analyzing of parameters - it throws
    an exception with a short message about a detected problem.
    More details concerning a cause of such issue can be found in logs.
    """
    error_message = Texts.INCORRECT_PARAM_FORMAT_ERROR_MSG.format(param_name=param_name)
    if not check_enclosing_brackets(param_values):
        log.error(error_message)
        raise ValueError(error_message)

    try:
        param_values = str.strip(param_values, "{}")
        temp_param_values = []
        # {start...stop:step} form
        if "..." in param_values:
            temp_param_values.extend(values_range(param_values))
        else:
            # {x, y, z} form
            temp_param_values.extend([str.strip(x) for x in param_values.split(",")])

        ret_values = []
        # each value contains parameter name
        for param in temp_param_values:
            ret_values.append("{}={}".format(param_name, param))

    except Exception:
        log.exception(error_message)
        raise ValueError(error_message)

    return ret_values


def analyze_pr_parameters_list(list_of_params: List[Tuple[str]]) -> List[Tuple[str, ...]]:
    """
    Analyzes a list of -pr/--parameter_range parameters. It returns a list
    containing a tuples with all combinations of values of parameters given by a user.

    :param list_of_params: list with tuples in form (parameter name, parameter value)
            list in this format is returned by a click
    :return: list containing tuples with all combinations of values of params given by
            a user
    In case of any problems during analyzing of parameters - it throws
    an exception with a short message about a detected problem.
    More details concerning a cause of such issue can be found in logs.
    """
    param_names = []
    param_values = []

    for param_name, param_value in list_of_params:
        if param_name in param_names:
            exe_message = Texts.PARAM_AMBIGUOUSLY_DEFINED.format(param_name=param_name)
            log.exception(exe_message)
            raise ValueError(exe_message)

        param_names.append(param_name)

        param_values.append(prepare_list_of_values(param_name, param_value))

    ret_list = list(itertools.product(*param_values))

    return ret_list


def analyze_ps_parameters_list(list_of_params: List[Tuple[str]]):
    """
    Analyzes a list of values of -ps options.
    :param list_of_params:
    :return: list containing tuples of all set of params given as a parameter
    """
    error_message = Texts.PARAM_SET_INCORRECT_FORMAT_ERROR_MSG

    ret_list = []

    for param_set in list_of_params:
        if not check_enclosing_brackets(param_set):
            log.error(error_message)
            raise ValueError(error_message)

        try:
            param_values = str.strip(param_set, "{}")
            param_values = [l.strip() for l in param_values.split(",")]
            param_tuple = tuple([l.replace(":", "=", 1) for l in param_values])
            ret_list.append(param_tuple)
        except Exception as e:
            log.exception(error_message)
            raise ValueError(error_message) from e

    return ret_list


def check_enclosing_brackets(params: str):
    """
    Performs an initial check of format of a parameters - whether it
    is enclosed in brackets and whether it is not empty
    :param params: parameter to be checked
    :return: True if check was a success, False otherwise
    """
    if not params or (str.strip(params)[0] != "{") or (str.strip(params)[-1] != "}"):
        return False
    return True


def validate_experiment_name(ctx, param, value):
    return check_experiment_name(value)


def validate_pack_params_names(ctx: click.Context, param, value: List[Tuple[str, str]]):
    for key, _ in value:
        if "=" in key:
            handle_error(user_msg=Texts.INVALID_PACK_PARAM_FORMAT_ERROR_MSG.format(key=key))
            exit(1)
    return value


def check_experiment_name(value: str) -> str:
    try:
        if value:
            if len(value) > 30:
                # tf-operator requires that {user}-{tfjob's name} is no longer than 63 chars, so we need to limit this
                raise ValidationError(Texts.EXPERIMENT_NAME_TOO_LONG_ERROR_MSG)
            validate_kubernetes_name(value)
            return value
    except ValidationError as ex:
        raise click.BadParameter(str(ex))


def validate_env_paramater(ctx, param, value):
    try:
        if value:
            for param in value:
                key, t_value = param.split("=")
                if not key or not t_value:
                    raise ValueError
        return value
    except Exception as exe:
        raise click.BadParameter(Texts.INCORRECT_ENV_PARAMETER)


def wrap_text(text: str, width: int, spaces: int = 2) -> str:
    return ("\n"+" " * spaces).join(textwrap.wrap(text, width))


def get_list_of_packs():
    path = os.path.join(Config().config_path, cmd.DRAFT_HOME_FOLDER, "packs")

    list_of_packs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if CHART_YAML_FILENAME in filenames and TEMPL_FOLDER_NAME in dirnames:
            pack_name = os.path.split(os.path.split(dirpath)[0])[1]
            list_of_packs.append(pack_name)

    return list_of_packs


def validate_template_name(ctx, param, value):
    if value not in get_list_of_packs():
        raise click.BadParameter(Texts.INCORRECT_TEMPLATE_NAME)
    return value


def validate_pack(name: str):
    # check corectenss of the Chart.yaml file
    chart_location = os.path.join(Config().config_path, cmd.DRAFT_HOME_FOLDER,
                                  "packs", name, "charts", CHART_YAML_FILENAME)

    if not os.path.isfile(chart_location):
        handle_error(user_msg=Texts.INCORRECT_PACK_DEFINITION.format(pack_name=name))
        exit(2)

    with open(chart_location, 'r', encoding='utf-8') as chart_file:
            chart_content = yaml.load(chart_file)
            if chart_content.get("name") != name:
                handle_error(user_msg=Texts.INCORRECT_PACK_DEFINITION.format(pack_name=name))
                exit(2)
