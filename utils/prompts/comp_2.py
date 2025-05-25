def prompt(tema: str) -> str:
    prompt = f"""
COMPETÊNCIA 2 - COMPREENSÃO E DESENVOLVIMENTO TEMÁTICO:

- Nessa competência, será feita uma análise sobre a abordagem do tema e o uso de repertório sociocultural.
- O tema em questão é: "{tema}"

- Avalie a compreensão e desenvolvimento do tema proposto
- Analise o uso de repertório sociocultural (filmes, livros, poemas, etc.)]

- Avalie o uso efetivo de repertório legítimo e relevante

- Analise os traços de outros tipos textuais, lembre-se que o tipo da redação deve ser dissertativo argumentativo.
- Se, no texto, for predominante o uso de outros tipos textuais, a redação deve ser zerada. 
- Caso sejam encontrados apenas alguns traços de outros tipos textuais, apenas dê nota 40 na competência.

- Se o estudante não seguir o tema "{tema}", a pontuação da redação DEVE ser ZERO(0)
- A fuga ao tema resulta em nota ZERO(0), independente da qualidade da escrita
"""
    return prompt