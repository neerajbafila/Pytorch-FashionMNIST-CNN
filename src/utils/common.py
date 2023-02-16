import os
import sys
from pathlib import Path
import yaml
import datetime

def read_config(config_file='config/config.yaml'):
    config_file = Path(config_file)
    with open(config_file, "r") as yaml_file:
        content = yaml.safe_load(yaml_file)
    # print(content)
    return content
    


def create_directories(path_to_dir: list):
    try:

        full_path = ''
        for folder in path_to_dir:
            full_path = os.path.join(full_path, folder)
        os.makedirs(full_path, exist_ok=True)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = exc_tb.tb_lineno
        file_name= exc_tb.tb_frame.f_code.co_filename
        print(f"Exception occurred \nexc_type {exc_type}, exc_obj {exc_obj}, line_no {line_no}, file_name {file_name}")


def unique_name():
    now = datetime.datetime.now()
    name = now.strftime("%y-%m-%d")
    return name
