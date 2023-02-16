import torch
import torch.nn as nn
import torch.nn.functional as F
from src.Logger.logger import logger
from src.utils.model_utils import get_model_params, save_model
from src.utils.common import create_directories, read_config
import argparse
import pandas as pd
import os
import mlflow
import mlflow.pytorch
STAGE = "stage_02_base_model_creation"

class BaseModelCreation(nn.Module):
    def __init__(self, _in, out_):
        super(BaseModelCreation, self).__init__()

        # define the neural network here

        self.conv_max_pool_01 = nn.Sequential(nn.Conv2d(in_channels=_in, out_channels=8, kernel_size=5, stride=1, padding=0),
                                           nn.ReLU(),
                                           nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
                                        )
        
        self.conv_max_pool_02 = nn.Sequential(nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=0),
                                           nn.ReLU(),
                                           nn.MaxPool2d(kernel_size=2, stride=2)
                                        )
        self.flatten = nn.Flatten()
        self.FC_01 = nn.Linear(in_features=16*5*5, out_features=128)
        self.FC_02 = nn.Linear(in_features=128, out_features=64)
        self.FC_03 = nn.Linear(in_features=64, out_features=32)
        self.FC_04 = nn.Linear(in_features=32, out_features=out_)

        # define forward pass

    def forward(self, x):

        x = self.conv_max_pool_01(x)
        x = self.conv_max_pool_02(x)
        x = self.flatten(x)
        x = self.FC_01(x)
        x = F.relu(x)
        x = self.FC_02(x)
        x = F.relu(x)
        x = self.FC_03(x)
        x = F.relu(x)
        x = self.FC_04(x)
        x = F.relu(x)
        x = F.softmax(x, dim=1)
        return x

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', '--c', default='config/config.yaml')
        parsed_arg = parser.parse_args()
        logs = logger(parsed_arg.config)
        logs.write_log(f"********* {STAGE} STARTED ***********")
        base_model = BaseModelCreation(1,10)
        logs.write_log(f"Base model architecture is {base_model}")
        config = read_config(parsed_arg.config)
        model_root_dir = config['Model']['Model_root_dir']
        create_directories([model_root_dir])
        model_name = config['Model']['base_model']
        path_to_model = os.path.join(model_root_dir, model_name)
        torch.save(base_model, path_to_model)
        logs.write_log(f'base model saved at {path_to_model}')        
        # df = get_model_params(base_model)
        # logs.write_log(f"param details for model are \n{df.to_string()}")
    except Exception as e:
        logs.write_exception(e)
