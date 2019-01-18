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


class KubernetesError(Exception):
    """Error raised in case of problems during interacting with Kubernetes"""
    pass


class KubectlConnectionError(Exception):
    """Error raised in case of problems with closing local proxy"""


class InvalidRegularExpressionError(RuntimeError):
    """Error raised when user provided regular expression is invalid"""
    pass


class ExceptionWithMessage(Exception):
    """Exception with placeholder for a message"""
    def __init__(self, message: str = None):
        self.message = message


class K8sProxyOpenError(ExceptionWithMessage):
    """Error raised in case of any problems during establishing k8s proxy error"""
    pass


class K8sProxyCloseError(ExceptionWithMessage):
    """Error raised in case of any problems during closing k8s proxy error"""
    pass


class LocalPortOccupiedError(ExceptionWithMessage):
    """Error raised in case when app is not able to use a local port"""
    pass


class SubmitExperimentError(ExceptionWithMessage):
    """Error raised in case of any problems during experiment's submitting"""
    pass


class LaunchError(ExceptionWithMessage):
    """Error raised in case of any problems with launching other apps"""
    pass


class ProxyClosingError(ExceptionWithMessage):
    """Error raised in case of problems with closing local proxy"""


class ScriptConversionError(Exception):
    """Error raised in case of problems during conversion of python scripts into Jupyter notebooks"""
    pass


class InvalidDependencyError(Exception):
    """
    Error raised when nctl fails to obtain some dependency version, or when this version does not meet the
    requirements.
    """
    pass


class InvalidOsError(Exception):
    """Error raised when nctl fails to read user's OS version, or this version does not meet the requirements."""
    pass
