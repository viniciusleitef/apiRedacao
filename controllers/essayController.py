from fastapi import HTTPException, UploadFile, File
from PIL import Image
import io
import sys
import os
import random
import numpy as np
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.correctEssay import ENEMCorrector
from schemas.essay import EssayRequest

corrector = ENEMCorrector('Tema geral, qualquer tema')

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
    
    return {
        "message": "Imagem processada com sucesso!",
        "essay_text": structured_text
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
    feedback_geral = response['feedback_geral']
    print(feedback_geral)
    return {
        "nota_final": nota_final,
        "competencias": competencias,
        "comentarios": comentarios,
        "feedback_geral": feedback_geral
    }


# def format_feedback_text(raw_text: str) -> str:
#     # 1. Negrito: **texto** → <strong>texto</strong>
#     formatted = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", raw_text)

#     # 2. Adiciona <br><br> depois de dois pontos seguidos por espaço, como títulos
#     formatted = re.sub(r"(:)( )", r":<br><br>", formatted)

#     # 3. Adiciona <br><br> antes de listas numeradas (ex: "1. ")
#     formatted = re.sub(r"(?<!\d)(\d\.\s)", r"<br><br>\1", formatted)

#     # 4. Espaçamento entre parágrafos longos (heurística: ponto final seguido de espaço + maiúscula)
#     formatted = re.sub(r"(\.)(\s)([A-Z])", r".<br><br>\3", formatted)

#     return formatted