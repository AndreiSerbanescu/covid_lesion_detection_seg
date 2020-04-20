from common.utils import *
from common import listener_server
from lesion_detector_common.common import *
import os

output_dir = "covid_lesion_detection_seg_output"
output_path = os.path.join(os.environ["DATA_SHARE_PATH"], output_dir)


def __get_mask_and_detection_volumes(files):

    mask_volume = ""
    detection_volume = ""

    for file in files:
        if "mask" in file:
            mask_volume = file
        elif "detection" in file:
            detection_volume = file

    return mask_volume, detection_volume



def covid_detector_seg(param_dict):
    return covid_detector_base(param_dict, __get_mask_and_detection_volumes, output_dir)


if __name__ == "__main__":

    setup_logging()
    log_info("Started listening")

    served_requests = {
        "/covid_detector_seg_nifti": covid_detector_seg
    }

    # make output dir

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    listener_server.start_listening(served_requests, multithreaded=True,
                                    mark_as_ready_callback=mark_yourself_ready)

