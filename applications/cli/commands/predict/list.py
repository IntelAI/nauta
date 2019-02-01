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

from commands.experiment.common import RUN_INFERENCE_NAME, RUN_PARAMETERS, RUN_START_DATE, RUN_END_DATE, \
    RUN_SUBMISSION_DATE, RUN_SUBMITTER, RUN_STATUS, RUN_TEMPLATE_NAME, RunKinds
from commands.common import list_runs_in_cli, list_unitialized_experiments_in_cli
from util.cli_state import common_options, pass_state, State
from platform_resources.run_model import RunStatus
from util.aliascmd import AliasCmd
from cli_text_consts import PredictListCmdTexts as Texts


LISTED_RUNS_KINDS = [RunKinds.INFERENCE]


@click.command(name='list', help=Texts.HELP, short_help=Texts.HELP, cls=AliasCmd, alias='ls',
               options_metavar='[options]')
@click.option('-a', '--all-users', is_flag=True, help=Texts.HELP_A)
@click.option('-n', '--name', type=str, help=Texts.HELP_N)
@click.option('-s', '--status', type=click.Choice([status.name for status in RunStatus]), help=Texts.HELP_S)
@click.option('-u', '--uninitialized', is_flag=True, help=Texts.HELP_U)
@click.option('-c', '--count', type=click.IntRange(min=1), help=Texts.HELP_C)
@click.option('-b', '--brief', is_flag=True, help=Texts.HELP_B)
@common_options()
@pass_state
def list_inference_instances(state: State, all_users: bool, name: str, status: RunStatus, uninitialized: bool,
                             count: int, brief: bool):
    """ List inference instances. """
    if brief:
        table_headers = [RUN_INFERENCE_NAME, RUN_SUBMISSION_DATE, RUN_SUBMITTER, RUN_STATUS]
    else:
        table_headers = [RUN_INFERENCE_NAME, RUN_PARAMETERS, RUN_SUBMISSION_DATE, RUN_START_DATE, RUN_END_DATE,
                         RUN_SUBMITTER, RUN_STATUS, RUN_TEMPLATE_NAME]
    if uninitialized:
        list_unitialized_experiments_in_cli(verbosity_lvl=state.verbosity, all_users=all_users, name=name,
                                            headers=table_headers,
                                            listed_runs_kinds=LISTED_RUNS_KINDS, count=count, brief=brief)
    else:
        list_runs_in_cli(state.verbosity, all_users, name, status, LISTED_RUNS_KINDS, table_headers,
                         with_metrics=False, count=count, brief=brief)
