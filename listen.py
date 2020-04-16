from common.utils import *
from common import listener_server


def covid_detector_seg(param_dict):
    return ""


if __name__ == "__main__":

    setup_logging()
    log_info("Started listening")

    served_requests = {
        "/covid_detector_seg_nifti": covid_detector_seg
    }

    listener_server.start_listening(served_requests, multithreaded=True, mark_as_ready_callback=mark_yourself_ready)

