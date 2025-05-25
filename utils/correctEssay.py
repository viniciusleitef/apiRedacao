from openai import OpenAI
from google.cloud import vision
from typing import Dict, List, TypedDict
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from utils.prompts import comp_1, comp_2, comp_3, comp_4, comp_5

load_dotenv()

# Configurações de API
print(os.getenv("GOOGLE_VISION_AUTH_PATH"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_VISION_AUTH_PATH")
gpt_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=gpt_key)

# Configurações
class CompetenciaResult(TypedDict):
    pontuacao: int
    pontos_fortes: List[str]
    areas_melhoria: List[str]
    sugestoes: List[str]
    
class ZeroRedacaoResult(TypedDict):
    zerar_redacao: bool

class ENEMCorrector:
    """Classe principal para correção de redações do ENEM com multiagentes"""
    
    def __init__(self, tema: str):
        self.tema = tema
        self.ocr_client = vision.ImageAnnotatorClient()
        self.agents_config = self._setup_agents_config(tema=self.tema)
        self.theory_agent = self._create_theory_agent()

    def _create_theory_agent(self) -> Dict:
        """Configura o agente de referencial teórico"""
        return {
            'role': "Especialista em Referencial Teórico",
            'goal': "Sugerir bibliografia para melhoria em cada competência",
            'backstory': "Doutor em Educação com especialização em metodologias de ensino",
            'prompt_template': """
            Com base nas seguintes avaliações:
            {avaliacoes}
            
            Sugira para cada competência com nota abaixo de 160:
            1. 2 referências bibliográficas específicas
            2. 1 material didático complementar
            3. 1 exercício prático
            
            Além disso, sugira 3 livros, 3 filmes e 3 músicas que se relacionam com o tema da redação para que o estudante possa explorar mais sobre o tema socioculturalmente.
            
            Formato JSON (exato):
            {{
                "competencias": {{
                    "1": {{
                        "referencias": ["Obra 1", "Obra 2"],
                        "material": "Material sugerido",
                        "exercicio": "Exercício específico"
                    }},
                    "3": {{
                        ...
                    }}
                }},
                "repertorio_sociocultural": {{
                    "livros": ["Livro 1", "Livro 2", "Livro 3"],
                    "filmes": ["Filme 1", "Filme 2", "Filme 3"],
                    "musicas": ["Música 1", "Música 2", "Música 3"]
                }}
            }}
            """
        }

    def _setup_agents_config(self, tema: str) -> Dict[int, Dict]:
        """Configuração completa dos critérios de todas as competências"""
        return {
            1: {
                'role': "Especialista em Norma Culta da Língua Portuguesa",
                'goal': "Avaliar domínio da língua portuguesa formal",
                'backstory': "Professor de Língua Portuguesa com 20 anos de experiência",
                'aspectos_avaliados': "Estrutura sintática e desvios gramaticais.",
                'detalhamento_competencia': comp_1.prompt(),
                'criteria': {
                    200: "Excelente domínio da escrita formal. Para atingir essa nota, o texto deve conter, no máximo: 2 desvios gramaticais e 1 falha de estrutura sintática OU 2 falhas de estrutura sintática sem desvios gramaticais OU 3 desvios gramaticais sem falha de estrutura sintática. Acima desses limites, a pontuação na competência será reduzida.",
                    160: "Bom domínio da escrita formal. Apresenta alguns desvios gramaticais e/ou falhas de estrutura sintática, totalizando entre 4 e 9 erros gerais. A clareza e a progressão das ideias são mantidas.",
                    120: "Domínio mediano da escrita formal. Apresenta um número significativo de desvios gramaticais e/ou falhas de estrutura sintática, totalizando entre 10 e 15 erros gerais. A compreensão do texto pode ser ocasionalmente comprometida devido a esses desvios.",
                    80: "Estrutura sintática deficitária ou muitos desvios gramaticais. Apresentar um ou outro: Muitos desvios gramaticais, mas poucas falhas de estrutura sintática OU Estrutura sintática deficitária, mas poucos desvios gramaticais.",
                    40: "Estrutura sintática deficitária com muitos desvios gramaticais. Os dois problemas juntos: Muitos desvios gramaticais e estrutura sintática deficitária.",
                    0: "Estrutura sintática inexistente (independente da quantidade de desvios gramaticais)."
                },
            },
            2: {
                'role': "Especialista em Desenvolvimento Temático",
                'goal': "Avaliar abordagem do tema, estrutura dissertativa e uso de repertório sociocultural",
                'backstory': "Mestre em Análise do Discurso especializado no ENEM",
                'aspectos_avaliados': "Abordagem completa do tema; Uso de repertório sociocultural; 3 partes do texto: Introdução, Desenvolvimento e Conclusão; Tipologia textual: dissertativo-argumentativo",
                'detalhamento_competencia': comp_2.prompt(tema=tema),
                'criteria': {
                    200: "Abordagem completa do tema. 3 partes do texto presentes: Introdução, Desenvolvimento e Conclusão, nenhuma delas embrionária(parágrafo com até 2 linhas) E Repertório legitimado e pertinente ao tema COM uso produtivo(bem relacionado ao tema).",
                    160: "Abordagem completa do tema. 3 partes do texto presentes: Introdução, Desenvolvimento e Conclusão, nenhuma delas embrionária(parágrafo com até 2 linhas) E Repertório legitimado e pertinente ao tema, mas SEM uso produtivo(não relaciona bem com o tema).",
                    120: "Abordagem completa do tema. 3 partes do texto presentes: Introdução, Desenvolvimento e Conclusão, 1 delas pode ser embrionária(parágrafo com até 2 linhas). E Repertório não legitimado E/OU Repertório legitmado, mas não pertinente ao tema.", # E/OU Repertório baseado nos textos motivadores.
                    80: "Abordagem completa do tema. 3 partes do texto presentes: Introdução, Desenvolvimento e Conclusão, sendo 2 delas embrionárias(parágrafos com até 2 linhas) OU Conclusão finalizada por frase incompleta.", # Redações que apresentam muitos trechos de cópia não devem ultrapassar essa nota (1/3 das linhas de cópia).
                    40: "Tangência ao tema OU texto composto por aglomerado caótico de palavras OU traços constantes de outros tipos textuais OU topicalização(textos com travessão no início dos parágrafos)."
                },
            },
            3: {
                'role': "Especialista em Coerência Argumentativa",
                'goal': "Avaliar: seleção e relação de fatos e opiniões em defesa de um ponto de vista",
                'backstory': "Doutor em Teoria da Argumentação",
                'aspectos_avaliados': "Lógica dos argumentos; Coerência das informações; Organização das ideias",
                'detalhamento_competencia': comp_3.prompt(),
                'criteria': {
                    200: "Projeto de texto estratégico. Desenvolvimento de informações, fatos e opiniões em todo o texto. Aqui se admitem deslizes pontuais, sejam de projeto e/ou de desenvolvimento.",
                    160: "Projeto de texto com poucas falhas. Desenvolvimento de informações, fatos e opiniões com poucas lacunas.",
                    120: "Projeto de texto com algumas falhas. Desenvolvimento informações, fatos e opiniões com algumas lacunas.", # Textos que apresentam argumentos dos textos motivadores não devem ultrapassar essa nota.
                    80: "Projeto de texto com muitas falhas. Sem desenvolvimento ou com desenvolvimento de apenas uma informação, fato ou opinião. Textos que apresentam contradição grave não devem ultrapassar essa nota.",
                    40: "Projeto de texto sem foco temático ou com foco temático distorcido. Textos tangentes ao tema não devem ultrapassar essa nota.",
                    0: "Aglomerado caótico de palavras, independente da abordagem do tema."
                },

            },
            4: {
                'role': "Especialista em Coesão Textual",
                'goal': "Avaliar articulação entre partes do texto",
                'backstory': "Especialista em Linguística Textual",
                'aspectos_avaliados': "Uso de elementos coesivos; Conectivos interparágrafos(entre parágrafos); Conectivos intraparágrafos(dentro do parágrafo); Variedade de conectores",
                'detalhamento_competencia': comp_4.prompt(),
                'criteria': {
                    200: "Resenha expressiva de elementos coesivos intraparágrafos e interparágrafos E raras ou ausentes repetições E sem inadequação. Presença de, no mínimo, 2 conectivos interparágrafos ao longo de todo o texto e, no mínimo, 2 conectivos intraparágrafos em cada parágrafo.",
                    160: "Presença constante de elementos coesivos intraparágrafos e interparágrafos E/OU poucas repetições E/OU poucas inadequações.", # Perguntar sobre qt de conectivos nesse nível e nos outros (se tiver).
                    120: "Presença regular de elementos coesivos intraparágrafos e/ou interparágrafos E/OU algumas repetições E/OU algumas inadequações.",
                    80: "Presença pontual de elementos coesivos intraparágrafos e/ou interparágrafos E/OU muitas repetições E/OU muitas inadequações.", # Textos em forma de monobloco não devem ultrapassar essa nota.
                    40: "Presença rara de elementos coesivos intraparágrafos e/ou interparágrafos E/OU excessivas repetições E/OU excessivas inadequações.",
                    0: "Ausência de articulação: palavras e/ou períodos desconexos ao longo de todo o texto."
                },
            },
            5: {
                'role': "Especialista em Proposta de Intervenção",
                'goal': "Avaliar proposta de solução para o problema",
                'backstory': "Consultor em Políticas Públicas Educacionais",
                'aspectos_avaliados': "Presença dos cinco elementos da proposta de intervenção; Viabilidade da proposta; Relação com o problema discutido",
                'detalhamento_competencia': comp_5.prompt(),
                'criteria': {
                    200: "Proposta detalhada e perfeitamente articulada. Todos os cinco elementos presentes e válidos: Agente, Ação, Meio/Modo, Finalidade e Detalhamento.",
                    160: "4 elementos válidos.",
                    120: "3 elementos válidos.",
                    80: "2 elementos válidos.",
                    40: "Tangenciamento do tema OU apenas 1 elemento válido.",
                    0: "Ausência de proposta OU proposta de intervenção que desrespeita direitos humanos OU proposta de intervenção não relacionada ao assunto do tema."
                },
            }
        }

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extrai texto de imagem usando Google Vision OCR a partir de bytes"""
        image = vision.Image(content=image_bytes)
        response = self.ocr_client.text_detection(image=image)
        return response.text_annotations[0].description

    def _process_text_only(self, text: str, tema: str = None) -> Dict:
        """Processamento alternativo para texto digitado diretamente"""
        clean_text = self.correct_text_with_gpt(text)
        
        results = {}
        for competencia in range(1, 6):
            results[competencia] = self.evaluate_competence(competencia, clean_text, tema)
        
        referencial = self.get_theoretical_references(results)
        
        return {
            "competencias": results,
            "pontuacao_total": sum(result['pontuacao'] for result in results.values()),
            "feedback_geral": self.generate_final_feedback(results),
            "referencial_teorico": referencial
        }

    def correct_text_with_gpt(self, text: str) -> str:
        """Corrige erros do OCR usando GPT-4 e remove cabeçalhos/rodapés/numeração"""
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "system",
                "content": """Você é um corretor especializado em reconstrução textual. Corrija erros do OCR mantendo o conteúdo original. Siga estas instruções:
                
    1. Corrija erros do OCR mantendo fielmente o conteúdo original da redação
    2. Remova completamente:
    - Cabeçalhos (qualquer texto no topo da página)
    - Rodapés (qualquer texto no final da página)
    - Numeração de linhas ou páginas
    - Marcas de identificação do aluno
    - Qualquer texto que não faça parte do corpo da redação
    3. Mantenha todos os elementos textuais da redação:
    - Título (se houver)
    - Parágrafos completos
    - Pontuação original
    - Estrutura do texto
    4. Se o texto já estiver limpo, apenas corrija os erros de OCR sem modificar a estrutura

    Retorne APENAS o texto da redação corrigido e limpo, sem comentários adicionais."""
            }, {
                "role": "user",
                "content": f"Corrija este texto extraído por OCR mantendo o conteúdo original:\n\n{text}"
            }],
            temperature=0.2  # Reduzido para maior consistência
        )
        return response.choices[0].message.content.strip()

    def evaluate_competence(self, competencia_num: int, text: str, tema: str = None) -> CompetenciaResult:
        """Avalia uma competência específica usando GPT-4"""
        config = self.agents_config[competencia_num]
        
        prompt = f"""
        Você é um especialista em correção de redações do ENEM ({config['role']}).
        Além disso, você é um {config['backstory']}
        
        A redação avaliada tem o seguinte Tema proposto: {tema if tema else 'Não especificado'}
        
        Objetivo:
        {config['goal']}
        
        Avalie rigorosamente segundo a Competência {competencia_num}:
        
        Aspectos avaliados:
        {config['aspectos_avaliados']}
        
        Critérios:
        {self._format_criteria(config['criteria'])}
        
        Detalhamento da competência:
        {config['detalhamento_competencia']}
        
        - A pontuação deve estar entre 0 e 1000.
        
        - Lembre-se que 1000 pontos em uma redação do ENEM é bastante incomum, então verifique se a pontuação que você deu é realista, mas não precisa reduzir a pontuação só para que não seja 1000.
        
        - Sempre responda em português.
        
        Texto para avaliação:
        {text}
        
        Retorne EXATAMENTE neste formato JSON:
      
        {{
            "pontuacao": int (0-200),
            "pontos_fortes": ["item1", "item2"],
            "areas_melhoria": ["item1", "item2"],
            "sugestoes": ["sugestao1", "sugestao2"],
            "fuga_tema": bool (apenas para Competência 2)
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14", # gpt-4-turbo-preview
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def zero_redacao(self) -> ZeroRedacaoResult:
        prompt = f"""
        Você é um especialista em correção de redações do ENEM.
        Você deve avaliar alguns critérios para saber se a redação deve ser zerada.
        
        Critérios para zerar a redação:
        - Violação de direitos humanos
        - Redação de um tipo textual diferente do dissertativo-argumentativo
        
        Se o usuário cometer alguma dessas violações, não importa quão boa seja a escrita, a redação deve ser zerada.
        
        Retorne EXATAMENTE neste formato JSON:
        {{
            "zerar_redacao": bool
        }}
        
        (True para zerar a redação, False para não zerar)
        """
        # Adicionar mais critérios para zerar a redação
            
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14", # gpt-4-turbo-preview
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

    def _format_criteria(self, criteria: Dict[int, str]) -> str:
        """Formata os critérios para incluir no prompt"""
        return "\n".join([f"{pts} pts: {desc}" for pts, desc in criteria.items()])
    
    def generate_final_feedback(self, results: Dict[int, CompetenciaResult]) -> str:
        """Gera feedback geral consolidado"""
        prompt = f"""
        Com base nestes resultados parciais:
        {json.dumps(results, indent=2)}
        
        Gere um feedback final para o aluno contendo:
        1. Visão geral do desempenho
        2. 3 principais pontos fortes
        3. 3 principais áreas para melhoria
        4. 3 recomendações gerais para próxima redação
        
        Seja detalhado, pedagógico e encorajador.
        """
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content

    def get_theoretical_references(self, results: Dict[int, CompetenciaResult]) -> Dict:
        """Agente que gera referencial teórico personalizado"""
        # Filtra competências com nota abaixo de 160
        weak_competences = {
            k: v for k, v in results.items() 
            if v['pontuacao'] < 160
        }
        
        prompt = self.theory_agent['prompt_template'].format(
            avaliacoes=json.dumps(weak_competences, indent=2)
        )
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def correct_redacao(self, text:str, ) -> Dict:  
        print(self.tema)
        print(text)
        print("✍️ Corrigindo erros do OCR...")
        clean_text = self.correct_text_with_gpt(text)
        
        print("📊 Avaliando competências...")
        results = {}
        for competencia in range(1, 6):
            results[competencia] = self.evaluate_competence(competencia_num=competencia, text=clean_text, tema=self.tema)

        print("📊 Avaliando Fuga de tema...")
        # Verificação especial para fuga ao tema
        if self.tema and results[2].get('fuga_tema', False):
            for competencia in results:
                results[competencia]['pontuacao'] = 0  # Nota zero em todas competências
                
        print("📊 Avaliando outros critérios para zerar a redação...")
        zero_redacao = self.zero_redacao()
        if zero_redacao['zerar_redacao']:
            for competencia in results:
                results[competencia]['pontuacao'] = 0  # Nota zero em todas competências
        
        print("📚 Gerando referencial teórico...")
        referencial = self.get_theoretical_references(results)
        
        print("✨ Consolidando resultados...")
        total_score = sum(result['pontuacao'] for result in results.values())
        
        return {
            "competencias": results,
            "pontuacao_total": total_score,
            "feedback_geral": self.generate_final_feedback(results),
            "referencial_teorico": referencial
        }

if __name__ == "__main__":
    print("✅ Iniciando correção ENEM...")
    tema = "O estigma associado às doenças mentais na sociedade brasileira"
    corretor = ENEMCorrector(tema=tema)
    resultado = corretor.correct_redacao(image_path="redacao.jpg", tema=tema)
    
    print("\n=== 🎯 RESULTADO FINAL ===")
    print(f"Pontuação Total: {resultado['pontuacao_total']}/1000")
    
    for comp, res in resultado['competencias'].items():
        print(f"\n🔹 Competência {comp}: {res['pontuacao']}/200")
        print("✅ Pontos fortes:")
        print("\n".join(f"- {p}" for p in res['pontos_fortes']))
        print("📌 Sugestões:")
        print("\n".join(f"- {s}" for s in res['sugestoes']))
    
    print("\n=== 📖 REFERENCIAL TEÓRICO ===")
    for comp, dados in resultado['referencial_teorico']['competencias'].items():
        print(f"\n📚 Para Competência {comp}:")
        print("📚 Referências:")
        print("\n".join(f"- {r}" for r in dados['referencias']))
        print("🛠️ Exercício recomendado:")
        print(f"- {dados['exercicio']}")
    
    print("\n=== ✨ FEEDBACK GERAL ===")
    print(resultado['feedback_geral'])