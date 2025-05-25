from fastapi import HTTPException, UploadFile, File
from PIL import Image
import io
import sys
import os
import random
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.correctEssay import ENEMCorrector
from schemas.essay import EssayRequest

corrector = ENEMCorrector('Tema geral, qualquer tema')

async def read_essay(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")
    image_bytes = await image.read()
    text = corrector.extract_text_from_image(image_bytes)
    text = corrector.correct_text_with_gpt(text)
    return {
        "message": "Imagem processada com sucesso!",
        "essay_text": text
    }
    #contents = await image.read()
    #pil_image = Image.open(io.BytesIO(contents))
    #image_np = np.array(pil_image)
    ##essay_text = ler_arquivo_redacao_mem(pil_image)
    #processor.process_image(image_np)
    #text = processor.get_full_text()
    #print(text['texto_completo'])
    
    #return {
    #    "message": "Imagem processada com sucesso!",
    #    "essay_text": text['texto_completo']
    #}

async def improve_essay(essay_text: str):
    pass

async def correct_essay(data: EssayRequest):
    corrector.tema = data.essay_theme
    response = corrector.correct_redacao(data.essay_text)
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
    return {
        "nota_final": nota_final,
        "competencias": competencias,
        "comentarios": comentarios
    }