from exceptions import *
import data_model as dm
from db import DataSource
from http import HTTPStatus

class TMsController(object):
    def __init__(self,cfg,logger) -> None:
        super().__init__()
        self.__logger = logger
        self.__cfg = cfg
        self.__data_source = DataSource(self.__logger)


    def start_session(self,req_body):
        """
        Creates a new session and returns a session_id

        param: req_body: A dict-like object wich contains all the request body
        type: dict object (json object)

        return: New SessionId is returned
        type: a dict object
        """

        if not isinstance(req_body,dict):
            raise TMSValueError(f"The parameter 'req_body' has to be a dict object instead of {type(req_body)}")
        
        result = dict()
        
        ### Fill the dataModel
        new_session = dm.SessionDM()
        new_session.init_start_session(user_id=req_body["userId"],
                                       machine_id=req_body["machineId"],
                                       start_at=req_body["startAt"],
                                       app_id=req_body["appId"])

        ### Insert new session into DB 
        self.__data_source.create_new_session(new_session)

        ### Return the new session_iud
        result["status"] = HTTPStatus.OK
        result["message"] = "New session was successfullt created!"
        result["sessionId"] = new_session.session_id

        return result

    def close_session(self,req_body):
        """
        close the current session by updating the end_at

        param: req_body: A dict-like object wich contains all the request body
        type: dict object (json object)
        """

        if not isinstance(req_body,dict):
            raise TMSValueError(f"The parameter 'req_body' has to be a dict object instead of {type(req_body)}")
        
        result = dict()
        
        ### Fill the dataModel
        new_session = dm.SessionDM()
        new_session.init_end_session(session_id=req_body["sessionId"],
                                     end_at=req_body["endAt"])

        ### Update session into DB and close it
        self.__data_source.close_session_by_id(new_session)

        ### Return the new session_iud
        result["status"] = HTTPStatus.OK
        result["message"] = "The session was successfullt closed!"

        return result
