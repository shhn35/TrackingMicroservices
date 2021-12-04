import psycopg2 as psql
from abc import ABCMeta,abstractmethod
from config_reader import ConfigReader
from exceptions import *
from data_model import *

class IDataSource:
    __metaclass__ = ABCMeta
    
    def __init__(self,logger):
        self._config = ConfigReader()
        self._logger =  logger
    
    
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
    def _exec_non_reader(self, sql_query,arg_tuple=None):
        '''
        Load data as table object into data source
        '''
    
    
class PsqlDataScource(IDataSource):
    _ds_engine = None
    _ds_conn = None
    def __init__(self,logger):
        super().__init__(logger)
        
        __host, __dbname, __user, __password = self._config.get_DB_info()
        
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
  
    def _exec_non_reader(self,sql_query, args_tuple=None):
        cursor = self._ds_conn.cursor()
        try:
            cursor.execute(sql_query, args_tuple)
            self._ds_conn.commit()
        except:
            self._ds_conn.rollback()
            raise PsqlDataSourceException("Something went wrong in executing query on data source.")
        finally:
            cursor.close()
    

class DataSource(PsqlDataScource):
    def __init__(self,logger):
        super().__init__(logger)
    
    def create_new_session(self,new_session: SessionDM):
        """
        Insert a new record into StartSession table.
        NOTE: This functionality can be implemented in different ways, but here, I sicked to the simplest one.

        param:  new_session: An object which holds all the fields for the new session
        type: AN object of type StartSessionDM

        result: The new generated SessionId
        type:   str object
        """

        if not isinstance(new_session,SessionDM):
            raise TMSValueError(f"Invalid object for 'new_session' parameter. It has to be a 'StartSessionDM' object instead of '{type(new_session)}'")

        query = "INSERT INTO public.sessions( \
	            session_id, user_id, machine_id, start_at, application_id) \
	            VALUES ('{session_id}', '{user_id}', '{machine_id}', '{start_at}', {app_id});".format(
                    session_id = new_session.session_id,
                    user_id = new_session.user_id,
                    machine_id = new_session.machine_id,
                    start_at = new_session.start_at,
                    app_id = new_session.app_id 
                )

        self._exec_non_reader(query)

    def close_session_by_id(self,current_session: SessionDM):
        """
        Close the session by updating the EndAt field.
        NOTE: This functionality can be implemented in different ways, but here, I sicked to the simplest one.

        param:  current_session: An object which holds all the fields for the new session
        type: AN object of type StartSessionDM
        """

        if not isinstance(current_session,SessionDM):
            raise TMSValueError(f"Invalid object for 'new_session' parameter. It has to be a 'StartSessionDM' object instead of '{type(new_session)}'")

        ### Some validations that are important to implement:

        ### 1. If the current session is already closed, the update 'end_at' should not execute.
        ### 2. end_at has to be greater than current_session.start_at, unless the update should get aborted.

        query = "UPDATE public.sessions \
	            SET end_at='{end_at}' \
                WHERE session_id= '{session_id}'".format(
                    session_id = current_session.session_id,
                    end_at = current_session.end_at
                )

        self._exec_non_reader(query)

