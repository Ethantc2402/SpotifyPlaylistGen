from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# change this later to allow only specific origins (in production)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataModel(BaseModel):
    acousticness: str
    danceability: str
    energy: str
    instrumentalness: str
    mood_valence: str
    tempo: str
    prompt: str
    trackId: str

@app.get("/")
def index():
    return {"message": "Spotify Playlist Generator API running..."}

@app.post("/post_features")
async def post_data(data: DataModel):
    
    # use the data to generate the playlist here
    print(data)
    return {"status": 200, "data": data}