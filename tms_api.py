from flask import request,jsonify,Flask,current_app
from controllers import TMsController
from log import Logger
from config_reader import ConfigReader
from exceptions import *

class TMS_API(object):
    hadi = dict()
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
        try:
            req_body = request.json
            
            new_session_id = current_app.__tms_controller.start_session(req_body=req_body)
            
            return jsonify(new_session_id)

        except TMSException:
            current_app.__logger.exception("Error in starting new session!")
            ### Other actions regarding the exception, given it is raised by our code


            return "<h1>Something wrong happeng withing your request.</h1>"
        except Exception:
            current_app.__logger.exception("Unexpected Error in starting new session!")
            return "<h1>Something wrong happeng withing your request.</h1>"




if __name__ == "__main__":
    app = TMS_API()