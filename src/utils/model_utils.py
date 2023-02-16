import pandas as pd
import os
import torch
import torch.nn as nn
from src.utils.common import read_config
from src.Logger.logger import logger



def get_model_params(model):
    try:

        parameters = {"Trainable_Param_name": list(), "Tradable_Param": list()}
        total = {'total_pram_count': 0, "Non_Tradable_count":0, "Trainable_count":0}
        for name, params in model.named_parameters():
            if params.requires_grad:
                parameters["Trainable_Param_name"].append(name)
                parameters["Tradable_Param"].append(params.numel())
                total['total_pram_count'] += params.numel()
                total['Trainable_count'] += params.numel()
            else:
                total['total_pram_count'] += params.numel()
                total['Non_Tradable_count'] += params.numel()
        
        df = pd.DataFrame(parameters)
        df = df.style.set_caption(f"Total parameters: {total}")
        return df
    except Exception as e:
        print(e)
    
    

def optimizer(model, config_path="config/params.yaml"):
    params =  read_config(config_path)
    optims = params['optimizer']
    lr = params['learning_rate']
    optimizer = torch.optim.optims(model.parameters(), lr=lr)
    return optimizer

def loss(config_path="config/params.yaml"):
    params = read_config(config_path)
    loss_fn = params['loss_funtion']
    criterion = nn.loss_fn
    return criterion

def save_model(model, path_to_model, type='Base'):
    try:
        torch.save(model, path_to_model)
    except Exception as e:
        print(e)

def load_model(model_full_path):
    load_model = torch.load(model_full_path)
    return load_model



    