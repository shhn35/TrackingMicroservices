from log import Logger
from config_reader import ConfigReader
import unique_id_generators as uidg

class TMsBasics(object):
    def __init__(self) :
        super().__init__()
        self._cfg = ConfigReader()
        self._logger = Logger(self._cfg).get_logger()
        self._uuid_gen = uidg.UUID()


