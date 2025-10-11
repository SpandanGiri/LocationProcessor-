import asyncio
from geopy.distance import geodesic
from pika_client import PikaClient

kolkata = (22.5726, 88.3639)
pika_client = PikaClient()

async def processDist(msg):
    print(f"Processing distance of {msg}")
    user_location = (msg.get('lat'), msg.get('long'))
    userdist = geodesic(kolkata, user_location).km
    print(f"Calculated distance: {userdist} km")

    await pika_client.send_message('db_queue', {'dist': userdist, 'email': msg.get('email')})
    print('Sent to db_queue')

async def main():
    print('keep your mind open')
    await pika_client.consume('process_dist_queue', processDist)

if __name__ == "__main__":
    asyncio.run(main())
