import os
import configparser

class ConfigReader():
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(self._config.read(os.path.join(os.path.dirname(__file__),'config.ini')),encoding='utf8')
    
    ### LOGS
    def get_logger_name(self):
        return self._config['LOGS']['logger_name']
    
    def get_logger_level(self):
        return self._config['LOGS']['logger_level']
    
    def get_logfile_path (self):
        return self._config['LOGS']['log_file']
    
        
    ### DB Part
    def get_DB_info(self):
        return  \
            os.environ[self._config['DB']['env_db_host']], \
                os.environ[self._config['DB']['env_db_dbname']], \
                    os.environ[self._config['DB']['env_db_usr']], \
                        os.environ[self._config['DB']['env_db_passwrd']]
    
    
    ### TMS_API
    def get_api_debug_mode(self):
        return bool(int(self._config['TMS_API']['debug_mode']))


    ### General Part
    def get_error_msg (self):
        return self._config['GENERAL']['error_msg'] 

    ### VALIDATION Part
    def get_max_event_count(self):
        return int(self._config['VALIDATIONS']['max_event_count'])
