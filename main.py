import os
import json
import requests
from datetime import datetime
import google.generativeai as genai

# Configuração das Chaves
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
FOOTBALL_KEY = os.environ.get("FOOTBALL_API_KEY")

if not GEMINI_KEY or not FOOTBALL_KEY:
    raise ValueError("Chaves GEMINI_API_KEY ou FOOTBALL_API_KEY nao encontradas!")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def buscar_jogos_do_dia():
    """
    Busca os jogos do dia atual na API Esportiva
    """
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Exemplo buscando ligas principais (Brasileirão = 71, Libertadores = 13, Sul-Americana = 11)
    headers = {
        "X-RapidAPI-Key": FOOTBALL_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    # Consulta os jogos agendados para hoje
    params = {"date": hoje, "timezone": "America/Sao_Paulo"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        dados = response.json()
        
        jogos_filtrados = []
        for item in dados.get("response", [])[:10]:  # Limita aos 10 primeiros jogos do dia
            fixture = item.get("fixture", {})
            league = item.get("league", {})
            teams = item.get("teams", {})
            
            nome_jogo = f"{teams.get('home', {}).get('name')} vs {teams.get('away', {}).get('name')}"
            nome_liga = league.get("name")
            horario = fixture.get("date", "")[11:16] # Extrai apenas Hora:Minuto
            
            jogos_filtrados.append({
                "jogo": nome_jogo,
                "liga": nome_liga,
                "horario": horario,
                "odds": "Odds de mercado em tempo real"
            })
            
        return jogos_filtrados
    except Exception as e:
        print(f"Erro ao buscar jogos na API: {e}")
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
      "clima_e_gramado": "Análise prevista das condições do clima/gramado para este jogo hoje e como afeta a tendência de gols",
      "desfalques_e_escalacao": "Principais desfalques recentes e contexto tático das equipes",
      "historico_e_momento": "Fase recente e histórico direto das equipes",
      "palpite_recomendado": "Mercado sugerido para aposta de valor",
      "odd_estimada": "Odd aproximada para este mercado (ex: 1.85)",
      "nivel_confianca": "Alta, Média ou Muito Alto",
      "resumo_analise": "Justificativa tática aprofundada baseada em momento e estatística"
    }}
    """
    try:
        res = model.generate_content(prompt)
        txt = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(txt)
    except Exception as e:
        print(f"Erro ao analisar {jogo}: {e}")
        return None

def main():
    print("🚀 Buscando lista de jogos de hoje na API Esportiva...")
    jogos = buscar_jogos_do_dia()
    
    if not jogos:
        print("Nenhum jogo encontrado para hoje ou limite da API atingido. Usando dados de segurança.")
        jogos = [
            {"jogo": "Flamengo vs Fluminense", "liga": "Brasileirão", "horario": "20:00", "odds": "1.90 / 3.40 / 3.80"}
        ]
        
    relatorio = []
    for j in jogos:
        print(f"Gerando análise da IA para: {j['jogo']}...")
        res = gerar_analise(j["jogo"], j["liga"], j["horario"], j["odds"])
        if res:
            relatorio.append(res)
            
    with open("dados_jogos_hoje.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
        
    print("✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
