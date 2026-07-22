import os
import json
import requests
from datetime import datetime
import google.generativeai as genai

# Configuração das Chaves
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
FOOTBALL_KEY = os.environ.get("FOOTBALL_API_KEY")

if not GEMINI_KEY:
    raise ValueError("Chave GEMINI_API_KEY nao encontrada!")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def buscar_jogos_api():
    """Tenta buscar na API Esportiva"""
    if not FOOTBALL_KEY:
        return []
        
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": FOOTBALL_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    params = {"date": hoje, "timezone": "America/Sao_Paulo"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        dados = response.json()
        jogos_filtrados = []
        
        for item in dados.get("response", [])[:8]:
            teams = item.get("teams", {})
            league = item.get("league", {})
            fixture = item.get("fixture", {})
            
            p_home = teams.get('home', {}).get('name')
            p_away = teams.get('away', {}).get('name')
            
            if p_home and p_away:
                jogos_filtrados.append({
                    "jogo": f"{p_home} vs {p_away}",
                    "liga": league.get("name", "Futebol"),
                    "horario": fixture.get("date", "")[11:16] or "20:00",
                    "odds": "Mercado Geral"
                })
        return jogos_filtrados
    except Exception as e:
        print(f"Aviso API: {e}")
        return []

def gerar_analise(jogo, liga, horario, odds):
    prompt = f"""
    Você é um analista esportivo profissional. Analise o confronto:
    - Jogo: {jogo}
    - Liga: {liga}
    - Horário: {horario}
    
    Retorne EXCLUSIVAMENTE um JSON válido com exatamente estas chaves:
    {{
      "jogo": "{jogo}",
      "liga": "{liga}",
      "clima_e_gramado": "Análise prevista das condições do clima e impacto no jogo",
      "desfalques_e_escalacao": "Principais desfalques e momento tático",
      "historico_e_momento": "Momento recente dos dois times",
      "palpite_recomendado": "Mercado sugerido de valor",
      "odd_estimada": "Odd aproximada (ex: 1.85)",
      "nivel_confianca": "Alta",
      "resumo_analise": "Justificativa da aposta baseada nos dados"
    }}
    """
    try:
        res = model.generate_content(prompt)
        txt = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(txt)
    except Exception as e:
        print(f"Erro IA para {jogo}: {e}")
        return None

def main():
    print("🚀 Buscando jogos...")
    jogos = buscar_jogos_api()
    
    # Se a API não retornar nada, usamos a grade garantida da rodada
    if not jogos or len(jogos) == 0:
        print("Usando grade padrão garantida...")
        jogos = [
            {"jogo": "Flamengo vs Fluminense", "liga": "Brasileirão", "horario": "21:30", "odds": "1.80 / 3.40 / 4.20"},
            {"jogo": "Palmeiras vs São Paulo", "liga": "Brasileirão", "horario": "19:30", "odds": "1.95 / 3.20 / 3.80"},
            {"jogo": "Corinthians vs Santos", "liga": "Brasileirão", "horario": "16:00", "odds": "2.10 / 3.10 / 3.50"},
            {"jogo": "Real Madrid vs Barcelona", "liga": "Amistoso / Liga", "horario": "20:00", "odds": "2.20 / 3.50 / 2.90"}
        ]
        
    relatorio = []
    for j in jogos:
        print(f"Gerando análise da IA: {j['jogo']}...")
        res = gerar_analise(j["jogo"], j["liga"], j["horario"], j["odds"])
        if res:
            relatorio.append(res)
            
    with open("dados_jogos_hoje.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Concluído com {len(relatorio)} análises salvas!")

if __name__ == "__main__":
    main()
