from fastapi import FastAPI 
from contextlib import asynccontextmanager 
from pymongo import MongoClient
from dotenv import dotenv_values
from routes import router
import uvicorn

config = dotenv_values('credentials.env')


async def connectToDatabase():
    db = MongoClient(config['MONGO_CONNECTION_STRING'])
    print(db)
    return db 

@asynccontextmanager
async def lifespan(app:FastAPI):
    print('Startup has begun')
    dbHost = await connectToDatabase()
    app.players = dbHost.tournament.players
    yield 
    print('Shutdown has begun')
    

    
    
app = FastAPI(lifespan=lifespan, docs_url='/')
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
    



    
