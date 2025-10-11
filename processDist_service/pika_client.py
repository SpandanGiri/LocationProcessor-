import os
import uuid
import json
import aio_pika

env = os.environ



class PikaClient:
    def __init__(self):
        pass

    async def send_message(self,queue_name:str,message: dict):
        connection = await aio_pika.connect_robust(host='rabbitmq',port=5672)
        
        async with connection:

            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message).encode(),correlation_id=str(uuid.uuid4()),),
                routing_key=queue_name,
            )


    async def consume(self,queue_name:str,callback):
        print('consuming process queue...')
        connection = await aio_pika.connect_robust(host='rabbitmq',port=5672)
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name,durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode())
                    try:
                        await callback(body)
                    except:
                        print('error  in processing')
                        Exception
                    
