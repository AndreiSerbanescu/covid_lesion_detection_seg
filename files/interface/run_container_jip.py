from common_jip.batch_job import start_batch_job, FileValidatorNiftiOnly
from listen import covid_detector_absolute
import os
import shutil

def handle_output(task_output, element_output_dir):

    rel_attention_path = task_output["auxiliary_volume"]
    rel_detection_path = task_output["detection_volume"]

    data_share = os.environ["DATA_SHARE_PATH"]
    full_attention_path = os.path.join(data_share, rel_attention_path)
    full_detection_path = os.path.join(data_share, rel_detection_path)

    element_attention_output_name = os.path.join(element_output_dir, "mask.nii.gz")
    element_detection_output_name = os.path.join(element_output_dir, "detection.nii.gz")

    shutil.copyfile(full_attention_path, element_attention_output_name)
    shutil.copyfile(full_detection_path, element_detection_output_name)

if __name__ == "__main__":

    file_validator = FileValidatorNiftiOnly(print_statements=True)
    start_batch_job(handle_output, covid_detector_absolute, file_validator=file_validator)
