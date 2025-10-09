from fastapi import FastAPI, BackgroundTasks
from models import UserLocationModel
from pika_client import PikaClient
import asyncio
from contextlib import asynccontextmanager

PROCESS_QUEUE_NAME = 'process_dist_queue'

pika_client = PikaClient()

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/')
def test():
    return {"I am alive"}

@app.post('/send')
async def getLocation(userLoc : UserLocationModel):
    userLoc_dump = userLoc.model_dump()
    await pika_client.send_message(PROCESS_QUEUE_NAME,userLoc_dump)
    return {"queued_message": userLoc_dump}



