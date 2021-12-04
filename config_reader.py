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
    
    def get_etl_logfile_path (self):
        return self._config['LOGS']['log_file']
    
        
    ### DB Part
    def get_DB_info(self):
        return  \
            os.environ[self._config['DB']['env_db_host']], \
                os.environ[self._config['DB']['env_db_dbname']], \
                    os.environ[self._config['DB']['env_db_usr']], \
                        os.environ[self._config['DB']['env_db_passwrd']]
    
    
    ### General Part