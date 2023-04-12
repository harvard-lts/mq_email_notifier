import json
import logging
import sys
import time
from typing import Optional

import stomp
sys.path.append('mqresources')
import mqutils
from stomp.utils import Frame


logging.basicConfig(format='%(message)s')

queue_name = "/queue/test-mq-email-notifier"


def test_get_mq_connection():
    connection_params = mqutils.get_mq_connection()
    assert connection_params.conn is not None


def test_notification():
    '''Sends a status message to the  queue and verifies that it made it'''
    # Send the message
    message = mqutils.notify_email_message("Test Subject", "Test Body", None, None, queue_name)
    assert type(message) is str
    message_dict = json.loads(message)
    mq_listener_object = TestConnectionListener()

    counter = 0
    # Try for 30 seconds then fail
    while mq_listener_object.get_message_body() is None:
        time.sleep(2)
        counter = counter + 2
        if counter >= 10:
            assert False, "test_notification: could not find anything on the {} after 30 seconds".format(queue_name)

    message_body = mq_listener_object.get_message_body()
    assert message_body is not None
    assert type(message_body) is dict
    assert message_body == message_dict

    mq_listener_object.disconnect()


class TestConnectionListener(stomp.ConnectionListener):
    def __init__(self) -> None:
        self._connection = self.__create_subscribed_connection()
        self.message_body = None

    def __create_subscribed_connection(self) -> stomp.Connection:
        connection_params = mqutils.get_mq_connection(queue_name)
        connection = connection_params.conn
        connection_params.conn.set_listener('', self)
        connection.subscribe(queue_name, id=1, ack="client-individual")
        return connection

    def on_message(self, frame: Frame) -> None:
        headers, body = frame.headers, frame.body
        message_id = headers.get('message-id')
        self._connection.ack(message_id, 1)
        self.message_body = json.loads(body)

    def get_message_body(self) -> Optional[dict]:
        return self.message_body

    def disconnect(self) -> None:
        self._connection.disconnect()
