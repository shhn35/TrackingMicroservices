import uuid
from abc import ABCMeta,abstractmethod

class IUniqueIDGenerator(object):
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def _get_next_id(self):
        """
        Generates and returns the next unique ID
        """
        raise NotImplementedError()        


class UUID(IUniqueIDGenerator):
    def __init__(self):
        super().__init__()

    def _get_next_id(self):
        return str(uuid.uuid4())