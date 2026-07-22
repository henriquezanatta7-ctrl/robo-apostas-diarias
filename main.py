import os
import json
import time
import google.generativeai as genai

# Carregamento da chave do Gemini a partir das Secrets do GitHub
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    raise ValueError("ERRO: A chave GEMINI_API_KEY não foi encontrada nas Secrets do GitHub!")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

# ==============================================================================
# 📋 TODOS OS JOGOS EXTRAÍDOS DAS CAPTURAS DE ECRÃ DO SOFASCORE DE HOJE
# ==============================================================================
JOGOS_DE_HOJE = [
    # --- FUTEBOL: BRASILEIRÃO SÉRIE A ---
    {"jogo": "Coritiba vs Palmeiras", "liga": "Brasileirão Série A", "esporte": "Futebol", "horario": "19:30"},
    {"jogo": "Chapecoense vs Flamengo", "liga": "Brasileirão Série A", "esporte": "Futebol", "horario": "21:30"},
    {"jogo": "Internacional vs Cruzeiro", "liga": "Brasileirão Série A", "esporte": "Futebol", "horario": "21:30"},
    {"jogo": "São Paulo vs Athletico-PR", "liga": "Brasileirão Série A", "esporte": "Futebol", "horario": "21:30"},

    # --- FUTEBOL: COPA SUL-AMERICANA ---
    {"jogo": "Independiente Medellín vs Vasco", "liga": "Copa Sul-Americana", "esporte": "Futebol", "horario": "19:00"},
    {"jogo": "Lanús vs Cienciano", "liga": "Copa Sul-Americana", "esporte": "Futebol", "horario": "21:30"},
    {"jogo": "Sporting Cristal vs RB Bragantino", "liga": "Copa Sul-Americana", "esporte": "Futebol", "horario": "21:30"},

    # --- FUTEBOL: BRASILEIRÃO SÉRIE B ---
    {"jogo": "Ceará vs CRB", "liga": "Brasileirão Série B", "esporte": "Futebol", "horario": "19:30"},
    {"jogo": "Operário-PR vs Ponte Preta", "liga": "Brasileirão Série B", "esporte": "Futebol", "horario": "19:30"},
    {"jogo": "Goiás vs Sport Recife", "liga": "Brasileirão Série B", "esporte": "Futebol", "horario": "20:30"},
    {"jogo": "Náutico vs Londrina", "liga": "Brasileirão Série B", "esporte": "Futebol", "horario": "21:30"},

    # --- FUTEBOL: UEFA CHAMPIONS LEAGUE (QUALIFICAÇÃO) ---
    {"jogo": "Omonia vs Kairat", "liga": "UEFA Champions League", "esporte": "Futebol", "horario": "14:00"},
    {"jogo": "Levski Sofia vs U. Craiova", "liga": "UEFA Champions League", "esporte": "Futebol", "horario": "14:30"},
    {"jogo": "Egnatia vs Celje", "liga": "UEFA Champions League", "esporte": "Futebol", "horario": "16:00"},

    # --- FUTEBOL: UEFA CONFERENCE LEAGUE (QUALIFICAÇÃO) ---
    {"jogo": "Neftçi vs Dinamo Minsk", "liga": "UEFA Conference League", "esporte": "Futebol", "horario": "13:00"},
    {"jogo": "Bohemian FC vs Ballkani", "liga": "UEFA Conference League", "esporte": "Futebol", "horario": "14:00"},
    {"jogo": "Başakşehir vs Inter", "liga": "UEFA Conference League", "esporte": "Futebol", "horario": "14:45"},
    {"jogo": "Vardar vs Riga", "liga": "UEFA Conference League", "esporte": "Futebol", "horario": "15:00"},

    # --- BASQUETE: WNBA & LIGAS ---
    {"jogo": "Phoenix Mercury @ Los Angeles Sparks", "liga": "WNBA", "esporte": "Basquete", "horario": "16:00"},
    {"jogo": "Minnesota Lynx @ Seattle Storm", "liga": "WNBA", "esporte": "Basquete", "horario": "16:00"},
    {"jogo": "Chicago Sky @ New York Liberty", "liga": "WNBA", "esporte": "Basquete", "horario": "20:00"},
    {"jogo": "Las Vegas Aces @ Washington Mystics", "liga": "WNBA", "esporte": "Basquete", "horario": "20:30"},
    {"jogo": "Connecticut Sun @ Indiana Fever", "liga": "WNBA", "esporte": "Basquete", "horario": "21:00"},
    {"jogo": "Dallas Wings @ Atlanta Fire", "liga": "WNBA", "esporte": "Basquete", "horario": "23:00"},
    {"jogo": "Al Riyadi vs Sagesse SC", "liga": "Lebanese Basketball League", "esporte": "Basquete", "horario": "15:30"},

    # --- BEISEBOL: MLB ---
    {"jogo": "Pittsburgh Pirates @ New York Yankees", "liga": "MLB", "esporte": "Beisebol", "horario": "14:05"},
    {"jogo": "Baltimore Orioles @ Boston Red Sox", "liga": "MLB", "esporte": "Beisebol", "horario": "14:35"},
    {"jogo": "San Francisco Giants @ Kansas City Royals", "liga": "MLB", "esporte": "Beisebol", "horario": "15:10"},
    {"jogo": "New York Mets @ Milwaukee Brewers", "liga": "MLB", "esporte": "Beisebol", "horario": "15:10"},
    {"jogo": "Washington Nationals @ Colorado Rockies", "liga": "MLB", "esporte": "Beisebol", "horario": "16:10"},
    {"jogo": "Oakland Athletics @ Arizona Diamondbacks", "liga": "MLB", "esporte": "Beisebol", "horario": "16:40"},
    {"jogo": "Cincinnati Reds @ Seattle Mariners", "liga": "MLB", "esporte": "Beisebol", "horario": "16:40"},
    {"jogo": "St. Louis Cardinals @ Los Angeles Angels", "liga": "MLB", "esporte": "Beisebol", "horario": "17:07"},
    {"jogo": "Minnesota Twins @ Cleveland Guardians", "liga": "MLB", "esporte": "Beisebol", "horario": "19:40"},
    {"jogo": "Los Angeles Dodgers @ Philadelphia Phillies", "liga": "MLB", "esporte": "Beisebol", "horario": "19:40"},
    {"jogo": "San Diego Padres @ Atlanta Braves", "liga": "MLB", "esporte": "Beisebol", "horario": "20:15"},
    {"jogo": "Chicago White Sox @ Texas Rangers", "liga": "MLB", "esporte": "Beisebol", "horario": "21:05"},
    {"jogo": "Detroit Tigers @ Chicago Cubs", "liga": "MLB", "esporte": "Beisebol", "horario": "21:10"},
    {"jogo": "Miami Marlins @ Houston Astros", "liga": "MLB", "esporte": "Beisebol", "horario": "21:10"}
]
# ==============================================================================

def analisar_com_gemini(item):
    jogo = item["jogo"]
    liga = item["liga"]
    horario = item["horario"]
    esporte = item["esporte"]

    prompt = f"""
    Atue como um analista estatístico esportivo sênior no padrão SofaScore/Flashscore.
    Analise o confronto de {esporte} agendado para HOJE: {jogo} ({liga} - {horario}).

    Forneça uma análise tática e matemática rigorosa para orientar apostadores.
    Retorne APENAS um JSON estrito no formato abaixo (sem nenhum tipo de texto ou marcadores de bloco markdown):
    {{
      "jogo": "{jogo}",
      "liga": "{liga}",
      "esporte": "{esporte}",
      "horario": "{horario}",
      "prob_casa": 50,
      "prob_empate": 25,
      "prob_fora": 25,
      "clima_e_gramado": "Contexto da quadra/estádio, temperatura e atmosfera para a partida",
      "desfalques_e_escalacao": "Principais destaques/jogadores chave disponíveis e desfalques",
      "historico_e_momento": "Momento recente da equipe e retrospecto direto",
      "palpite_recomendado": "Entrada principal de maior valor tático no esporte",
      "odd_estimada": "1.85",
      "nivel_confianca": "Alta (85%)",
      "resumo_analise": "Justificativa tática bem fundamentada para orientar a aposta"
    }}
    """
    
    delays = [1, 2, 4, 8]
    for delay in delays:
        try:
            response = model.generate_content(prompt)
            txt = response.text.strip()
            
            # Limpeza de marcadores de formato markdown caso existam
            if txt.startswith("

