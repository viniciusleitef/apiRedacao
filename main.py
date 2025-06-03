import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from typing import Optional
from models.model import Redacao
from sqlalchemy.orm import Session  

import controllers.essayController as essayController

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@app.post("/upload-image")
#async def upload_image(image: UploadFile = File(...)):
#    return await essayController.read_essay(image)

@app.post("/correct-essay")
async def correct_essay(
    essay_text: Optional[str] = Form(None),
    essay_theme: str = Form(...),
    essay_motivational_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = Form(None),
    db: Session = Depends(get_db)
):
    if not file and not essay_text:
        return {"error": "Obrigatório fornecer o texto de redação ou um arquivo de imagem"}
    
    data = {
        "essay_text": essay_text,
        "essay_theme": essay_theme,
        "essay_motivational_text": essay_motivational_text
    }
    
    return await essayController.correct_essay(db, data, file)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5656, reload=True) 