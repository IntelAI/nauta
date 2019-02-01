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

import click

from commands.experiment.common import EXPERIMENTS_LIST_HEADERS, RunKinds, RUN_NAME, RUN_STATUS, RUN_SUBMISSION_DATE,\
    RUN_SUBMITTER
from commands.common import list_runs_in_cli, list_unitialized_experiments_in_cli
from util.cli_state import common_options, pass_state, State
from platform_resources.run_model import RunStatus
from util.aliascmd import AliasCmd
from util.logger import initialize_logger
from cli_text_consts import ExperimentListCmdTexts as Texts


logger = initialize_logger(__name__)

LISTED_RUNS_KINDS = [RunKinds.TRAINING, RunKinds.JUPYTER]


@click.command(name='list', short_help=Texts.SHORT_HELP, cls=AliasCmd, alias='ls', options_metavar='[options]')
@click.option('-a', '--all-users', is_flag=True, help=Texts.HELP_A)
@click.option('-n', '--name', type=str, help=Texts.HELP_N)
@click.option('-s', '--status', type=click.Choice([status.name for status in RunStatus]), help=Texts.HELP_S)
@click.option('-u', '--uninitialized', is_flag=True, help=Texts.HELP_U)
@click.option('-c', '--count', type=click.IntRange(min=1), help=Texts.HELP_C)
@click.option('-b', '--brief', is_flag=True, help=Texts.HELP_B)
@common_options()
@pass_state
def list_experiments(state: State, all_users: bool, name: str, status: RunStatus, uninitialized: bool, count: int,
                     brief: bool):
    """ List experiments. """
    if brief:
        list_headers = [RUN_NAME, RUN_SUBMISSION_DATE, RUN_SUBMITTER, RUN_STATUS]
    else:
        list_headers = EXPERIMENTS_LIST_HEADERS
    if uninitialized:
        list_unitialized_experiments_in_cli(verbosity_lvl=state.verbosity, all_users=all_users, name=name,
                                            headers=list_headers, count=count, brief=brief)
    else:
        list_runs_in_cli(state.verbosity, all_users, name, status, LISTED_RUNS_KINDS, list_headers, with_metrics=True,
                         count=count, brief=brief)
