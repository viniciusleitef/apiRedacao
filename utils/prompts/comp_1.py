def prompt() -> str:
    prompt = f"""
COMPETÊNCIA 1 - DOMÍNIO DA NORMA CULTA:

- Avalie o domínio do padrão formal escrito da língua portuguesa.
- Seja flexível com erros de OCR, mas mantenha o rigor na avaliação.
- Ao identificar erros, destaque-os mostrando a forma correta.
- Nessa competência você irá avaliar a quantidade de erros categorizados em: desvios gramaticais e falhas de estrutura sintática.

- São considerados desvios gramaticais ocorrências na escrita que fogem às regras estabelecidas pela gramática normativa da língua portuguesa.
- Principais tipos de desvios gramaticais:
  - Barbarismo: Erro na grafia, acentuação ou uso da palavra. Exemplo errado: "Ele rúbricou o documento". Exemplo correto: "Ele rubricou o documento";
  - Pleonasmo Vicioso: Repetição desnecessária de ideias. Exemplo errado: "Subir para cima" Exemplo correto: "Subir";
  - Vulgarismo / Oralidade: Uso de linguagem informal ou gírias em contexto formal. Exemplo errado: "A gente fomos ao debate" Exemplo correto: "Nós fomos ao debate".

- São consideradas falhas de estrutura sintática erros na forma como as palavras e frases são organizadas dentro de uma oração ou período, prejudicando a coerência e a coesão do texto.
- Principais tipos de falhas de estrutura sintática:
  - Erro de Concordância:Desacordo entre sujeito e verbo, ou nome e seus determinantes. Exemplo errado: "É necessário mudanças". Exemplo correto: "São necessárias mudanças";
  - Erro de Regência:Uso incorreto ou omissão de preposição exigida por verbo ou nome. Exemplo errado: "Ele assistiu o filme". Exemplo correto: "Ele assistiu ao filme";
  - Erro de Crase: Uso incorreto ou omissão do acento grave. Exemplo errado: "Ele foi a escola". Exemplo correto: "Ele foi à escola";
  - Erro de Colocação Pronominal: Posicionamento inadequado de pronomes oblíquos átonos. Exemplo errado: "Me disseram a verdade." Exemplo correto: "Disseram-me a verdade." ou "Não me disseram a verdade."
  - Erro de Pontuação: Uso inadequado ou omissão de sinais de pontuação."A sociedade, precisa de leis mais rígidas" (Vírgula entre sujeito e verbo)"A sociedade precisa de leis mais rígidas";
  
- A partir de 16 erros gerais, a correção será mais subjetiva com base nos critérios informados para cada pontuação (80, 40 e 0).
"""
    return prompt
