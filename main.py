import os
import json
import google.generativeai as genai

# Pega a chave da API do Gemini enviada pelo GitHub Actions
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    raise ValueError("ERRO: GEMINI_API_KEY nao encontrada nos Secrets!")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==============================================================================
# ⚽ EDITE AQUI OS JOGOS DO DIA QUE VOCÊ QUER ANALISAR:
# ==============================================================================
JOGOS_DE_HOJE = [
    {"jogo": "Flamengo vs Palmeiras", "liga": "Brasileirão Série A", "horario": "21:30"},
    {"jogo": "São Paulo vs Corinthians", "liga": "Brasileirão Série A", "horario": "19:30"},
    {"jogo": "Atlético-MG vs Cruzeiro", "liga": "Brasileirão Série A", "horario": "18:30"},
    {"jogo": "Real Madrid vs Barcelona", "liga": "El Clásico", "horario": "16:00"},
    {"jogo": "Liverpool vs Manchester City", "liga": "Premier League", "horario": "12:30"}
]
# ==============================================================================

def analisar_jogo(jogo, liga, horario):
    prompt = f"""
    Atue como um analista tático de futebol profissional.
    Analise a partida: {jogo} ({liga} - {horario}).

    Retorne APENAS um JSON estrito no seguinte formato (sem formatação markdown extra, apenas o JSON):
    {{
      "jogo": "{jogo}",
      "liga": "{liga}",
      "clima_e_gramado": "Condições climáticas esperadas e impacto na velocidade da bola e desgaste dos atletas",
      "desfalques_e_escalacao": "Ajustes táticos, suspensos e prováveis formações",
      "historico_e_momento": "Desempenho recente e retrospecto do confronto",
      "palpite_recomendado": "Melhor oportunidade de mercado tático",
      "odd_estimada": "1.85",
      "nivel_confianca": "Alta",
      "resumo_analise": "Justificativa tática aprofundada para a entrada recomendada"
    }}
    """
    try:
        response = model.generate_content(prompt)
        txt
