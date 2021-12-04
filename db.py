import psycopg2 as psql
from abc import ABCMeta,abstractmethod
from .config_reader import ConfigReader
from exceptions import PsqlDataSourceException


class IDataSource:
    __metaclass__ = ABCMeta
    
    def __init__(self,logger):
        self.__config = ConfigReader()
        self.__logger =  logger
    
    
    @abstractmethod    
    def _conn_init(self,**kwargs):
        '''
        Initial the connection to the target data source, e.g., Psql, MS-Sql, AWS , and etc
        '''
        raise NotImplementedError
    
    @abstractmethod
    def _exec_select(self,query):
        '''
        Execute a SQL query on the _ds_conn and return the result in LIST format
        '''
        raise NotImplementedError
          
    @abstractmethod
    def _load_to_database(self, obj):
        '''
        Load data as table object into data source
        '''
    
    
class PsqlDataScource(IDataSource):
    _ds_engine = None
    _ds_conn = None
    def __init__(self):
        super().__init__()
        
        __host, __dbname, __user, __password = self.__config.get_DB_info()
        self.__conn_string = "postgresql://{}:{}@{}/{}".format(__user, __password, __host, __dbname)
        
        self.__crs, self.__geom_col_name = self.__config.get_gdp_query_conf()
        
        kwargs = {'hname':__host, 'dbname': __dbname, 'uname': __user, 'pas': __password}
        self._conn_init(**kwargs)
    
    ############### Overwriten methods and properties ###############
    def _conn_init(self,**kwargs):
        hname = kwargs['hname']
        pas = kwargs['pas']
        uname = kwargs['uname']
        dbname = kwargs['dbname']
        
        self._ds_conn = psql.connect(host = hname,
                                        user = uname,
                                        password = pas,
                                        database = dbname)

    def _exec_select(self,query):
        cursor = self._ds_conn.cursor() 
        try:  
            cursor.execute(query)
            return cursor.fetchall() 
        
        except:   
            raise PsqlDataSourceException("Something went wrong in executing query on data source.")
        finally:
            cursor.close()
  
    def _load_to_database(self, obj):
        s = self.__create_session()
        try:
            s.add(obj)
            s.commit()
        except :
            s.rollback()
            raise PsqlDataSourceException("Something went wrong in loading data as object into data base")
        finally:
            s.close()
    

class SourceDS(PsqlDataScource):
    def __init__(self):
        super().__init__()
        