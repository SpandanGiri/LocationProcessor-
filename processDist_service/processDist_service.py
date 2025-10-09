from pika_client import PikaClient
from geopy.distance import geodesic
import asyncio

# kolkata coordinates
kolkata = (22.5726, 88.3639)

pika_client = PikaClient()

PROCESS_QUEUE_NAME = 'process_dist_queue'
DB_QUEUE = 'db_queue'

def processDist(msg:dict):
    print(f"Processing distance of {msg}")
    user_location = (msg.get('lat'),msg.get('long'))
    userdist = geodesic(kolkata, user_location).km

    asyncio.create_task(pika_client.send_message(DB_QUEUE,{'dist':userdist,'email':msg.get('email')}))

    print('sent to db queue')



async def consume_process_dist(loop):
    return await pika_client.consume(loop,PROCESS_QUEUE_NAME,processDist)
