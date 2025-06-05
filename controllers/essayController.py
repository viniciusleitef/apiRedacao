from fastapi import HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import io
import sys
import os
import hashlib

from models.model import Redacao

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.correctEssay import ENEMCorrector
from schemas.essay import EssayRequest

corrector = ENEMCorrector('Tema geral, qualquer tema')

async def get_essay_by_hash_database(db, hash: str):
    return db.query(Redacao).filter(Redacao.hash_imagem == hash).first()
    

async def create_essay_database(db: Session, nota_final: int, competencias: dict, comentarios: dict, imageHash: str, text:str, feedback_geral: str | None = None):
    nova_redacao = Redacao(
        hash_imagem=imageHash,
        nota_final=nota_final,
        competencias=competencias,
        comentarios=comentarios,
        feedback_geral=feedback_geral,
        text = text
    )
    
    db.add(nova_redacao)
    db.commit()
    db.refresh(nova_redacao)  
    return nova_redacao

async def read_essay(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")
    image_bytes = await image.read()
    
    try:
        text = corrector.extract_text_from_image(image_bytes)
    except Exception as e:
        print(f"Erro ao extrair texto da imagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar a imagem com o OCR")
    
    clean_text = corrector.correct_text_with_gpt(text)
    structured_text = corrector.format_text_with_image(image_binary_content=image_bytes, ocr_text=clean_text)
    
    if structured_text == "I'm sorry, I can't assist with that.":
        structured_text = clean_text

    return clean_text

async def correct_essay(db, data: EssayRequest, file: UploadFile = File(...)):
    imageHash = None
    text = data['essay_text']
    if file:
        imageHash = await hash_file(file)                                       # Gera hash da imagem
        essay = await get_essay_by_hash_database(db, imageHash)                 # Se ja existir um hash igual no banco, retorna os dados desse hash e converte para dict
        if essay:
            return await redacao_to_dict(essay)
        text = await read_essay(file)
        
    print(text)
    corrector.tema = data['essay_theme']                                        # Definindo o tema da redação
    response = corrector.correct_redacao(text)                                  # Corrigindo a redação
    # Montar o dicionário no formato CorrecaoRedacao
    competencias = {}
    comentarios = {}
    for i in range(1, 6):
        comp = response['competencias'][i]
        competencias[f'competencia_{i}'] = comp['pontuacao']
        # Comentário: pontos fortes + áreas de melhoria + sugestões (resumido)
        comentario = []
        if comp['pontos_fortes']:
            comentario.append("Pontos fortes: " + ", ".join(comp['pontos_fortes']))
        if comp['areas_melhoria']:
            comentario.append("Áreas de melhoria: " + ", ".join(comp['areas_melhoria']))
        if comp['sugestoes']:
            comentario.append("Sugestões: " + ", ".join(comp['sugestoes']))
        comentarios[f'competencia_{i}'] = " | ".join(comentario)
    nota_final = response['pontuacao_total']
    feedback_geral = response['feedback_geral']
    
    if file:
        await create_essay_database(db, nota_final, competencias, comentarios, imageHash, text, feedback_geral)
    
    return {
        "nota_final": nota_final,
        "competencias": competencias,
        "comentarios": comentarios,
        "feedback_geral": feedback_geral,
        "text": text
    }
    
    
async def hash_file(upload_file: UploadFile) -> str:
    file_content = await upload_file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    await upload_file.seek(0)
    return file_hash

async def redacao_to_dict(redacao: Redacao):
    return {
        "hash_imagem": redacao.hash_imagem,
        "nota_final": redacao.nota_final,
        "competencias": redacao.competencias,
        "comentarios": redacao.comentarios,
        "feedback_geral": redacao.feedback_geral,
        "text": redacao.text
    }


