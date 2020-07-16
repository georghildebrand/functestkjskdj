import logging
from logging import INFO
import os
import sys
import azure.functions as func


# Note:
# As ServiceBus has currently only simple message (str) input bindings 
# in its extensions we are using the sdk to write to ServiceBus
# https://azure.github.io/azure-sdk-for-python/ref/Service-Bus.html
# ToDo: add open API for advanced api :
# https://docs.microsoft.com/de-de/azure/azure-functions/functions-api-definition 
# ToDo: Propper error handling



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    INFOS = " PATH:"
    INFOS += ",".join(sys.path)
    ERRORS = ""

    try:
        from azure.servicebus import QueueClient, Message
    except ImportError as ie:
        ERRORS += str(ie)
    try:
        import numpy as np
    except ImportError as ie:
        ERRORS += str(ie)

    # todo: caution! will also return sensible information only use for testing!

    try:
        from pip._internal.operations import freeze
    except ImportError as ie:  # pip < 10.0
        from pip.operations import freeze
        ERRORS += str(ie)

    INFOS += " PIP FREEZE:"
    INFOS += str([i for i in freeze.freeze()])
    INFOS += " ENV VARS: "
    INFOS += str({(k,v) for k,v in os.environ.items()})
    

    return func.HttpResponse(f"ERRORS: {ERRORS}; INFOS: {INFOS}")
