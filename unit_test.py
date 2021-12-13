import unittest
from controllers import TMsController
import view_models as vm
import datetime as dt
import json
from http import HTTPStatus
from config_reader import ConfigReader

class TestEndSession(unittest.TestCase):
    _controller = TMsController()   
    def test_no_session(self):
        req = {
            "sessionId": "no_session_test",
            "endAt": str(dt.datetime.now())
            }

        result = self._controller.close_session_controller(req)

        self.assertEqual(result['status'], HTTPStatus.BAD_REQUEST)

    def test_already_closed_session(self):
        req = {
            "sessionId": "2540e370-e5bb-4d24-9b4e-0740d181ffae",
            "endAt": str(dt.datetime.now())
            }

        result = self._controller.close_session_controller(req)

        self.assertEqual(result['status'], HTTPStatus.BAD_REQUEST)

    def test_closing_before_session_start(self):
        req = {"sessionId": "2540e370-e5bb-4d24-9b4e-0740d181ffae","endAt": str(dt.datetime.fromisoformat("1970-01-01 00:00:00"))}

        result = self._controller.close_session_controller(req)

        self.assertEqual(result['status'], HTTPStatus.BAD_REQUEST)


class TestAddEvent(unittest.TestCase):
    _controller = TMsController()
    _cfg = ConfigReader()
    def test_session_not_exist(self):
        req = {"sessionId": "NO-session-id",\
                "events":[
                {
                    "eventAt": "2021-12-06 05:14:55",
                    "eventType": "sensor1",
                    "payload": "Payload 1"
                }]
        }

        result = self._controller.add_event_controller(req)

        self.assertEqual(result['status'], HTTPStatus.BAD_REQUEST)

    def test_session_is_open(self):
        
        req = {"sessionId": "2540e370-e5bb-4d24-9b4e-0740d181ffae",\
                "events":[
                {
                    "eventAt": "2021-12-06 05:14:55",
                    "eventType": "sensor1",
                    "payload": "Payload 1"
                }]
        }

        result = self._controller.add_event_controller(req)

        self.assertEqual(result['status'], HTTPStatus.BAD_REQUEST)

    def test_max_event(self):
        events = []
        for i in range(self._cfg.get_max_event_count()+1):
            events.append({
                    "eventAt": "2021-12-06 05:14:55",
                    "eventType": "sensor1",
                    "payload": "Payload 1"
                })

        req = {"sessionId": "Always-Open-session",\
                "events":events
        }

        result = self._controller.add_event_controller(req)

        self.assertEqual(result['status'], HTTPStatus.BAD_REQUEST)

if __name__ == '__main__':
    unittest.main()