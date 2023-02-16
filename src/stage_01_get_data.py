import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from src.utils.common import create_directories, read_config
from src.Logger.logger import logger
import mlflow
import argparse
STAGE = "stage_01_get_data"

class get_data:
    def __init__(self, config_file='config/config.yaml', param_file='config/params.yaml'):
        self.logs = logger(config_file)
        self.logs.write_log(f"In src.get_data")
        try:
            self.content = read_config(config_file)
            self.params = read_config(param_file)
        except Exception as e:
            self.logs.write_exception(e)

    def get_train_test_data(self):
        root_data_dir = self.content['root_data_dir']
        create_directories([root_data_dir])
        try:
            train_ds = datasets.FashionMNIST(root=root_data_dir, train=True,  download=True, transform=transforms.ToTensor())
            test_ds = datasets.FashionMNIST(root=root_data_dir, train=False, download=True,transform=transforms.ToTensor())
            # self.logs.write_log(f"Data downloaded successfully. ")
        except Exception as e:
            self.logs.write_exception(e)
        # with mlflow.start_run():
        mlflow.log_artifacts(root_data_dir)
        return train_ds, test_ds

    def create_data_loader(self):
        try:
                
            batch_size = self.params['batch_size']
            train_ds, test_ds = self.get_train_test_data()
            train_data_loader = DataLoader(dataset=train_ds, batch_size=batch_size, shuffle=True)
            self.logs.write_log(f"train_data_loader created")
            test_data_loader =  DataLoader(dataset=test_ds, batch_size=batch_size)
            self.logs.write_log(f"test_data_loader created")
            return train_data_loader, test_data_loader
        except Exception as e:
            self.logs.write_exception(e)


    def get_label_idx(self):
        try:
            train_ds, test_ds = self.get_train_test_data()
            label_idx = {val: key for key, val in train_ds.class_to_idx.items()}
            return label_idx
        except Exception as e:
            self.logs.write_exception(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '--c', default="config/config.yaml")
    parser.add_argument('--params', '--p', default="configs/params.yaml")
    parsed_args = parser.parse_args()
    logs = logger(parsed_args.config)
    try:
        logs.write_log(f"*********** {STAGE} started **************")
        get_data_ob = get_data(parsed_args.config, parsed_args.params)
        get_data_ob.create_data_loader()
        label_idx = get_data_ob.get_label_idx()
        logs.write_log(label_idx)
        # mlflow.log_dict(label_idx, "label.yaml") # log dict in yaml format inside mlrun/runid/artifacts/
        # mlflow.log_dict(label_idx, "label") # log dict in json
        logs.write_log(f"*********** {STAGE} completed **************")
    except Exception as e:
        logs.write_exception(e)
        print(e)
