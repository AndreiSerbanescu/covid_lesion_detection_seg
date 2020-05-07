import os
from common.utils import *
from common.exceptions import TaskFailedException
import glob

class FileValidatorNiftiOnly:

    def __init__(self, print_statements=False):
        self.print_statements = print_statements

    def files_valid(self, files):

        if len(files) == 0:
            if self.print_statements:
                log_error(f"No files found")

            return False

        if files[0].endswith(".dcm"):
            if self.print_statements:
                log_error(f"Not able to compute task for dicom files (only nifti .nii.gz)")

            return False

        if not files[0].endswith(".nii.gz"):
            if self.print_statements:
                log_error(f"Unknown file extension")

            return False

        return True

    def get_fullpath(self, files, element_input_dir):
        return os.path.join(element_input_dir, files[0])


class NiftiAndDicomFileValidator:

    def __init__(self, print_statements=False):
        self.print_statements = print_statements

    def files_valid(self, files):

        if len(files) == 0:
            if self.print_statements:
                log_error("No files found")

            return False

        if not files[0].endswith(".nii.gz") and not files[0].endswith(".dcm"):
            if self.print_statements:
                log_error("Unknown file extension")

            return False

        return True

    def get_fullpath(self, files, element_input_dir):
        if files[0].endswith(".nii.gz"):
            return os.path.join(element_input_dir, files[0])

        if files[0].endswith(".dcm"):
            return element_input_dir

        assert False



def compute_task(task_method, source_file):
    try:
        task_output, success = task_method(source_file)
    except Exception as e:
        raise TaskFailedException(str(e))

    if not success:
        raise TaskFailedException()

    return task_output

def start_batch_job(handle_output_callback, task_method, file_validator=None):

    if file_validator is None:
        file_validator = FileValidatorNiftiOnly(print_statements=True)

    setup_logging()

    batch_folders = [f for f in glob.glob(os.path.join('/', os.environ['WORKFLOW_DIR'], os.environ['BATCH_NAME'], '*'))]

    for batch_element_dir in batch_folders:

        element_input_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_IN_DIR'])
        element_output_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_OUT_DIR'])
        os.makedirs(element_output_dir, exist_ok=True)

        files = os.listdir(element_input_dir)

        if not file_validator.files_valid(files):
            log_error(f"Files inputted not valid for {element_input_dir}")
            log_error("Skipping")
            continue

        abs_source_file = file_validator.get_fullpath(files, element_input_dir)

        try:
            task_output = compute_task(task_method, source_file=abs_source_file)
        except TaskFailedException as e:
            log_error(f"Task failed with exception {e}")
            log_error("Skipping")
            continue

        handle_output_callback(task_output, element_output_dir)
