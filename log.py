import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

class Logger(object):
    def __init__(self,config) :
        super().__init__()
        
        self.__logger_name = config.get_logger_name()
        __logger_level = config.get_logger_level()
        
        _log_format = logging.Formatter('%(levelname)s:\t%(asctime)s:\t%(message)s')
        
        _log_level = logging.DEBUG
        if __logger_level.lower() == 'info':
            _log_level = logging.INFO
        elif __logger_level.lower() == 'warning':
            _log_level = logging.WARN
        elif __logger_level.lower() == 'error':
            _log_level = logging.ERROR
        elif __logger_level.lower() == 'critical':
            _log_level = logging.CRITICAL
            
        
        _log_filename = config.get_logfile_path()
        
        Path(os.path.join(_log_filename[0:_log_filename.rfind('\\')])).mkdir(parents=True,exist_ok=True)
        
        _f_handler = RotatingFileHandler(_log_filename,maxBytes=100*1024*1024,backupCount=10)
        _f_handler.setFormatter(_log_format)        
        _f_handler.setLevel(_log_level)
        
        _s_handler = logging.StreamHandler()
        _s_handler.setFormatter(_log_format)        
        _s_handler.setLevel(_log_level)
        
        self.__logger = logging.getLogger(self.__logger_name)
        self.__logger.setLevel(_log_level)
        
        self.__logger.addHandler(_f_handler)
        self.__logger.addHandler(_s_handler)

    def get_logger(self):
        """
        Returns the logger object
        """
        return self.__logger

