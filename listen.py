from common.utils import *
from common import listener_server
import os
import subprocess as sb
import shutil
import time

output_dir = "covid_lesion_detection_seg_output"
output_path = os.path.join(os.environ["DATA_SHARE_PATH"], output_dir)


def covid_detector_seg(param_dict):
    rel_source_file = param_dict["source_file"][0]
    data_share = os.environ["DATA_SHARE_PATH"]
    source_file = os.path.join(data_share, rel_source_file)

    script_path = "/app/code/keras_retinanet/bin/predict_covid.py"
    model_path = "/app/model/vgg19_csv_55.h5"

    tmp = "/tmp"
    input_path = os.path.join(tmp, "input")

    if os.path.exists(input_path):
        shutil.rmtree(input_path)

    os.mkdir(input_path)

    cp_cmd = "cp {} {}".format(source_file, input_path)
    log_debug("Running", cp_cmd)
    cp_exit_code = sb.call([cp_cmd], shell=True)
    if cp_exit_code == 1:
        return {}, False

    # TODO not thread safe
    tmp_output_path = "/tmp/output"
    if os.path.exists(tmp_output_path):
        shutil.rmtree(tmp_output_path)

    os.mkdir(tmp_output_path)

    lesion_detection_cmd = "cd /app/code && python3 {} --model={} --gpu=0 --save-path={} nii {}" \
        .format(script_path, model_path, tmp_output_path, input_path)

    log_debug("Running", lesion_detection_cmd)
    exit_code = sb.call([lesion_detection_cmd], shell=True)
    if exit_code == 1:
        return {}, False

    shutil.rmtree(input_path)

    # get names of files
    files = os.listdir(tmp_output_path)
    mask_volume = ""
    detection_volume = ""


    print(files)

    assert len(files) == 2

    for file in files:

        if "mask" in file:
            mask_volume = file
        elif "detection" in file:
            detection_volume = file


    print(mask_volume, detection_volume)
    if mask_volume == "" or detection_volume == "":
        return {}, False

    rel_mask_volume_path = os.path.join(output_dir, mask_volume)
    rel_detection_volume_path = os.path.join(output_dir, detection_volume)

    log_debug("rel attention volume", rel_mask_volume_path)
    log_debug("rel detection volume", rel_detection_volume_path)

    # os.rename()
    # os.rename(, )

    tmp_mask_path = os.path.join(tmp_output_path, mask_volume)
    data_share_mask_path = os.path.join(data_share, rel_mask_volume_path)
    mv_cmd1 = "mv {} {}".format(tmp_mask_path, data_share_mask_path)
    sb.call([mv_cmd1], shell=True)

    tmp_volume_path = os.path.join(tmp_output_path, detection_volume)
    data_share_volume_path = os.path.join(data_share, rel_detection_volume_path)
    mv_cmd2 = "mv {} {}".format(tmp_volume_path, data_share_volume_path)
    sb.call([mv_cmd2], shell=True)


    shutil.rmtree(tmp_output_path)

    result_dict = {
        "mask_volume": rel_mask_volume_path,
        "detection_volume": rel_detection_volume_path
    }

    return result_dict, True


if __name__ == "__main__":

    setup_logging()
    log_info("Started listening")

    served_requests = {
        "/covid_detector_seg_nifti": covid_detector_seg
    }

    # make output dir

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    listener_server.start_listening(served_requests, multithreaded=True, mark_as_ready_callback=mark_yourself_ready)

