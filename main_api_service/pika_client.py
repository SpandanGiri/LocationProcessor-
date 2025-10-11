import pika
import os
import uuid
import json
import aio_pika

env = os.environ

DATA_PROCESS_QUEUE = 'process_publish_queue'


class PikaClient:
    def __init__(self):
        pass

    async def send_message(self,queue_name:str,message: dict):
        connection = await aio_pika.connect_robust(host='rabbitmq',port=5672)
        

        async with connection:

            channel = await connection.channel()

            await channel.declare_queue(queue_name, durable=True)

            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message).encode(),correlation_id=str(uuid.uuid4()),),
                routing_key=queue_name,
            )


    async def consume(self,loop,queue_name:str,callback):
        connection = await aio_pika.connect_robust(host='rabbitmq',port=5672,loop=loop)
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name)

        async def process_incoming_message(message):
            await message.ack()
            body = message.body
            if body:
                callback(json.loads(body))        

        await  queue.consume(process_incoming_message)

        return connection

