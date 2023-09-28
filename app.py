import os
import requests
from logging.config import dictConfig
import configparser
from datetime import datetime
from contextlib import suppress
from exceptions import (
    CannotDownloadXML,
    ImproperlyConfiguredApp,
    InvalidDestination, 
    ProviderNotFound, 
    NoProvider
)
from flask import Flask, request, render_template
from requests.exceptions import ConnectionError
from utils import AppUtils
from dotenv import load_dotenv
load_dotenv()

# sanity checks
app_config = configparser.ConfigParser()
app_config.read('config.ini')
if 'reroute' not in app_config.sections():
    raise ImproperlyConfiguredApp("No reroute section in config.ini")


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s]: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
    
        'filehandler': {
            'class': 'logging.FileHandler',
            'filename': os.getenv(
                "LOG_FILE_LOCATION", 
                "/var/log/app/app.log"
            ),
            'formatter': 'default'
        },

    },
    
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'filehandler']
    }
})



app = Flask(__name__)


@app.route("/")
def proxy_entry():
    query_params = request.args
    provider = ""

    try:
        with suppress(Exception):
            provider = list(query_params.keys())[0]
        if not provider:
            # log error
            app.logger.error("No provider found in query params")
            raise NoProvider()



        # map providers with config file
        config = configparser.ConfigParser(
            strict=False, 
            interpolation=None
        )
        config.read('config.ini')

        reroute_sections = config["reroute"]
        if provider.lower() not in reroute_sections:
            app.logger.error(f"Provider {provider} not found in config.ini")
            raise ProviderNotFound(provider)
        
        # when a provider and source is mapped, then we can say message is recieved
        received_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        app.logger.info(f"PROVIDER={provider}, MSG_RCD_REQ={received_at}")
        
        
        source_url = reroute_sections[provider.lower()]

        # sanity check
        if not AppUtils.is_valid_url(source_url):
            app.logger.error(f"Invalid destination url {source_url}")
            raise InvalidDestination(source_url)

        # make request to download xml file from source_url
        message_sent_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        app.logger.info(f"PROVIDER={provider}, MSG_SENT_PROV={message_sent_at}")
        req = requests.get(source_url)
        if req.status_code != 200:
            app.logger.error(f"Cannot download xml from {source_url}")
            raise CannotDownloadXML(source_url)
        message_received_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        elapsed_time = (
            datetime.strptime(message_received_at, "%d-%m-%Y %H:%M:%S")
            - datetime.strptime(message_sent_at, "%d-%m-%Y %H:%M:%S")
        ).total_seconds()
        elapsed_milliseconds = elapsed_time * 1000
        app.logger.info(f"PROVIDER={provider}, MSG_RCD_PROV={message_sent_at}, ELAPSED_TIME={elapsed_milliseconds}")

        # # save xml file to memory
        xml_content = req.content
        resp = AppUtils.process_xml(xml_content)
        xml_resp = resp['xml']
        
        # log info
        programs_count = resp['programs_count']
        channels_count = resp['channels_count']
        resp_sent_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        app.logger.info(f"PROVIDER={provider}, ChannelCount={channels_count}, ProgrammeCount={programs_count}")
        app.logger.info(f"PROVIDER={provider}, MSG_SENT_RESP={resp_sent_at}")
        
        #if log level is set to debug, then log xml response
        if app.logger.level == 10:
            time_stamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            with open(f"{time_stamp}_{provider}_EPG_Guide.xml", "wb") as f:
                f.write(xml_content)

            with open(f"{time_stamp}_generated_EPG_Guide.xml", "wb") as f:
                f.write(xml_resp)
        
        return xml_resp, 200, {"Content-Type": "application/xml"}

    except ConnectionError as e:
        return render_template(
            "error_page.html", 
            error_message= f"Cannot connect to {source_url}",
            providers=app_config["reroute"].keys(),
            ), 400
    except Exception as e:
        return render_template(
        "error_page.html", 
        error_message= str(e),
        providers=app_config["reroute"].keys(),
        ), 400
    

if __name__ == "__main__":
    app.run(debug=True)