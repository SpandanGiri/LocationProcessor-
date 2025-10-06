from pika_client import PikaClient


QUEUE_NAME = 'db_queue'

pika_client = PikaClient()

def processDB(msg:dict):
    print(f"added log for user {msg.get("email")}")

async def send_db(msg:dict):
    await pika_client.send_message(QUEUE_NAME,msg)

async def consume_db(loop):
    return await pika_client.consume(loop,QUEUE_NAME,processDB)

