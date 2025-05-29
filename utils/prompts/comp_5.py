def prompt() -> str:
    prompt = f"""
COMPETÊNCIA 5 - PROPOSTA DE INTERVENÇÃO:

INSTRUÇÕES:

- Avalie o desenvolvimento da proposta de intervenção e a sua relação com o problema discutido.
- Verifique a presença dos cinco elementos obrigatórios:
  * Agente – Quem fará? Exemplo: "O Estado"
  * Ação – O que será feito? Exemplo: "Criar leis"
  * Meio/Modo – Como será feito? Exemplo: "Por meio da criação de secretarias especializadas"
  * Finalidade – Para quê? Exemplo: "Para conscientizar a população"
  * Detalhamento – Adição de informações mais precisas e completas a um dos elementos da proposta de intervenção.
Caso nenhum dos elementos da proposta de intervenção esteja presente, pontue 0 na competência.

ATENÇÃO:
- Basta que o estudante apresente uma ocorrência de cada elemento da proposta (agente, ação, meio, finalidade e detalhamento); não é preciso repetir nenhum deles.
- O texto pode ter mais de uma proposta de intervenção, aceite e pontue a que contém mais elementos válidos.
- Estruturas condicionais não passam de 80 pontos nessa competência, exemplos como: "Se o governo criar leis..." "Caso a mídia divulgue..." devem ser penalizados.

CONTEXTO:

Explicando melhor o que é o detalhamento:
É o acréscimo de informações sobre um dos elementos da proposta(agente, ação, meio/modo, finalidade), tornando-o mais completo. 

Exemplos de detalhamento:
1. Detalhamento do agente:  
“O Estado, na condição de garantidor dos direitos individuais, deve…”
(O detalhamento aparece ao mencionar a função do agente.)

2. Detalhamento do modo/meio: 
“Por meio da criação de secretarias especializadas, já que o ambiente digital carece de fiscalização eficaz.”
(O trecho “já que…” detalha o porquê do modo escolhido.)

3. Detalhamento da ação:
“Campanhas em mídias sociais, como TV e jornais, que já vêm sendo adotadas em outros países.”
(O parêntese traz um detalhe que reforça a viabilidade da ação.)

4. Detalhamento da finalidade:
“Para conscientizar a população, uma demanda antiga que cresce com o tempo.”
(A frase final aproxima o efeito da realidade atual.)

"""
    return prompt

# Explicar o que é considerado um elemento válido.
