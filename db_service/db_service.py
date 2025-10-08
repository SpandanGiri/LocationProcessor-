from main_api_service.pika_client import PikaClient
from sqlmodel import Field, SQLModel, create_engine, Session
from main_api_service.models import User

QUEUE_NAME = 'db_queue'
DATABASE_URL = "sqlite:///./master.db"

engine = create_engine(DATABASE_URL, echo=True)

def createDb():
    SQLModel.metadata.create_all(engine)

def getSession():
    with Session(engine) as session:
        yield session


pika_client = PikaClient()

def processDB(msg:dict):
    print(f"added log for user {msg.get("email")}")

async def send_db(msg:dict):
    await pika_client.send_message(QUEUE_NAME,msg)

async def consume_db(loop):
    return await pika_client.consume(loop,QUEUE_NAME,processDB)

