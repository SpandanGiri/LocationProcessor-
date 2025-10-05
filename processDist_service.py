from pika_client import PikaClient

pika_client = PikaClient()

QUEUE_NAME = 'process_dist_queue'

def processDist(msg:dict):
    print(f"Processed  + {msg}")


async def send_process_dist(msg:dict):
    await pika_client.send_message(QUEUE_NAME,msg)


async def consume_process_dist(loop):
    await pika_client.consume(loop,QUEUE_NAME,processDist)
