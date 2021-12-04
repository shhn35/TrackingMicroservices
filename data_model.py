import datetime as dt
from utilities import UUID

class SessionDM(object):
    """
    Data Model for SessionStart endpoint input
    """
    def __init__(self):
        super().__init__()
        self.session_id = UUID()._get_next_id()

    def init_start_session(self,user_id,machine_id,start_at,app_id):
        """
        Initializes the object based on the start_session endpoint
        """
        self.session_id = UUID()._get_next_id()
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
            raise ValueError("The value for the 'start_at' attribute is not a valid datetime!")

    
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
            raise ValueError("The value for the 'end_at' attribute is not a valid datetime!")

    
    ### AppID
    @property
    def app_id(self):
        return self.__app_id
    
    @app_id.setter
    def app_id(self,value):
        ### implement validation here ...
        self.__app_id = int(value)

        
        ### Note: OrgId is ignored given it is handled in DB


