from basics import TMsBasics
import view_models as vm
from exceptions import *
from db import DataSource

class TMsValidator(TMsBasics):
    def __init__(self):
        super().__init__()        
        self.__data_source = DataSource(self._cfg,self._logger)

    def add_event_validations(self,event:vm.EventVM):
        """
        Add the validation regarding add_event 

        param event: The event object
        type:   vm.EventVM

        return: The result of validation
        type:   vm.ValidationResultVM
        """
        if not isinstance(event,vm.EventVM):
            raise TMSValueError(f"The parameter 'event' has to be a EventVM object instead of {type(event)}")
        
        ### 1. Session exists and is open
        result = self.validate_session(session_id = event.session_id)
        if not result.status:
            return result

        ### 2. The number of events dont excced the max_events 
        result = self.__check_event_max_size(event)
        if not result.status:
            return result

        return result

    def validate_session(self,session_id,end_at=None):
        """
        Checks whether session exists and also it is open or not

        In case end_at provided, also checks whether end_at>start_at
        """
        session = self.__data_source.get_session_by_id(session_id=session_id)

        if not session and len(session) != 1:
            return vm.ValidationResultVM(status=False,message=f"No session or more than one session exists for session_id '{session_id}'")
        
        if session[0][5] is not None:
            return vm.ValidationResultVM(status=False,message=f"Session already closed for session_id '{session_id}'")

        if end_at is not None:
            if session[0][3]>end_at:
                return vm.ValidationResultVM(status=False,message=f"End_at cannot be greater than session.start_at for session_id '{session_id}'")

        return vm.ValidationResultVM(status=True)

    def validate_start_session(self,session:vm.SessionVM):
        """
        Add the validation regarding start_session 

        param session: The session object
        type:   vm.SessionVM

        return: The result of validation
        type:   vm.ValidationResultVM
        """

        if not isinstance(session,vm.SessionVM):
            raise TMSValueError(f"The parameter 'session' has to be a SessionVM object instead of {type(session)}")
        
        ### 1. machine_id is valid
        if session.machine_id and len(session.machine_id) > 0:
            result = self.__machine_is_exist(machine_id = session.machine_id)
            if not result.status:
                return result

        ### 2. user_id is valid 
        if session.user_id and len(session.user_id) > 0:
            result = self.__user_is_exist(session.user_id)
            if not result.status:
                return result

        return result

    ### Private methods
    def __machine_is_exist(self,machine_id):
        """
        Checks whether session exists and also it is open or not
        """
        machine = self.__data_source.get_machine_by_id(machine_id=machine_id)

        if not machine and len(machine) != 1:
            return vm.ValidationResultVM(status=False,message=f"Invalid machine Id!")
        
        return vm.ValidationResultVM(status=True)

    def __user_is_exist(self,user_id):
        """
        Checks whether user exists and also it is open or not
        """
        user = self.__data_source.get_user_by_id(user_id=user_id)

        if not user and len(user) != 1:
            return vm.ValidationResultVM(status=False,message=f"Invalid user Id!")
        
        return vm.ValidationResultVM(status=True)

    def __check_event_max_size(self,event:vm.EventVM):
        """
        Checks whether the number of events dont exceed the max allowance
        """

        if len(event.events) > self._cfg.get_max_event_count():
            return vm.ValidationResultVM(status=False,message=f"The number of events exceeded the '{self._cfg.get_max_event_count()}'")

        return vm.ValidationResultVM(status=True)

