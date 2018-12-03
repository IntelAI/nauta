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

VERBOSE_RERUN_MSG = "Use -v or -vv option for more info."
SPINNER_COLOR = "green"


class VersionCmdTexts:
    HELP = "Displays the version of the installed dlsctl application."
    INITIAL_PLATFORM_VERSION = "Failed to get platform version."
    KUBECTL_INT_ERROR_MSG = "Falied to check platform version. This may occur for example due to invalid path to " \
                            "kubectl config, invalid k8s credentials or k8s cluster being unavailable. Check your " \
                            "KUBECONFIG environment variable and make sure that the k8s cluster is online."
    OTHER_ERROR_MSG = "Unexpected error occurred during platform version check."
    TABLE_APP_ROW_NAME = "dlsctl application"
    TABLE_PLATFORM_ROW_NAME = "dls4e platform"
    TABLE_HEADERS = ["Component", "Version"]


class MountCmdTexts:
    HELP = "Displays a command that can be used to mount client's folders on his/her local machine."
    MAIN_MSG = """Use the following command to mount those folders:
 - replace <MOUNTPOINT> with a proper location on your local machine)
 - replace <DLS4E_FOLDER> with one of the following:
        - input - User's private input folder (read/write)
          (can be accessed as /mnt/input/home from training script).
        - output - User's private output folder (read/write)
          (can be accessed as /mnt/output/home from training script).
        - input-shared - Shared input folder (read/write)
          (can be accessed as /mnt/input/root/public from training script).
        - output-shared - Shared output folder (read/write)
          (can be accessed as /mnt/output/root/public from training script).
        - input-output-ro - Full input and output directories, read only.
Additionally, each experiment has a special folder that can be accessed
as /mnt/output/experiment from training script. This folder is shared by Samba
as output/<EXPERIMENT_NAME>.
--------------------------------------------------------------------"""

    HELP_L = "Displays a list of dls4e folders mounted on a local machine. If run using admin credentials, displays " \
             "mounts of all users."
    USER_IS_ADMIN_ERROR_MSG = "DLS4E doesn't create shares for administrators. Please execute this command as a " \
                              "regular user."
    ADMIN_CHECK_ERROR_MSG = "Problems detected while verifying that current user is an administrator."
    GET_MOUNT_COMMAND_ERROR_MSG = "Error detected while gathering data needed for mounting Samba share."
    UNMOUNT_COMMAND_MSG = "Use following command to unmount previously mounted folder:"
    UNMOUNT_OPTIONS_MSG = "In case of problems with unmounting (disconnected disk etc.) try out -f (force) or -l " \
                          "(lazy) options. For more info about these options refer to man umount."
    UNMOUNT_OPTIONS_OSX_MSG = "In case of problems with unmounting (disconnected disk etc.) try out -f (force) " \
                              "option. For more info about these options refer to man umount."
    MOUNTS_LIST_COMMAND_ERROR_MSG = "Error detected while gathering list of mounted shares."


class CmdsCommonTexts:
    INVALID_REGEX_ERROR_MSG = "Regular expression provided for name filtering is invalid: {name}"
    OTHER_ERROR_MSG = "Failed to get experiments list."


class VerifyCmdTexts:
    HELP = "Command verifies whether all external components required by dlsctl are installed in proper versions. " \
           "If something is missing, the application displays detailed information about it."
    KUBECTL_NOT_INSTALLED_ERROR_MSG = "kubectl is not installed."
    GET_K8S_NAMESPACE_ERROR_MSG = "Failed to get current Kubernetes namespace."
    VERSION_CHECKING_MSG = "Checking version of {dependency_name}. Installed version: ({installed_version}). " \
                           "Supported version {supported_versions_sign} {expected_version}."
    DEPENDENCY_VERIFICATION_SUCCESS_MSG = "{dependency_name} verified successfully."
    INVALID_VERSION_WARNING_MSG = "Warning: the installed version of {dependency_name} ({installed_version}) is " \
                                  "not supported, supported version {supported_versions_sign} " \
                                  "{expected_version}"
    DEPENDENCY_NOT_INSTALLED_ERROR_MSG = "{dependency_name} is not installed. Check installation manual for more " \
                                         "information."
    DEPENDENCY_VERSION_CHECK_ERROR_MSG = "Failed to get {dependency_name} version."
    DEPENDENCY_VERIFICATION_OTHER_ERROR_MSG = "{dependency_name} - exception during verification."
    OS_SUPPORTED_MSG = "This OS is supported."
    CHECKING_CONNECTION_TO_CLUSTER_MSG = "Checking connection to the cluster..."
    CHECKING_OS_MSG = "Checking operating system..."
    VERIFYING_DEPENDENCY_MSG = "Verifying {dependency_name} ..."
    CHECKING_PORT_FORWARDING_FROM_CLUSTER_MSG = "Checking port forwarding from cluster..."


class UserCmdTexts:
    HELP = "Command for creating/deleting/listing users of the platform. Can only be run by a platform " \
           "administrator."


class UserListCmdTexts:
    HELP = "List users."
    HELP_C = "If given - command displays c last rows."
    TABLE_HEADERS = ["Name", "Creation date", "Date of last submitted job", "Number of running jobs",
                     "Number of queued jobs"]
    OTHER_ERROR_MSG = "Failed to get users list."


class UserCreateCmdTexts:
    SHORT_HELP = "Command used to create a new user on the platform. Can only be run by a platform administrator."
    HELP = """
    Command used to create a new user on the platform. Can only be run by a platform administrator. 

    USERNAME - is a name of user which should be created.
    """
    HELP_L = "If given - content of the generated user's config file is displayed on the screen only."
    HELP_F = "Name of file where user's configuration will be stored. If not given configuration is stored in the " \
             "config. file."
    ADD_USER_ERROR_MSG = "User {username} has not been created."
    REMOVE_USER_ERROR_MSG = "Additional error appeared when the system tried to remove artifacts of a non-created " \
                            "{username} user. Please contact an administrator to completely remove those artifacts."
    F_L_OPTIONS_EXCLUSION_ERROR_MSG = "Both -f/--filename and -l/--list_only options cannot be given. Please " \
                                      "choose one of them."
    NAME_VALIDATION_ERROR_MSG = "Error detected while validating user name: {username}."
    USER_NOT_ADMIN_ERROR_MSG = "Only administrators can create new users."
    USER_ALREADY_EXISTS_ERROR_MSG = "User {username} already exists."
    USER_BEING_REMOVED_ERROR_MSG = "User {username} is still being removed."
    USER_VERIFICATION_ERROR_MSG = "Problems detected while verifying user with user name: {username}."
    PASSWORD_GATHER_ERROR_MSG = "The app encountered problems while gathering user's password."
    USER_ADD_ERROR_MSG = "Error detected while adding of a user."
    USER_CREATION_SUCCESS_MSG = "User {username} has been added successfully."
    USER_NOT_READY_ERROR_MSG = "User {username} is still not ready."
    CONFIG_CREATION_ERROR_MSG = "Problems during creation of the kubeconfig with user's configuration."
    LIST_ONLY_HEADER = "Please use the following kubectl config to connect to this user.\n" \
                       "----------------------------------------------------------------"
    CONFIG_SAVE_SUCCESS_MSG = "Configuration has been saved to the {filename} file."
    CONFIG_SAVE_FAIL_MSG = "File with configuration wasn't saved."
    CONFIG_SAVE_FAIL_INSTRUCTIONS_MSG = "Content of the generated config file is as follows. Please copy it " \
                                        "to a file manually."
    CREATING_USER_PROGRESS_MSG = "Creating user {username}..."

class UserDeleteCmdTexts:
    SHORT_HELP = "Command used to delete a user from the platform. Can be only run by a platform administrator."
    HELP = """
    Command used to delete a user from the platform. Can be only run by a platform administrator.

    USERNAME - is a name of user which should be deleted.
    """
    HELP_PR = "If this option is added, the command removes all of client's artifacts."
    USER_NOT_ADMIN_ERROR_MSG = "Only administrators can delete users."
    USER_NOT_EXISTS_ERROR_MSG = "User {username} doesn't exists."
    USER_BEING_REMOVED_ERROR_MSG = "User is still being removed."
    USER_PRESENCE_VERIFICATION_ERROR_MSG = "Problems during verifying users presence."
    DELETE_CONFIRM_MSG = "User {username} is about to be deleted. Do you want to continue?"
    DELETE_ABORT_MSG = "Operation of deleting of a user was aborted."
    PURGE_ERROR_MSG = "Some artifacts belonging to a user weren't removed."
    DELETE_IN_PROGRESS_MSG = "User is still being deleted. Please check status of this user in a while."
    DELETE_SUCCESS_MSG = "User {username} has been deleted."
    PROXY_ERROR_LOG_MSG = "Error during closing of a proxy for elasticsearch."
    PROXY_ERROR_USER_MSG = "Elasticsearch proxy hasn't been closed properly. Check whether it still exists, if " \
                           "yes - close it manually."
    OTHER_ERROR_LOG_MSG = "Error during deleting a user of a user."
    OTHER_ERROR_USER_MSG = "User hasn't been deleted due to technical reasons."
    DELETION_CHECK_PRESENCE = "Checking presence of a user that is going to be deleted..."
    DELETION_START_DELETING = "Deleting of a user is starting now..."
    DELETION_START_PURGING = "Purging of a user is starting now..."
    DELETION_VERIFICATION_OF_DELETING = "Verifying, whether a user has been deleted properly..."
    DELETION_DELETING_NAMESPACE = "- deleting user's namespace"
    DELETION_DELETING_USERS_OBJECTS = "- deleting user's objects"
    DELETION_DELETING_USERS_EXPERIMENTS = "- deleting user experiments' logs"


class LaunchCmdTexts:
    HELP = "Command for launching web user-interface or tensorboard. It works as process in the system console " \
           "until user does not stop it. If process should be run as background process, please add '&' at the end " \
           "of line"
    HELP_P = "Port on which service will be exposed locally."
    HELP_N = "Run command without a web browser starting, only proxy tunnel is created"
    WEBUI_HELP = "Subcommand for launching webUI with credentials"
    APP_PROXY_EXISTS_ERROR_MSG = "K8s proxy hasn't been closed properly. Check whether it still exists, if yes - " \
                                 "close it manually."
    APP_PROXY_OTHER_ERROR_MSG = "Other exception during launching web application."
    SHORT_TB_HELP = "Subcommand for launching tensorboard with credentials."
    TB_HELP = """
    Subcommand for launching tensorboard with credentials.

    EXPERIMENT_NAME - is a name of experiment for which tensorboard instance should be launched.
    """
    TB_HELP_TSCP = "Local port on which tensorboard service client will be started."
    TB_INVALID_RUNS_MSG = "There is no data for the following experiments : {invalid_runs}\n" \
                          "Tensorboard will present information from the rest of given experiments."
    TB_CREATE_ERROR_MSG = "Failed to create tensorboard!"
    TB_WAITING_MSG = "Please wait for Tensorboard to run..."
    TB_WAITING_FOR_TB_MSG = "Tensorboard instance: {tb_id} still in {tb_status_value} status, waiting for " \
                            "RUNNING..."
    TB_TIMEOUT_ERROR_MSG = "Tensorboard failed to run - timeout."


class PredictCmdTexts:
    HELP = "Command for starting, stopping, and managing prediction jobs and instances. To get further help on " \
           "commands use COMMAND with -h or --help option."


class PredictListCmdTexts:
    HELP = "Show prediction instances"
    HELP_A = "Show all prediction instances, regardless of the owner."
    HELP_N = "A regular expression to narrow down list to prediction instances that match this expression."
    HELP_S = "List prediction instances with matching status."
    HELP_U = "List uninitialized prediction instances, i.e. prediction instances" \
             " without resources submitted for creation."
    HELP_C = "If given - command displays c last rows."
    HELP_B = "Print short version of result table. Only 'name', 'submission date', 'owner' and 'state' columns will" \
             " be print."


class PredictLaunchCmdTexts:
    HELP = "Starts a new prediction instance that can be used for performing prediction, classification and " \
           "regression tasks on trained model."
    HELP_N = "The name of this prediction instance."
    HELP_M = "Path to saved model that will be used for inference. Model must be located on one of the input or " \
             "output system shares (e.g. /mnt/input/saved_model)."
    HELP_R = "Path to file with experiment's pip requirements." \
             " Dependencies listed in this file will be automatically installed using pip."
    INSTANCE_START_ERROR_MSG = "Failed to create prediction instance."
    INSTANCE_INFO_MSG = "\nPrediction instance URL (append method verb manually, e.g. :predict):\n" \
                        "{inference_instance_url}\n\nAuthorize with following header:\n{authorization_header}"
    INSTANCE_URL_ERROR_MSG = "Failed to obtain prediction instance URL."
    TABLE_HEADERS = ["Prediction instance", "Model Location", "State"]
    HELP_LOCAL_MODEL_LOCATION = "Local path to saved model that will be used for inference. Model content will be " \
                                "copied into an image"
    MODEL_DIR_NOT_FOUND_ERROR_MSG = "Cannot find: {local_model_location}. local_model_location must be a path to " \
                                    "existing directory."
    MISSING_MODEL_LOCATION_ERROR_MSG = "Missing model location param - " \
                                       "'model location' or 'local model location' required"
    HELP_MODEL_NAME = "Name of a model passed as a servable name. By default it is the name of directory in model's " \
                      "location."
    HELP_P = " Additional pack param in format: 'key value' or 'key.subkey.subkey2 value'. For lists use: " \
             "'key \"['val1', 'val2']\"' For maps use: 'key \"{'a': 'b'}\"' "


class PredictStreamCmdTexts:
    HELP = "Perform stream prediction task on deployed prediction instance."
    HELP_N = "Name of prediction session."
    HELP_D = "Path to JSON data file that will be streamed to prediction instance. Data must be formatted such " \
             "that it is compatible with the SignatureDef specified within the model deployed in selected " \
             "prediction instance."
    HELP_M = "Method verb that will be used when performing inference. Predict verb is used by default."
    INSTANCE_NOT_EXISTS_ERROR_MSG = "Prediction instance {name} does not exist."
    INSTANCE_NOT_RUNNING_ERROR_MSG = "Prediction instance {name} is not in {running_code} state."
    INSTANCE_GET_FAIL_ERROR_MSG = "Failed to get prediction instance {name} URL."
    JSON_LOAD_ERROR_MSG = "Failed to load {data} data file. Make sure that provided file exists and is in a " \
                          "valid JSON format."
    INFERENCE_OTHER_ERROR_MSG = "Failed to perform inference. Reason: {exception}"
    INFERENCE_ERROR_RESPONSE_MSG = "\n Response: {response_text}"
    WAITING_FOR_RESPONSE_MSG = "Waiting for prediction instance response..."


class PredictCancelCmdTexts:
    SHORT_HELP = "Cancels prediction instance/s chosen based on criteria given as a parameter."
    HELP = """
    Cancels prediction instance/s chosen based on criteria given as a parameter.

    name - is a name of prediction instance which should be cancelled, name argument value can be empty when 'match' option is used.
    """
    HELP_P = "If given, then all information concerning all prediction instances, completed and currently " \
             "running, is removed from the system."
    HELP_M = "If given, command searches for prediction instances matching the value of this option."
    EXPERIMENT_NAME = "prediction instance"
    EXPERIMENT_NAME_PLURAL = "prediction instances"


class PredictBatchCmdTexts:
    HELP = "Uses specified dataset to perform inference. Results stored in output file"
    HELP_DATA = "location of a folder with data that will be used to perform the batch inference. Value should " \
                "points out the location from one of the system's shares."
    HELP_MODEL_LOCATION = "Path to saved model that will be used for inference. Model must be located on one of the " \
                          "input or output system shares (e.g. /mnt/input/saved_model)."
    HELP_LOCAL_MODEL_LOCATION = "Local path to saved model that will be used for inference. Model content will be " \
                                "copied into an image"
    HELP_MODEL_NAME = "Name of a model passed as a servable name. By default it is the name of directory in model's " \
                      "location."
    HELP_NAME = "name of a predict session"
    HELP_OUTPUT = "location of a folder where outputs from inferences will be stored. Value should points out the " \
                  "location from one of the system's shares."
    HELP_REQUIREMENTS = "Path to file with experiment's pip requirements." \
                        " Dependencies listed in this file will be automatically installed using pip."
    OTHER_INSTANCE_CREATION_ERROR_MSG = "Failed to create batch prediction instance."
    TABLE_NAME_HEADER = "Prediction instance"
    TABLE_MODEL_LOCATION_HEADER = "Model location"
    TABLE_STATUS_HEADER = "State"
    TABLE_HEADERS = ["Prediction instance", "Model location", "State"]
    MODEL_DIR_NOT_FOUND_ERROR_MSG = "Cannot find: {local_model_location}. local_model_location must be a path to " \
                                    "existing directory."
    MISSING_MODEL_LOCATION_ERROR_MSG = "Missing model location param - " \
                                       "'model location' or 'local model location' required"
    HELP_TF_RECORD = "If given - batch prediction accepts files in TFRecord formats. Otherwise files should be " \
                     "delivered in protobuf format."
    HELP_P = " Additional pack param in format: 'key value' or 'key.subkey.subkey2 value'. For lists use: " \
             "'key \"['val1', 'val2']\"' For maps use: 'key \"{'a': 'b'}\"' "


class ExperimentCmdTexts:
    HELP = "Command for starting, stopping, and managing training jobs."


class ExperimentListCmdTexts:
    SHORT_HELP = "Show logs for a given experiment."
    HELP_A = "Show all experiments, regardless of the owner."
    HELP_N = "A regular expression to narrow down list to experiments that match this expression."
    HELP_S = "List experiments with matching status."
    HELP_U = "List uninitialized experiments, i.e. experiments without resources submitted for creation."
    HELP_C = "If given - command displays c last rows."
    HELP_B = "Print short version of result table. Only 'name', 'submission date', 'owner' and 'state' columns will" \
             " be print."


class ExperimentTemplateListCmdTexts:
    SHORT_HELP = "Show logs for a given experiment."
    HELP = "Returns a list of available templates that can be used to submit training jobs."
    LACK_OF_PACKS_ERROR_MSG = "Lack of installed packs."


class ExperimentLogsCmdTexts:
    SHORT_HELP = "Show logs for a given experiment."
    HELP = """
    Show logs for a given experiment.

    experiment_name - is a name of experiment whose logs should be displayed, experiment_name argument value can be
    empty when 'match' option is used.
    """
    HELP_S = "Show all events with this specified minimal and greater severity."
    HELP_SD = "Retrieve all logs produced on and after this date (use ISO 8601 date format)."
    HELP_ED = "Retrieve all logs produced on and before this date (use ISO 8601 date format)."
    HELP_I = "Comma separated list of pod IDs. If provided, only logs from these pods will be returned."
    HELP_P = "Get logs only for pods with given status."
    HELP_M = "If given, command searches for logs from experiments matching the value of this option. " \
             "This option cannot be used along with the NAME argument."
    HELP_O = "If given - logs are stored in a file with a name derived from a name of an experiment."
    HELP_F = "Specify if logs should be streamed. Only logs from a single experiment can be streamed."
    HELP_PAGER = "Display logs in interactive pager."
    PROXY_CREATION_ERROR_MSG = "Error during creation of a proxy for elasticsearch."
    LOGS_GET_OTHER_ERROR_MSG = "Failed to get experiment logs."
    EXPERIMENT_NOT_EXISTS_ERROR_MSG = "Experiment with name {experiment_name} does not exist."
    LOCAL_PORT_OCCUPIED_ERROR_MSG = "Error during creation of a proxy for elasticsearch. {exe.message}"
    PROXY_CLOSE_LOG_ERROR_MSG = "Error during closing of a proxy for elasticsearch."
    PROXY_CLOSE_USER_ERROR_MSG = "Elasticsearch proxy hasn't been closed properly. Check whether it still exists, if " \
                                 "yes - close it manually."
    NAME_M_BOTH_GIVEN_ERROR_MSG = "Both experiment name and -m option cannot be given. Please choose one of them."
    NAME_M_NONE_GIVEN_ERROR_MSG = "Error: Experiment name or -m option must be given. Please pass one of them."
    LOGS_STORING_CONFIRMATION = "Logs from the {experiment_name} experiment will be stored in " \
                                "the {filename} file. Should the app proceed?"
    LOGS_STORING_CONFIRMATION_FILE_EXISTS = "Logs from the {experiment_name} experiment will be stored in the " \
                                            "{filename} file. The file with this name already exists. Should the app " \
                                            "proceed?"
    LOGS_STORING_ERROR = "Some problems occurred during storing a file with logs. {exception_message}"
    LOGS_STORING_FINAL_MESSAGE = "Logs have been written to the file mentioned above."
    LOGS_STORING_CANCEL_MESSAGE = "Logs have not been written to the file mentioned above - cancelled by user."
    MORE_EXP_LOGS_MESSAGE = "There is more than one log to be stored. Each log will be stored in a separate file."
    SAVING_LOGS_TO_FILE_PROGRESS_MSG = "Saving logs to a file..."


class ExperimentSubmitCmdTexts:
    SHORT_HELP = "Command used to submitting training scripts."
    HELP = """
    Command used to submitting training scripts.

    SCRIPT_LOCATION - is a location of the script used for training purposes - it is an obligatory argument.

    script_parameters - contains parameters passed directly to the script - all such parameters should be added
    at the end of command after '--' string.
    """
    HELP_N = "Name for this experiment."
    HELP_SFL = "Name of a folder with additional files used by a script, e.g., other .py files, data etc. If not " \
               "given - its content won't be copied into an image."
    HELP_T = "Name of a template used to create a deployment. By default, this is a single-node tensorflow training." \
             " Template is chosen. List of available templates might be obtained by" \
             " Issuing dlsctl experiment template_list command."
    HELP_P = " Additional pack param in format: 'key value' or 'key.subkey.subkey2 value'. For lists use: " \
             "'key \"['val1', 'val2']\"' For maps use: 'key \"{'a': 'b'}\"' "
    HELP_PR = "Values (set or range) of a single parameter."
    HELP_PS = "Set of values of one or several parameters."
    USER_IS_ADMIN_LOG_MSG = "Current user is dls4e administrator. Submit cannot be performed."
    USER_IS_ADMIN_USR_MSG = "You cannot submit experiments as dls4e administrator. Switch your KUBECONFIG " \
                            "environment variable to point to a valid dls4e user config. If you don't have one you " \
                            "can create it with command 'dlsctl user create'."
    HELP_E = "Environment variables passed to training. User can pass as many environmental variables as it is " \
             "needed - each variable should be in such case passed as a separate -e parameter."
    HELP_R = "Path to file with experiment's pip requirements." \
             " Dependencies listed in this file will be automatically installed using pip."
    SCRIPT_NOT_FOUND_ERROR_MSG = "Cannot find: {script_location}. Make sure that provided path is correct."
    DEFAULT_SCRIPT_NOT_FOUND_ERROR_MSG = "Cannot find script: {default_script_name} in directory: " \
                                         "{script_directory}. If path to directory was passed as submit command " \
                                         "argument, then {default_script_name} file has to exist in that directory."
    SCRIPT_DIR_NOT_FOUND_ERROR_MSG = "Cannot find: {script_folder_location}. script_folder_location must be a path " \
                                     "to existing directory. "
    DUPLICATED_PACK_PARAM = "Pack param was provided more than once. Set '{pack_param}' param correctly."
    SUBMIT_START_LOG_MSG = "Submit - start"
    SUBMIT_START_USER_MSG = "Submitting experiments."
    SUBMIT_ERROR_MSG = "Problems during submitting experiment: {exception_message}"
    SUBMIT_OTHER_ERROR_MSG = "Other problems during submitting experiment."
    FAILED_RUNS_LOG_MSG = "There are failed runs"


class ExperimentInteractCmdTexts:
    SHORT_HELP = "Launches a local browser with Jupyter Notebook."
    HELP = "Launches a local browser with Jupyter Notebook. If the script name argument is given, then script is put " \
           "into the opened notebook."
    HELP_N = "The name of this Jupyter Notebook session."
    HELP_F = "File with a notebook or a python script that should be opened in Jupyter notebook."
    HELP_PN = "Port on which service will be exposed locally."
    HELP_P = " Additional pack param in format: 'key value' or 'key.subkey.subkey2 value'. For lists use: " \
             "'key \"['val1', 'val2']\"' For maps use: 'key \"{'a': 'b'}\"' "
    HELP_NO_LAUNCH = "Run command without a web browser starting, only proxy tunnel is created"
    EXPERIMENT_GET_ERROR_MSG = "Problems during loading a list of experiments."
    NAME_ALREADY_USED = "The chosen name ({name}) is already used by an experiment other than Jupyter Notebook. " \
                        "Please choose another one."
    CONFIRM_EXPERIMENT_CREATION = "Experiment with a given name doesn't exist. Should the app continue and create a " \
                                  "new one? "
    SUBMITTING_EXPERIMENT_USER_MSG = "Submitting interactive experiment."
    SUBMIT_ERROR_MSG = "Error during starting jupyter notebook session: {exception_message}"
    SUBMIT_OTHER_ERROR_MSG = "Other error during starting jupyter notebook session."
    SESSION_EXISTS_MSG = "Jupyter notebook's session exists. dlsctl connects to this session ..."
    NOTEBOOK_STATE_CHECK_ERROR_MSG = "Error during checking state of Jupyter notebook."
    ATTACHING_SCRIPT_NOT_SUPPORTED_MSG = "Attaching script to existing Jupyter notebook's session is not supported. " \
                                         "Please create a new Jupyter notebook's session to attach script."
    NOTEBOOK_NOT_READY_ERROR_MSG = "Jupyter notebook is still not ready. Please try to connect to it by running " \
                                   "interact command another time passing a name of a current Jupyter notebook " \
                                   "session."
    PROXY_CLOSING_ERROR_MSG = "K8s proxy hasn't been closed properly. Check whether it still exists, if yes - close " \
                              "it manually."
    SESSION_LAUNCH_OTHER_ERROR_MSG = "Other exception during launching interact session."
    EXP_WITH_THE_SAME_NAME_MUST_BE_PURGED = "Notebook with the same name exists but is in state other than RUNNING. " \
                                            "If you want to start another notebook using the same name, please " \
                                            "purge the previous one."
    HELP_E = "Environment variables passed to Jupyter instance. User can pass as many environmental variables as " \
             "it is needed - each variable should be in such case passed as a separate -e paramater."
    HELP_T = "Name of a jupyter notebook template used to create a deployment. " \
             "Supported templates for interact command are: jupyter (python3) and jupyter-py2 (python2)"


class ExperimentCancelCmdTexts:
    SHORT_HELP = "Cancels experiment/s or deletes pods chosen based on criteria given as parameters."
    HELP = """
    Cancels experiment/s or deletes pods chosen based on criteria given as parameters.

    name - is a name of experiment which should be cancelled, name argument value can be empty when 'match'
    option is used.
    """
    HELP_P = "If given, then all information concerning all experiments, completed and currently running, is removed " \
             "from the system."
    HELP_M = "If given, command searches for experiments matching the value of this option. This option cannot be " \
             "used along with the name argument."
    HELP_I = "Comma-separated pods IDs - if given then matches pods by their IDs and deletes them."
    HELP_S = "One of: {available_statuses} - searches pods by their status and deletes them."
    NAME_M_BOTH_GIVEN_ERROR_MSG = "Both name and -m option cannot be given. Please choose one of them."
    NAME_M_NONE_GIVEN_ERROR_MSG = "Error: Name or -m option must be given. Please pass one of them."
    LIST_RUNS_ERROR_MSG = "Problems during loading a list of {experiment_name_plural}."
    LACK_OF_EXPERIMENTS_ERROR_MSG = "Lack of {experiment_name_plural} fulfilling given criteria. Name or match " \
                                    "string parameters do not match any existing {experiment_name} in an appropriate " \
                                    "state for the command. Run 'dlsctl exp list' to find out what are the names and " \
                                    "states of existing {experiment_name_plural}."
    CANCEL_OPERATION = {
        "cancelled": "cancelled",
        "cancellation": "cancellation"
    }
    DELETE_OPERATION = {
        "deleted": "deleted",
        "deletion": "deletion"
    }
    EXPERIMENTS_ALREADY_CANCELLED_ERROR_MSG = "{experiment_name_plural} fulfilling given criteria have been " \
                                              "{operation_word} already."
    ALREADY_CANCELLED_LIST_HEADER = "The following {experiment_name_plural} have been {operation_word} already or " \
                                    "cannot be {operation_word} due to their current state:"
    CAN_BE_CANCELLED_LIST_HEADER = "The following {experiment_name_plural} can still be {operation_word}:"
    WILL_BE_CANCELLED_LIST_HEADER = "The following {experiment_name_plural} will be {operation_word}:"
    WILL_BE_PURGED_LIST_HEADER = "The following {experiment_name_plural} will be {operation_word}:"
    CONFIRM_CANCEL_MSG = "Do you want to continue with {operation_word} of those {experiment_name_plural}?"
    CANCELLATION_ABORTED_MSG = "Operation of {operation_word} of {experiment_name_plural} was aborted."
    OTHER_CANCELLING_ERROR_MSG = "Error during cancelling an experiment."
    PROXY_CLOSING_ERROR_LOG_MSG = "Error during closing of a proxy for elasticsearch."
    PROXY_CLOSING_ERROR_USER_MSG = "Elasticsearch proxy hasn't been closed properly. Check whether it still exists, " \
                                   "if yes - close it manually."
    PORT_OCCUPIED_ERROR_LOG_MSG = "Error during creation of proxy - port is occupied."
    PORT_OCCUPIED_ERROR_USER_MSG = "Error during creation of a proxy for elasticsearch. {exception_message}"
    PROXY_OPEN_ERROR_MSG = "Error during creation of a proxy for elasticsearch."
    SUCCESSFULLY_CANCELLED_LIST_HEADER = "The following {experiment_name_plural} were {operation_word} successfully:"
    FAILED_TO_CANCEL_LIST_HEADER = "The following {experiment_name_plural} weren't {operation_word} properly:"
    GET_EXPERIMENT_ERROR_MSG = "Error during loading experiment's data."
    PURGING_START_MSG = "Purging {run_name} experiment ..."
    INCOMPLETE_PURGE_ERROR_MSG = "Not all {experiment_name}'s components were removed properly."
    CANCELING_RUNS_START_MSG = "Cancelling {run_name} {experiment_name} ..."
    DELETING_RELATED_OBJECTS_MSG = "Deleting objects related to {run_name} {experiment_name} ..."
    CANCEL_SETTING_STATUS_MSG = "Setting {run_name} status to CANCELLED ..."
    INCOMPLETE_CANCEL_ERROR_MSG = "Not all components of {run_name} {experiment_name} were deleted ...\nExperiment " \
                                  "remains in its previous state."
    BAD_POD_STATUS_PASSED = "Wrong status: {status_passed} , available: {available_statuses}"
    LACK_OF_PODS_ERROR_MSG = "Lack of pods fulfilling given criteria. Pod ID or pod status parameters do not match " \
                             "any existing pod."
    CANCELING_PODS_MSG = "Deleting the pod: {pod_name} ..."
    OTHER_POD_CANCELLING_ERROR_MSG = "Error during deleting the pod."
    UNINITIALIZED_EXPERIMENT_CANCEL_MSG = "Experiment {experiment_name} has no resources submitted for creation."
    PURGING_PROGRESS_MSG = 'Purging experiment {run_name}...'
    PURGING_LOGS_PROGRESS_MSG = 'Purging experiment {run_name} logs...'


class ExperimentViewCmdTexts:
    SHORT_HELP = "Displays details of experiment with a given name."
    HELP = """
    Displays details of experiment with a given name.

    EXPERIMENT_NAME - is a name of experiment whose details should be displayed.
    """
    HELP_T = "If given, then exposes a tensorboard's instance with experiment's data."
    CONTAINER_DETAILS_MSG = "- Name: {name}\n- Status: {status}\n- Volumes:\n  {volumes}\n- Resources:  {resources}"
    EXPERIMENT_NOT_FOUND_ERROR_MSG = "Experiment \"{experiment_name}\" not found."
    PODS_PARTICIPATING_LIST_HEADER = "\nPods participating in the execution:\n"
    PODS_TABLE_HEADERS = ["Name", "Uid", "Pod Conditions", "Container Details"]
    VIEW_OTHER_ERROR_MSG = "Failed to get experiment."
    CONTAINER_NOT_CREATED_MSG = "Not created"
    CONTAINER_RUNNING_MSG = "Running, started at: "
    CONTAINER_TERMINATED_MSG = "Terminated, "
    CONTAINER_WAITING_MSG = "Waiting, "
    CONTAINER_REQUESTS_LIST_HEADER = "- Requests:\n{}"
    CONTAINER_LIMITS_LIST_HEADER = "- Limits:\n{}"
    RESOURCES_SUM_LIST_HEADER = "\nResources used by pods:\n"
    RESOURCES_SUM_PARSING_ERROR_MSG = "There was an error when trying to parse pods resources. Error msg: {error_msg}"
    RESOURCES_SUM_TABLE_HEADERS = ["Resource type", "Total usage"]
    RESOURCES_SUM_TABLE_ROWS_HEADERS = ["CPU requests:", "Memory requests:", "CPU limits:", "Memory limits:"]
    INSUFFICIENT_RESOURCES_MESSAGE = "Experiment is in QUEUED state due to insufficient {resources}."
    TOP_CPU_CONSUMERS = "Top CPU consumers: {consumers}"
    TOP_MEMORY_CONSUMERS = "Top memory consumers: {consumers}"
    PROBLEMS_WHILE_GATHERING_USAGE_DATA = "Reasons of QUEUED state and top consumers cannot be displayed due to " \
                                          "errors."
    PROBLEMS_WHILE_GATHERING_USAGE_DATA_LOGS = "Error when gathering consumers data."
    HELP_U = "Name of a user to who belongs viewed experiment. If not given - only experiments of a current " \
             "user are taken into account."
    REASON = "\n  Reason: "


class ExperimentCommonTexts:
    CONFIRM_EXP_DIR_DELETION_MSG = "Experiment data directory: {run_environment_path} already exists. It will be " \
                                   "deleted in order to proceed with experiment submission. Do you want to continue?"
    UNABLE_TO_CONTINUE_EXP_SUBMISSION_ERROR_MSG = "Cannot continue experiment submission. Please delete experiment's " \
                                                  "data directory {run_environment_path} manually or use different " \
                                                  "name for experiment."
    CREATE_ENV_MSG_PREFIX = "Experiment's environment hasn't been created. Reason - {reason}"
    DIR_CANT_BE_COPIED_ERROR_TEXT = "Additional folder cannot be copied into experiment's folder."
    EXP_DIR_CANT_BE_CREATED = "Folder with experiments' data cannot be created."
    TRAINING_SCRIPT_CANT_BE_CREATED = "Training script cannot be created."
    GET_NAMESPACE_ERROR_MSG = "Failed to get current Kubernetes namespace."
    SUBMIT_PREPARATION_ERROR_MSG = "Problem during preparation of experiments' data."
    LOCAL_DOCKER_TUNNEL_ERROR_MSG = "Error during creation of a local docker-host tunnel."
    ENV_CREATION_ERROR_MSG = "Problems during creation of environments."
    CONFIRM_SUBMIT_MSG = "Please confirm that the following experiments should be submitted."
    CONFIRM_SUBMIT_QUESTION_MSG = "Do you want to continue?"
    SUBMISSION_FAIL_ERROR_MSG = "Experiment submission failed. Try verbose option for more detailed information " \
                                "about failure cause."
    PROXY_CLOSE_ERROR_MSG = "Docker proxy hasn't been closed properly. Check whether it still exists, if yes - close " \
                            "it manually."
    PROXY_OPEN_ERROR_MSG = "Error during opening of a proxy for a docker registry."
    SUBMIT_OTHER_ERROR_MSG = "Other error during submitting experiments."
    DOCKER_TUNNEL_CLOSE_ERROR_MSG = "Local Docker-host tunnel hasn't been closed properly. Check whether it still " \
                                    "exists, if yes - close it manually."
    DRAFT_TEMPLATES_NOT_GENERATED_ERROR_MSG = "Draft templates haven't been generated. Reason - {reason}"
    JOB_NOT_DEPLOYED_ERROR_MSG = "Job hasn't been deployed."
    JOB_NOT_DEPLOYED_ERROR_MSG_LOGFILE = "For more details run: draft logs {log_filename}"
    INCORRECT_PARAM_FORMAT_ERROR_MSG = "Parameter {param_name} has incorrect format."
    PARAM_AMBIGUOUSLY_DEFINED = "Parameter {param_name} ambiguously defined."
    PARAM_SET_INCORRECT_FORMAT_ERROR_MSG = "One of -ps options has incorrect format."
    INVALID_PACK_PARAM_FORMAT_ERROR_MSG = "Invalid pack params format for param: {key}. Key cannot contain '='. " \
                                          "Specify pack params in format 'key value' not as 'key=value'."
    EXPERIMENT_NAME_TOO_LONG_ERROR_MSG = "Name given by a user cannot be longer than 30 characters."
    ERROR_DURING_PATCHING_RUN = "Error during patching a run occured {}."
    PROBLEMS_DURING_GETTING_DRAFT_LOGS = "Error during getting draft logs : {exception}"
    THE_SAME_EXP_IS_SUBMITTED = "There is another experiment with the same name submitted at this moment."
    PREPARING_RESOURCE_DEFINITIONS_MSG = "Preparing resources' definitions..."
    CLUSTER_CONNECTION_MSG = "Connecting to the cluster..."
    CREATING_ENVIRONMENT_MSG = "Creating {run_name} environment..."
    CREATING_RESOURCES_MSG = "Creating {run_name} resources..."
    CLUSTER_CONNECTION_CLOSING_MSG = "Closing tunnel to the cluster..."
    INCORRECT_TEMPLATE_NAME = "Incorrect template name."
    INCORRECT_ENV_PARAMETER = "-e/--env option must be in <KEY>=<VALUE> format."
    INCORRECT_PACK_DEFINITION = "Definition of the {pack_name} pack is incorrect."


class DraftCmdTexts:
    DOCKER_IMAGE_NOT_BUILT = "Docker image hasn't been built."
    DOCKER_IMAGE_NOT_SENT = "Docker image hasn't been sent to the cluster."
    APP_NOT_RELEASED = "Application hasn't been released."
    DEPLOYMENT_NOT_CREATED = "Deployment hasn't been created."
    PACK_NOT_EXISTS = "Chosen pack doesn't exist."


class PacksTfTrainingTexts:
    CONFIG_NOT_UPDATED = "Configuration hasn't been updated."
    CANT_PARSE_VALUE = "Can not parse value: \"{value}\" to list/dict. Error: {error}"


class UtilSystemTexts:
    COMMAND_EXE_FAIL_ERROR_MSG = "COMMAND execution FAIL: {command}"
    UNSUPPORTED_PLATFORM_ERROR_MSG = "unsupported platform: {sys_platform}, supported: {supported_os}!"
    PORT_AVAILABILITY_CHECK_ERROR_MSG = "Problem during checking port's availability."


class UtilSocatTexts:
    SOCAT_CONTAINER_START_FAIL_MSG = "failed to start socat container! expected status: 'running', got: " \
                                     "{container_status}"


class UtilJupyterTexts:
    IPYNB_CONVERSION_ERROR_MSG = "Py to Ipynb conversion error."


class UtilLauncherTexts:
    LOCAL_DOCKER_TUNNEL_ERROR_MSG = "Error during creation of a local docker-host tunnel."
    BROWSER_STARTING_MSG = "Browser will start in few seconds. Please wait..."
    CANNOT_USE_PORT = "Cannot use required port {required_port}. Port has been set automatically to {random_port}"
    NO_WEB_BROWSER_ERROR_MSG = "Cannot find a suitable web browser - running with --no-launch option."
    PROXY_CLOSE_ERROR_MSG = "Error during closing of a proxy for a {app_name}"
    WEB_APP_LAUCH_FAIL_MSG = "Failed to launch web application."
    WEB_APP_CLOSING_MSG = "Closing all connections. Please wait..."
    GO_TO_MSG = "Go to {url}"
    PROXY_CREATED_MSG = "Proxy connection created.\nPress Ctrl-C key to close a port forwarding process..."
    PROXY_CREATED_ERROR_MSG = "Error during creation of a proxy for a {app_name}."
    PROXY_CREATED_EXTENDED_ERROR_MSG = "Error during creation of a proxy for a {app_name}. {reason}"
    LAUNCHING_APP_MSG = "Launching..."


class UtilHelmTexts:
    HELM_RELEASE_REMOVAL_ERROR_MSG = "Error during removal of helm release {release_name}."


class TensorboardClientTexts:
    INVALID_RUNS_ERROR_MSG = "There is no data for the following experiments : {invalid_runs_list}"
    RUNS_NOT_EXIST_ERROR_MSG = "Experiments given as parameters of the command don't exist."


class UtilDockerTexts:
    TAGS_GET_ERROR_MSG = "Error during getting list of tags for an image."
    IMAGE_DELETE_ERROR_MSG = "Error during deletion of an image."


class UtilDependenciesCheckerTexts:
    PARSE_FAIL_ERROR_MSG = "Failed to parse version({version_field}) from following input: {version_output}"
    VERSION_CMD_FAIL_MSG = "Failed to run {version_cmd} with args {version_cmd_args}. Output: {output}"
    DEPENDENCY_NOT_INSTALLED_ERROR_MSG = "{dependency_name} is not installed."
    VERSION_GET_FAIL_MSG = "Failed to get {dependency_name} version."
    INVALID_DEPENDENCY_ERROR_MSG = "{dependency_name} installed version: {installed_version}, does not match " \
                                   "expected version: {expected_version}"
    UNKNOWN_OS_ERROR_MSG = "Unknown OS version."
    GET_OS_VERSION_ERROR_MSG = "Could not determine OS version"
    UNSUPPORTED_OS_ERROR_MSG = "This OS ({os_name} {os_version}) is not supported. Please check the list of " \
                               "supported OS."
    INVALID_OS_VERSION_ERROR_MSG = "This version ({os_name} {os_version}) of the OS is not supported. Please check " \
                                   "the list of supported OS."


class UtilConfigTexts:
    USER_DIR_NOT_FOUND_ERROR_MSG = "Cannot find {user_path} directory from {config_env_name} env!"
    DLS_CTL_CONFIG_DIR_NOT_FOUND_ERROR_MSG = "Cannot find {config_dir_name} directory in {binary_config_dir_path} " \
                                             "and {user_local_config_dir_path}. Use {config_env_name} env to point " \
                                             "{config_dir_name} directory location"


class PlatformResourcesCustomModelTexts:
    INVALID_K8S_NAME = "name must consist of lower case alphanumeric characters, '-' or '.', and must start with " \
                       "alphabetic character and end with an alphanumeric character "


class PlatformResourcesExperimentsTexts:
    REGEX_COMPILATION_FAIL_MSG = "Failed to compile regular expression: {name_filter}"
    K8S_RESPONSE_LOAD_ERROR_MSG = "preparing load of ExperimentKubernetes response object error - {err}"
    K8S_DUMP_PREPARATION_ERROR_MSG = "preparing dump of ExperimentKubernetes request object error - {err}"
    EXPERIMENT_ALREADY_EXISTS_ERROR_MSG = " experiment with name: {name} already exist!"
    EXPERIMENT_INVALID_STATE_MSG = " experiment with name: {name} already exist, " \
                                   "but it doesn't have any resources submitted for creation. " \
                                   "In order to create experiment with desired name," \
                                   " purge old experiment using following command: dlsctl experiment cancel --purge" \
                                   " {name}"
    EXPERIMENT_UPDATE_ERROR_MSG = "Error during patching an Experiment"


class PlatformResourcesRunsTexts:
    REGEX_COMPILATION_FAIL_MSG = "Failed to compile regular expression: {name_filter}"
    K8S_RESPONSE_LOAD_ERROR_MSG = "preparing load of RunKubernetes response object error - {err}"
    K8S_DUMP_PREPARATION_ERROR_MSG = "preparing dump of RunKubernetes request object error - {err}"
    RUN_UPDATE_ERROR_MSG = "Error during patching a Run"


class PlatformResourcesUsersTexts:
    USERNAME_CANNOT_BE_EMPTY_ERROR_MSG = "Name of a user cannot be an empty string."
    USERNAME_TOO_LONG_ERROR_MSG = "Name of a user cannot be longer than 32 characters."
    INCORRECT_K8S_USERNAME_ERROR_MSG = "Incorrect k8s user name."
    USERNAME_IS_RESERVED_FOR_SYSTEM_USE = "Unable to create user: username is reserved or blacklisted."

class UtilKubectlTexts:
    NO_AVAILABLE_PORT_ERROR_MSG = "Available port cannot be found."
    PROXY_CREATION_OTHER_ERROR_MSG = "Other error during creation of port proxy."
    PROXY_CREATION_MISSING_PORT_ERROR_MSG = "Missing port during creation of port proxy."
    USER_PRESENCE_CHECK_ERROR_MSG = "Error during checking user's presence."
    K8S_OBJECT_DELETE_ERROR_MSG = "Error when deleting k8s object: {output}"
    K8S_CLUSTER_NO_CONNECTION_ERROR_MSG = "Cannot connect to K8S cluster: {output}"
    TOP_COMMAND_ERROR = "Problems during getting usage of resources."
    TOP_COMMAND_ERROR_LOG = "Incorrect format of data returned by top command: {output}"
    K8S_PORT_FORWARDING_ERROR_MSG = "Cannot forward port from K8S cluster. Check cluster configuration and " \
                                    "proxy settings."


class UtilK8sInfoTexts:
    OTHER_FIND_NAMESPACE_ERROR_MSG = "Other find_namespace error"
    NAMESPACE_DELETE_ERROR_MSG = "Error during deleting namespace {namespace}"
    CONFIG_MAP_ACCESS_ERROR_MSG = "Problem during accessing ConfigMap : {name}."
    LACK_OF_DEFAULT_TOKEN_ERROR_MSG = "Lack of default-token on a list of tokens."
    EMPTY_LIST_OF_TOKENS_ERROR_MSG = "Empty list of tokens."
    GATHERING_USERS_TOKEN_ERROR_MSG = "Problem during gathering users token."
    GATHERING_PASSWORD_ERROR_MSG = "Error during gathering users password."
    LACK_OF_PASSWORD_ERROR_MSG = "Lack of password."
    GATHERING_EVENTS_ERROR_MSG = "Problem during gathering k8s events."
    PATCHING_CM_ERROR_MSG = "Problem during patching configmap."


class UtilK8sProxyTexts:
    PROXY_ENTER_ERROR_MSG = "k8s_proxy - enter - error"
    PROXY_EXIT_ERROR_MSG = "k8s_proxy - exit - error"
    TUNNEL_NOT_READY_ERROR_MSG = "connection on {address}:{port} NOT READY!"
    TUNNEL_ALREADY_CLOSED = "Proxy tunnel is already closed."


class CliStateTexts:
    INVALID_DEPENDENCY_ERROR_MSG = "Dependency check failed."
    KUBECTL_NAMESPACE_ERROR_MSG = "Failed to determine kubectl namespace during verification. This may occur for " \
                                  "example due to invalid path to kubectl config, invalid k8s credentials or k8s " \
                                  "cluster being unavailable. Check your KUBECONFIG environment variable and make " \
                                  "sure that the k8s cluster is online."
    DLSCTL_CONFIG_NOT_SET_ERROR_MSG = "Configuration directory for dlsctl is not set."
    DLSCTL_CONFIG_INIT_ERROR_MSG = "Config initialization failed. Reason: {exception_msg}"


class LicenseAcceptanceTexts:
    LICENSE_ACCEPTANCE_QUESTION_MSG = "DO NOT ACCESS, COPY OR PERFORM ANY PORTION OF THE PRE-RELEASE SOFTWARE " \
                                      "UNTIL YOU HAVE READ AND ACCEPTED THE TERMS AND CONDITIONS OF THIS " \
                                      "AGREEMENT LICENSE.TXT . BY COPYING, ACCESSING, OR PERFORMING " \
                                      "THE PRE-RELEASE SOFTWARE, YOU AGREE TO BE LEGALLY BOUND BY THE TERMS AND " \
                                      "CONDITIONS OF THIS AGREEMENT. Agree?"
    CANNOT_ACCEPT_LICENSE_MSG = "Cannot save license agreement - \"config\" file or directory already exists in " \
                                "{dlsctl_config_path} but this name is reserved for dlsctl app. Please remove it " \
                                "and try again."
