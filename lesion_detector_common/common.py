import os
from common.utils import *
import subprocess as sb
import shutil

def covid_detector_base(param_dict, get_volumes_from_output_directory, output_dir):
    rel_source_file = param_dict["source_file"][0]
    data_share = os.environ["DATA_SHARE_PATH"]

    # remove trailing / at the beggining of name
    # otherwise os.path.join has unwanted behaviour for base dirs
    # i.e. join(/app/data_share, /app/wrongpath) = /app/wrongpath
    rel_source_file = rel_source_file.lstrip('/')

    source_file = os.path.join(data_share, rel_source_file)

    script_path = "/app/code/keras_retinanet/bin/predict_covid.py"
    model_path = "/app/model/vgg19_csv_55.h5"

    input_path, cp_exit_code = __create_and_copy_files_to_tmp_input_directory(source_file)

    if cp_exit_code == 1:
        return {}, False

    tmp_output_path = __create_shared_output_directory()

    lesion_detection_cmd = "cd /app/code && python3 {} --model={} --gpu=0 --save-path={} nii {}" \
        .format(script_path, model_path, tmp_output_path, input_path)

    log_debug("Running", lesion_detection_cmd)
    exit_code = sb.call([lesion_detection_cmd], shell=True)
    if exit_code == 1:
        return {}, False

    shutil.rmtree(input_path)

    # get names of files
    files = os.listdir(tmp_output_path)

    print(files)
    assert len(files) == 2

    mask_volume, detection_volume = get_volumes_from_output_directory(files)

    print(mask_volume, detection_volume)
    if mask_volume == "" or detection_volume == "":
        return {}, False

    rel_mask_volume_path = os.path.join(output_dir, mask_volume)
    rel_detection_volume_path = os.path.join(output_dir, detection_volume)

    log_debug("rel attention volume", rel_mask_volume_path)
    log_debug("rel detection volume", rel_detection_volume_path)

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
        "auxiliary_volume": rel_mask_volume_path,
        "detection_volume": rel_detection_volume_path
    }

    return result_dict, True

def __create_and_copy_files_to_tmp_input_directory(source_file):
    tmp = "/tmp"
    input_path = os.path.join(tmp, "input")

    if os.path.exists(input_path):
        shutil.rmtree(input_path)

    os.mkdir(input_path)

    cp_cmd = "cp {} {}".format(source_file, input_path)
    log_debug("Running", cp_cmd)
    cp_exit_code = sb.call([cp_cmd], shell=True)
    return input_path, cp_exit_code

def __create_shared_output_directory():
    # TODO not thread safe
    tmp_output_path = "/tmp/output"
    if os.path.exists(tmp_output_path):
        shutil.rmtree(tmp_output_path)

    os.mkdir(tmp_output_path)

    return tmp_output_path