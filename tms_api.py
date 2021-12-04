from flask import request,jsonify,Flask,current_app
from controllers import TMsController
from log import Logger
from config_reader import ConfigReader
from exceptions import *
from http import HTTPStatus

class TMS_API(object):
    tms_api = Flask(__name__)
    def __init__(self) :
        self.tms_api.__cfg = ConfigReader()
        self.tms_api.__logger = Logger(self.tms_api.__cfg).get_logger()
        
        self.tms_api.__tms_controller = TMsController(cfg=self.tms_api.__cfg,logger=self.tms_api.__logger)

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
            
            result = current_app.__tms_controller.start_session(req_body=req_body)
            
            return jsonify(result)

        except TMSException:
            current_app.__logger.exception("Error in starting new session!")
            
            ### Other actions regarding the exception, given it is raised by our code
            ###
            ###

            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = "Something went wrong withing your request."
            return jsonify(result)
        except Exception:            
            current_app.__logger.exception("Error in starting new session!")
            
            ### Other actions regarding the exception, given it is raised by our code
            ###
            ###

            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = "Something went wrong withing your request."
            return jsonify(result)

    @tms_api.route('/EndSession',methods=['POST'])
    def end_session():
        result = dict()
        try:
            req_body = request.json
            
            result = current_app.__tms_controller.close_session(req_body=req_body)
            
            return jsonify(result)

        except TMSException:
            current_app.__logger.exception("Error in starting new session!")
            
            ### Other actions regarding the exception, given it is raised by our code
            ###
            ###

            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = "Something went wrong withing your request."
            return jsonify(result)
        except Exception:            
            current_app.__logger.exception("Error in starting new session!")

            ### Other actions regarding the exception, given it is raised by our code
            ###
            ###

            result["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["message"] = "Something went wrong withing your request."
            return jsonify(result)



if __name__ == "__main__":
    app = TMS_API()