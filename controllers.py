from exceptions import *
from validations import TMsValidator
import view_models as vm
from db import DataSource
from http import HTTPStatus
from event_producers import IEventProducer
from basics import TMsBasics

class TMsController(TMsBasics):
    def __init__(self) -> None:
        super().__init__()
        self.__data_source = DataSource(self._cfg,self._logger)
        self.__event_producer = IEventProducer()
        self.__validator = TMsValidator()

    def start_session_controller(self,req_body):
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
        new_session = vm.SessionVM()
        new_session.init_start_session(user_id=req_body["userId"],
                                       machine_id=req_body["machineId"],
                                       start_at=req_body["startAt"],
                                       app_id=req_body["appId"])


        validation_res = self.__validator.validate_start_session(new_session)
        if not validation_res.status:
            result["status"] = HTTPStatus.BAD_REQUEST
            result["message"] = validation_res.message
            return result

        ### Insert new session into DB 
        self.__data_source.create_new_session(new_session)

        ### Return the new session_iud
        result["status"] = HTTPStatus.OK
        result["message"] = "New session was successfullt created!"
        result["sessionId"] = new_session.session_id

        return result

    def close_session_controller(self,req_body):
        """
        close the current session by updating the end_at

        param: req_body: A dict-like object wich contains all the request body
        type: dict object (json object)
        """

        if not isinstance(req_body,dict):
            raise TMSValueError(f"The parameter 'req_body' has to be a dict object instead of {type(req_body)}")
        
        result = dict()
        
        ### Fill the viewModel
        session = vm.SessionVM()
        session.init_end_session(session_id=req_body["sessionId"],
                                     end_at=req_body["endAt"])


        ### Some validations that are important to implement:
        ### 1. If the current session is already closed, the update 'end_at' should not execute.
        ### 2. end_at has to be greater than current_session.start_at, unless the update should get aborted.
        validation_res = self.__validator.validate_session(session_id=session.session_id,end_at=session.end_at)
        if not validation_res.status:
            result["status"] = HTTPStatus.BAD_REQUEST
            result["message"] = validation_res.message
            return result

        ### Update session into DB and close it
        self.__data_source.close_session_by_id(session)

        ### Return the new session_iud
        result["status"] = HTTPStatus.OK
        result["message"] = "The session was successfullt closed!"

        return result

    def add_event_controller(self,req_body):
        """
        Add the new event request into the Kafka partition to be processed by the consumer

        param: req_body: A dict-like object wich contains all the request body
        type: dict object (json object)
        """

        if not isinstance(req_body,dict):
            raise TMSValueError(f"The parameter 'req_body' has to be a dict object instead of {type(req_body)}")

        result = dict()
        
        ### Fill the viewModel
        event = vm.EventVM(event_obj=req_body)


        ### Some validation here
        ### 1. Session exists and is open
        ### 2. The number of events dont excced the max_events 
        validation_res = self.__validator.add_event_validations(event)

        if not validation_res.status:
            result["status"] = HTTPStatus.BAD_REQUEST
            result["message"] = validation_res.message
            return result

        ### pass the event to consumer microserivce (e.g., kafka partition, queue, ...) to store them in DB 
        self.__event_producer._add_event(event)

        result["status"] = HTTPStatus.OK
        result["message"] = "The event is eventually recorded."

        return result