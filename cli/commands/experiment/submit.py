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

import sys
from typing import Tuple, List
import os

import click
from tabulate import tabulate

from commands.experiment.common import RUN_NAME, RUN_PARAMETERS, RUN_STATUS, RUN_MESSAGE
from cli_state import common_options, pass_state, State
from util.logger import initialize_logger
from commands.experiment.common import submit_experiment
from util.aliascmd import AliasCmd
from util.exceptions import SubmitExperimentError, K8sProxyCloseError
from commands.experiment.common import validate_experiment_name

log = initialize_logger('commands.submit')

HELP = "Command used to submitting training scripts for a single-node tensorflow training."
HELP_N = "Name for this experiment."
HELP_SFL = "Name of a folder with additional files used by a script, e.g., other .py files, data etc. " \
           "If not given - its content won't be copied into an image."
HELP_T = "Name of a template used to create a deployment. By default, this is a single-node tensorflow training." \
         " Template is chosen. List of available templates might be obtained by" \
         " Issuing dlsctl experiment template_list command."
HELP_PR = "Values (set or range) of a single parameter. "
HELP_PS = "Set of values of one or several parameters."


@click.command(short_help=HELP, cls=AliasCmd, alias='s')
@click.argument("script_location", type=click.Path(), required=True)
@click.option("-sfl", "--script_folder_location", type=click.Path(), help=HELP_SFL)
@click.option("-t", "--template", help=HELP_T, default="tf-training-tfjob")
@click.option("-n", "--name", help=HELP_N, callback=validate_experiment_name)
@click.option("-pr", "--parameter_range", nargs=2, multiple=True, help=HELP_PR)
@click.option("-ps", "--parameter_set", multiple=True, help=HELP_PS)
@click.argument("script_parameters", nargs=-1)
@common_options()
@pass_state
def submit(state: State, script_location: str, script_folder_location: str, template: str, name: str,
           parameter_range: List[Tuple[str, str]], parameter_set: Tuple[str, ...],
           script_parameters: Tuple[str, ...]):
    log.debug("Submit - start")

    if not os.path.isfile(script_location):
        click.echo(f'Cannot find script: {script_location}. Make sure that provided path is correct.')
        sys.exit(1)

    if script_folder_location and not os.path.isdir(script_folder_location):
        click.echo(f'Cannot find script folder: {script_folder_location}. Make sure that provided path is correct.')
        sys.exit(1)

    click.echo("Submitting experiments.")

    try:
        runs_list = submit_experiment(state, script_location, script_folder_location, template, name,
                                      parameter_range, parameter_set, script_parameters)
    except K8sProxyCloseError as exe:
        click.echo(exe.message)
    except SubmitExperimentError as exe:
        click.echo(f"Problems during submitting experiment:{exe.message}")
        sys.exit(1)
    except Exception:
        click.echo("Other problems during submitting experiment.")
        sys.exit(1)

    # display information about status of a training
    click.echo(tabulate({RUN_NAME: [run.name for run in runs_list],
                         RUN_PARAMETERS: [run.formatted_parameters() for run in runs_list],
                         RUN_STATUS: [run.formatted_status() for run in runs_list],
                         RUN_MESSAGE: [run.error_message for run in runs_list]},
                        headers=[RUN_NAME, RUN_PARAMETERS, RUN_STATUS, RUN_MESSAGE], tablefmt="orgtbl"))
