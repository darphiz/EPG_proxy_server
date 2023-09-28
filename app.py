import requests

import configparser
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

# sanity checks
app_config = configparser.ConfigParser()
app_config.read('config.ini')
if 'reroute' not in app_config.sections():
    raise ImproperlyConfiguredApp("No reroute section in config.ini")



app = Flask(__name__)


@app.route("/")
def proxy_entry():
    query_params = request.args
    provider = ""
    try:
        with suppress(Exception):
            provider = list(query_params.keys())[0]
        if not provider:
            raise NoProvider()

        # map providers with config file
        config = configparser.ConfigParser(
            strict=False, 
            interpolation=None
        )
        config.read('config.ini')

        reroute_sections = config["reroute"]
        if provider.lower() not in reroute_sections:
            raise ProviderNotFound(provider)
        source_url = reroute_sections[provider.lower()]

        # sanity check
        if not AppUtils.is_valid_url(source_url):
            raise InvalidDestination(source_url)

        # make request to download xml file from source_url
        req = requests.get(source_url)
        if req.status_code != 200:
          raise CannotDownloadXML(source_url)

        # # save xml file to memory
        xml_content = req.content
        xml_resp = AppUtils.process_xml(xml_content)
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