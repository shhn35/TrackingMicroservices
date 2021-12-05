from abc import ABCMeta,abstractmethod
import view_models as vm
import pickle

class IEventConsumer:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        pass

    @abstractmethod
    def _process_event(self,event):
        """"
        Hand overs the new add_event request to the EventConsumer 
        """
        ### event_obj = pickle.reads(events)

        # raise NotImplementedError
        pass
