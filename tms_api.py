from flask import request,jsonify,Flask,current_app
from controllers import TMsController
from exceptions import *
from http import HTTPStatus
from basics import TMsBasics

class TMS_API(TMsBasics):
    tms_api = Flask(__name__)
    def __init__(self) :
        super().__init__()

        self.tms_api.__cfg = self._cfg
        self.tms_api.__logger = self._logger
        
        self.tms_api.__tms_controller = TMsController()

        ### Flast initialization        
        self.tms_api.config["DEBUG"] = self.tms_api.__cfg.get_api_debug_mode()

        self.tms_api.run()

    
    @tms_api.route('/',methods=['GET'])
    def home():
        """
        The root page of the API,
        Just for the sacke of the demo!
        """
        return "<h1>Welcome to Tracking Microservices Demo </h1> \
                <h3>John Deere ISG_K Digital Application</h3 \
                <div>Written by <b>Seyedhadi Hosseininejad</b></div>"

    
    @tms_api.route('/StartSession',methods=['POST'])
    def start_session():
        result = dict()
        try:
            req_body = request.json
            
            result = current_app.__tms_controller.start_session_controller(req_body=req_body)
            
            return jsonify(result)

        except Exception as ex:            
            if isinstance(ex,TMSException):
                ### Other specific actions regarding the exception
                ###
                ###
                pass

            current_app.__logger.exception("Error in starting new session!")
            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = current_app.__cfg.get_error_msg()
            return jsonify(result)

    @tms_api.route('/EndSession',methods=['POST'])
    def end_session():
        result = dict()
        try:
            req_body = request.json
            
            result = current_app.__tms_controller.close_session_controller(req_body=req_body)
            
            return jsonify(result)

        except Exception as ex:            
            if isinstance(ex,TMSException):
                ### Other specific actions regarding the exception
                ###
                ###
                pass

            current_app.__logger.exception("Error in closing session!")
            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = current_app.__cfg.get_error_msg()
            return jsonify(result)

    @tms_api.route('/AddEvent',methods=['POST'])
    def add_event():
        result = dict()
        try:
            req_body = request.json
            
            result = current_app.__tms_controller.add_event_controller(req_body=req_body)
            
            return jsonify(result)

        except Exception as ex:            
            if isinstance(ex,TMSException):
                ### Other specific actions regarding the exception
                ###
                ###
                pass

            current_app.__logger.exception("Error in adding new event!")
            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = current_app.__cfg.get_error_msg()
            return jsonify(result)

if __name__ == "__main__":
    app = TMS_API()