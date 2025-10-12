from pika_client import PikaClient
import asyncio

DB_QUEUE_NAME = 'db_queue'


pika_client = PikaClient()

async def processDB(msg:dict):
    print(f"added log for user {msg}")



async def main():
    await pika_client.consume(DB_QUEUE_NAME,processDB)


if __name__ == "__main__":
    asyncio.run(main())


