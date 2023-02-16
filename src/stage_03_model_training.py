import torch
from tqdm import tqdm
import argparse
import os
import torch.nn as nn
from src.Logger.logger import logger
from src.utils.common import read_config
from src.utils.model_utils import save_model, load_model
from src.stage_02_base_model_creation import BaseModelCreation
from src.stage_01_get_data import get_data

STAGE = "stage_03_model_training"

class Training:
    def __init__(self, config_path, param_path, base_model_path):
        self.config = read_config(config_path)
        self.params = read_config(param_path)
        self.logs = logger(config_path)
        try:
            self.loaded_model = load_model(base_model_path)
            # print(self.loaded_model.parameters)
            self.get_data_ob = get_data(config_path, param_path)
        except Exception as e:
            self.logs.write_exception(e)

    def training(self):
        try:
            train_data_loader, test_data_loader = self.get_data_ob.create_data_loader()
            epochs = self.params['EPOCHS']
            lr = self.params['learning_rate']
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.loaded_model = self.loaded_model.to(device)
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.loaded_model.parameters(), lr=lr)
            print(device)
            
            for epoch in range(epochs):
                with tqdm(train_data_loader) as tqdm_data_loader:
                    for images, labels in tqdm_data_loader:
                        tqdm_data_loader.set_description(f"{epoch}/{epochs}")
                        # put data into device 
                        images = images.to(device)
                        labels = labels.to(device)
                        # forward pass
                        outputs = self.loaded_model(images)
                        # calculate loss
                        loss = criterion(outputs, labels)
                        # clear privios grad
                        optimizer.zero_grad()
                        # calculate grad
                        loss.backward() 
                        # update weight
                        optimizer.step()
                        tqdm_data_loader.set_postfix(loss=loss.item())
        except Exception as e:
            self.logs.write_exception(e)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '--c', default='config/config.yaml')
    parser.add_argument('--params', '--p', default='config/params.yaml')
    parsed_args = parser.parse_args()
    config = read_config(parsed_args.config)
    params = read_config(parsed_args.params)
    logs = logger(parsed_args.config)
    logs.write_log(f"********{STAGE} STARTED***********")
    try:
        base_model_path = os.path.join(config['Model']['Model_root_dir'], config['Model']['base_model'])
        Training_ob = Training(parsed_args.config, parsed_args.params, base_model_path)
        
        Training_ob.training()
    except Exception as e:
        logs.write_exception(e)
