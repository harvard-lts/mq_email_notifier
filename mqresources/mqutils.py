import json
import logging
import os
import time, traceback
from datetime import datetime, timedelta

import stomp

DATEFORMAT = '%Y-%m-%d %H:%M:%S'
log_dir = os.getenv("LOG_DIR", "logs")
log_level = os.getenv("LOG_LEVEL", "WARNING")
logname_template = os.path.join(log_dir, "mqutils_{}.log")
logging.basicConfig(filename=logname_template.format(datetime.today().strftime("%Y%m%d")),
                    format='%(asctime)-2s --%(filename)s-- %(levelname)-8s %(message)s', datefmt=DATEFORMAT,
                    level=log_level)

class ConnectionParams:
    def __init__(self, conn, queue, host, port, user, password, ack="client-individual"):
        self.conn = conn
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ack = ack


def get_mq_connection(queue=None):
    logging.debug("************************ MQUTILS - GET_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('MQ_HOST')
        port = os.getenv('MQ_PORT')
        user = os.getenv('MQ_USER')
        password = os.getenv('MQ_PASSWORD')
        if (queue is None):
            queue_name = os.getenv('QUEUE_NAME')
        else:
            queue_name = queue
        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        connection_params = ConnectionParams(conn, queue_name, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        logging.error(e)
        raise (e)
    return connection_params


def notify_email_message(subject, body, recipients=None, exception: Exception=None, queue=None):
    '''Creates a json message to notify the listener to send an error email message'''
    logging.debug("************************ MQUTILS - NOTIFY_EMAIL_MESSAGE *******************************")
    message = "No message"
    try:
        if (queue is None):
            queue_name = os.getenv('QUEUE_NAME')
        else:
            queue_name = queue

        if exception is not None:
            exc = traceback.format_exc(exception)
            body = body + "\n\n" + exc
            
        msg_json = {
            "subject": subject,
            "body": body,
            "recipients": recipients
        }

        expiration = _get_expiration()

        logging.debug("msg json:")
        logging.debug(msg_json)
        message = json.dumps(msg_json)
        connection_params = get_mq_connection(queue_name)
        connection_params.conn.send(queue_name, message, headers={"persistent": "true", "expires": expiration})
        logging.debug("MESSAGE TO QUEUE notify_email_message")
        logging.debug(message)
    except Exception as e:
        logging.error(e)
        raise e
    return message


def _get_expiration():
    # Default to one hour from now
    now_in_ms = int(time.time()) * 1000
    expiration = int(os.getenv('MESSAGE_EXPIRATION_MS', 36000000)) + now_in_ms
    return expiration
