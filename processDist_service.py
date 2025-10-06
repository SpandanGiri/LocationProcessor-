from pika_client import PikaClient
from geopy.distance import geodesic
from db_service import send_db
import asyncio

#kolkata coordinates
kolkata = (22.5726, 88.3639)

pika_client = PikaClient()

QUEUE_NAME = 'process_dist_queue'

def processDist(msg:dict):
    print(f"Processing distance of {msg}")
    user_location = (msg.get('lat'),msg.get('long'))
    userdist = geodesic(kolkata, user_location).km

    asyncio.create_task(send_db({'dist':userdist,'email':msg.get('email')}))

    print('sent to db queue')


async def send_process_dist(msg:dict):
    await pika_client.send_message(QUEUE_NAME,msg)


async def consume_process_dist(loop):
    return await pika_client.consume(loop,QUEUE_NAME,processDist)
