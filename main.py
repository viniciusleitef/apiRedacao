import uvicorn
from fastapi import FastAPI, UploadFile, File 
from fastapi.middleware.cors import CORSMiddleware

import controllers.essayController as essayController
from schemas.essay import EssayRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-image")
async def upload_image(image: UploadFile = File(...)):
    return await essayController.read_essay(image)
        
@app.post("/correct-essay")
async def correct_essay(data: EssayRequest):
    data.essay_text
    return await essayController.correct_essay(data)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5656, reload=True) 