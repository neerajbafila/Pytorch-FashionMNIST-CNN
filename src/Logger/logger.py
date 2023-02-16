import os
import logging
import sys
from src.utils.common import read_config, create_directories, unique_name

class logger:
    def __init__(self, config_file = "config/config.yaml") -> None:
        self.config_data = read_config(config_file)
        self.log_filename = self.config_data['Logger']['log_file_name']
        self.log_location =  self.config_data['Logger']['log_location']
        create_directories([self.log_location])
        self.unique_log_file_name = unique_name()
        self.log_filename = f"{self.log_filename}_{self.unique_log_file_name}.txt"
        self.log_file_path = os.path.join(self.log_location, self.log_filename)
        
    
    def write_log(self, msg, log_level='INFO'):
        # get logger
        self.log_level = log_level
        # print(self.log_level)

        self.mylogger = logging.getLogger(__name__)        
        # set handler
        self.fileHandler = logging.FileHandler(self.log_file_path)
        # set log level
        # self.level = logging.log_level
        self.mylogger.setLevel(self.log_level.upper())

        # define formatter
        # formats = logging.Formatter('[%(asctime)s-%(levelname)s-%(module)s-%(name)s]-%(message)s')
        formats = logging.Formatter('[%(asctime)s-%(levelname)s-%(module)s]-%(message)s')
        # add formatter to file handller
        self.fileHandler.setFormatter(formats)
        # add filehandler to mylogger
        self.mylogger.addHandler(self.fileHandler)

        if self.log_level.upper()=='INFO':
            self.mylogger.info(msg)
        elif self.log_level.upper()=='WARNING':
            self.mylogger.warning(msg)
        elif self.log_level.upper()=='DEBUG':
            self.mylogger.debug(msg)
        # elif self.log_level.upper()=='ERROR':
        #     self.mylogger.error(msg)
        else:
            self.mylogger.info(msg)
        
        # remove exiting handler when job finished as if you call method seconde time it will write it no of time it was previously called or duplicate msg
        self.mylogger.removeHandler(self.fileHandler)
        # # self.log_location
        # print(self.log_filename)
    def write_exception(self, e, log_level='ERROR'):

        self.log_level = log_level
        
        self.mylogger = logging.getLogger(__name__)        
        # set handler
        self.fileHandler = logging.FileHandler(self.log_file_path)
        # set log level
        # self.level = logging.log_level
        self.mylogger.setLevel(self.log_level.upper())

        # define formatter
        # formats = logging.Formatter('[%(asctime)s-%(levelname)s-%(module)s-%(name)s]-%(message)s')
        formats = logging.Formatter('[%(asctime)s-%(levelname)s-%(module)s]-%(message)s')
        # add formatter to file handller
        self.fileHandler.setFormatter(formats)
        # add filehandler to mylogger
        self.mylogger.addHandler(self.fileHandler)

        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        msg = (f"Exception occurred {e} \ndetails are below:\nexc_type {exc_type}, exc_obj {exc_obj}, line_no {line_no}, file_name {file_name}")
        self.mylogger.error(msg)
        self.mylogger.removeHandler(self.fileHandler)



            