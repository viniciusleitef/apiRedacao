def prompt(tema: str) -> str:
    prompt = f"""
COMPETÊNCIA 2 - COMPREENSÃO E DESENVOLVIMENTO TEMÁTICO:

- Nessa competência, será feita uma análise sobre a abordagem do tema e o uso de repertório sociocultural.
- O tema em questão é: "{tema}"

VOCÊ DEVE AVALIAR:
- A compreensão e desenvolvimento do tema proposto
- O uso de repertório sociocultural (filmes, livros, poemas, etc.)]
- O uso efetivo de repertório legítimo, produtivo e pertinente

CONTEXTO:

- Repertório legitimado: O aluno dá autoria ao repertório. Exemplo: o livro "1984" de George Orwell. Além disso, o repertório deve pertencer a uma área de conhecimento.
- Repertório pertinente: O repertório deve ser relacionado ao tema.
- Repertório produtivo: Contextualizar o repertório relacionando-o com o tema.

Tome cuidado ao diferenciar tangenciamento e fuga ao tema:

Tangenciamento ao tema:
- Considera-se tangenciamento ao tema uma abordagem parcial baseada somente no assunto mais amplo a que o tema está vinculado, deixando em segundo plano a discussão em torno do eixo temático objetivamente proposto.
- Exemplo, no tema de 2021: "Invisibilidade e registro civil: garantia de acesso à cidadania no Brasil", se o participante tratasse apenas de “registro civil” em geral e não argumentasse sobre a “invisibilidade” e a importância de garantir o “acesso à cidadania no Brasil” poderia ser considerado tangência ao tema.

Fuga ao tema:
- Uma redação que configura fuga ao tema é aquela que não atende à proposta temática, ou seja, é uma redação que “nem o assunto mais amplo nem o tema específico proposto são desenvolvidos”.
- Exemplo: No tema de 2021: "Invisibilidade e registro civil: garantia de acesso à cidadania no Brasil", se o participante, por exemplo, escrevesse sobre outras questões relacionadas à “cidadania” que não tenham a ver com o registro civil, ou até mesmo escrevesse sobre “democracia”, e não abordasse a “invisibilidade” e a “falta de acesso ao registro civil” poderia ser considerado fuga ao tema.

INSTRUÇÕES:
- Analise os traços de outros tipos textuais, lembre-se que o tipo da redação deve ser dissertativo argumentativo.
- Se, no texto, for predominante o uso de outros tipos textuais, a redação deve ser totalmente zerada. 
- Caso sejam encontrados apenas alguns traços de outros tipos textuais, apenas dê nota 40 na competência.
- Ao analisar os reperórios, prevalece o de melhor qualidade para dar nota à competência.
- Se o estudante não seguir o tema "{tema}", a pontuação da redação DEVE ser ZERO(0)
- A fuga ao tema resulta em nota ZERO(0), independente da qualidade da escrita
"""
    return prompt
