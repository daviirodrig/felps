import functools
import os
import threading

import pika
from dotenv import load_dotenv

import check_chat

load_dotenv()
def ack_message(ch, delivery_tag):
    """Note that `ch` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def do_work(ch, delivery_tag, body):
    vod_id = str(body.decode())
    check_chat.main(vod_id)
    cb = functools.partial(ack_message, ch, delivery_tag)
    ch.connection.add_callback_threadsafe(cb)


def on_message(ch, method_frame, _header_frame, body, args):
    thrds = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(ch, delivery_tag, body))
    t.start()
    thrds.append(t)


parameters = pika.ConnectionParameters("localhost", credentials=pika.PlainCredentials(os.environ["rabbit_user"], os.environ["rabbit_password"]))
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue="vods_to_be_processed", durable=True)

channel.basic_qos(prefetch_count=1)

threads = []
on_message_callback = functools.partial(on_message, args=(threads))
channel.basic_consume("vods_to_be_processed", on_message_callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()
