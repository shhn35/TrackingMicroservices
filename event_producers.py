from abc import ABCMeta,abstractmethod
import view_models as vm
import pickle

class IEventProducer:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        pass

    @abstractmethod
    def _add_event(self,event:vm.EventVM):
        """"
        Hand overs the new add_event request to the EventConsumer 
        """
        ### event_bin = pickle.dumps(events)

        # raise NotImplementedError
        pass
