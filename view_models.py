import datetime as dt
from exceptions import TMSValueError
from basics import TMsBasics

class SessionVM(TMsBasics):
    """
    View Model for SessionStart endpoint input
    """
    def __init__(self):
        super().__init__()

    def init_start_session(self,user_id,machine_id,start_at,app_id):
        """
        Initializes the object based on the start_session endpoint
        """
        self.session_id = self._uuid_gen._get_next_id()
        self.user_id = user_id
        self.machine_id = machine_id
        self.start_at = start_at
        self.app_id = app_id

    def init_end_session(self,session_id,end_at):
        """
        Initializes the object based on the end_session endpoint
        """
        self.session_id = session_id
        self.end_at = end_at


    ### SessionId
    @property
    def session_id(self):
        return self.__session_id
    @session_id.setter
    def session_id(self,value):
        ### implement validation here ...
        self.__session_id = value


    ### UserId
    @property
    def user_id(self):
        return self.__user_id
    @user_id.setter
    def user_id(self,value):
        ### implement validation here ...
        self.__user_id = value

    
    ### MachineID
    @property
    def machine_id(self):
        return self.__machine_id
    @machine_id.setter
    def machine_id(self,value):
        ### implement validation here ...
        self.__machine_id = value

    
    ### StartAt
    @property
    def start_at(self):
        return self.__start_at
    @start_at.setter
    def start_at(self,value):
        ### implement validation here ...
        try:
            self.__start_at = dt.datetime.fromisoformat(value)
        except:
            raise TMSValueError("The value for the 'start_at' attribute is not a valid datetime!")

    
    ### EndAt
    @property
    def end_at(self):
        return self.__end_at
    @end_at.setter
    def end_at(self,value):
        ### implement validation here ...
        try:
            self.__end_at = dt.datetime.fromisoformat(value)
        except:
            raise TMSValueError("The value for the 'end_at' attribute is not a valid datetime!")

    
    ### AppID
    @property
    def app_id(self):
        return self.__app_id
    @app_id.setter
    def app_id(self,value):
        ### implement validation here ...
        self.__app_id = int(value)

        
    ### Note: OrgId is ignored given it is handled in DB


class EventDetailVM(object):
    """
    View Model for Event details input
    """
    def __init__(self,event_at,event_type,payload) :
        super().__init__()
        self.event_at = event_at
        self.event_type = event_type
        self.payload = payload
    
    ### eventAt
    @property
    def event_at(self):
        return self.__event_at
    @event_at.setter
    def event_at(self,value):
        try:
            self.__event_at = dt.datetime.fromisoformat(value)
        except:
            raise TMSValueError("The value for the 'event_at' attribute is not a valid datetime!")

    ### eventType
    @property
    def event_type(self):
        return self.__event_type
    @event_type.setter
    def event_type(self,value):
        ### Validation here
        self.__event_type = str(value)
    
    ### payload
    @property
    def payload(self):
        return self.__payload
    @payload.setter
    def payload(self,value):
        ### Validation here
        self.__payload = str(value)
    
class EventVM(object):
    """
    View Model for Events endpoint input
    """
    def __init__(self,event_obj):
        super().__init__()

        if not isinstance(event_obj,dict):
            raise TMSValueError(f"The parameter 'events' has to be a dict object instead of {type(event_obj)}")

        self.__event_decoder(json_obj=event_obj)

    def __event_decoder(self,json_obj):
        self.session_id = json_obj["sessionId"]
        events = []
        for e in json_obj["events"]:
            ###
            ### a Try,Except block can be applied here, in case we dont want to stop the process when the data of a single event is not correct.
            ###
            events.append(
                EventDetailVM(
                    event_at=e["eventAt"],
                    event_type=e["eventType"],
                    payload=e["payload"])
                )
        self.events = events

    ### SessionId
    @property
    def session_id(self):
        return self.__session_id
    @session_id.setter
    def session_id(self,value):
        ### implement validation here ...
        self.__session_id = value

    ### SessionId
    @property
    def events(self):
        return self.__events
    @events.setter
    def events(self,value):
        ### implement validation here ...
        if not isinstance(value,list):
            raise TMSValueError("The value for the 'events' attribute of an event object is not a valid list!")
        self.__events = value


class ValidationResultVM(object):
    """
    The view model for validation result
    """
    def __init__(self,status,src=None,message=None):
        super().__init__()
        self.src = src
        self.status = status
        self.message = message

    @property
    def src(self):
        return self.__src
    @src.setter
    def src(self,value):
        ### implement validation here ...
        self.__src = value

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self,value):
        ### implement validation here ...
        self.__status = value

    @property
    def message(self):
        return self.__message
    @message.setter
    def message(self,value):
        ### implement validation here ...
        self.__message= value
    


