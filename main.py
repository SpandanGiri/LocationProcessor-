from fastapi import FastAPI, BackgroundTasks
from models import UserLocationModel
from pika_client import PikaClient
import asyncio
from contextlib import asynccontextmanager
from processDist_service import consume_process_dist,send_process_dist
from db_service import consume_db

pika_client = PikaClient()

@asynccontextmanager
async def lifespan(app:FastAPI):
    loop = asyncio.get_running_loop()
    processDist_task = loop.create_task(consume_process_dist(loop))
    db_task = loop.create_task(consume_db(loop))
    yield  # startup complete
    processDist_task.cancel()
    db_task.cancel()


app = FastAPI(lifespan=lifespan)

def pushProcessQ(userLoc : UserLocationModel):
    print(f'Pushed {userLoc.email} in Process Queue')
    return {f'Pushed {userLoc.email} in Process Queue'}

@app.get('/')
def test():
    return {"I am alive"}

@app.post('/send')
async def getLocation(userLoc : UserLocationModel,background_tasks:BackgroundTasks):
    userLoc_dump = userLoc.model_dump()
    await send_process_dist(userLoc_dump)
    return {"queued_message": userLoc_dump}





