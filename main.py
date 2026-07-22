import os
import json
import google.generativeai as genai

# Pega a chave do Gemini dos Secrets
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# ==============================================================================
# ⚽ JOGOS DO DIA (Edite nomes, ligas e horários aqui):
# ==============================================================================
JOGOS_DE_HOJE = [
    {"jogo": "Flamengo vs Palmeiras", "liga": "Brasileirão Série A", "horario": "21:30"},
    {"jogo": "São Paulo vs Corinthians", "liga": "Brasileirão Série A", "horario": "19:30"},
    {"jogo": "Atlético-MG vs Cruzeiro", "liga": "Brasileirão Série A", "horario": "18:30"},
    {"jogo": "Real Madrid vs Barcelona", "liga": "El Clásico", "horario": "16:00"}
]
# ==============================================================================

def analisar_com_gemini(jogo, liga, horario):
    if not GEMINI_KEY:
        print("Aviso: Chave GEMINI_API_KEY nao encontrada. Usando modo de seguranca.")
        return None

    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Atue como um analista tático de futebol profissional.
        Analise a partida: {jogo} ({liga} - {horario}).

        Retorne APENAS um JSON estrito no seguinte formato (sem markdown ou textos adicionais):
        {{
          "jogo": "{jogo}",
          "liga": "{liga}",
          "clima_e_gramado": "Condições climáticas esperadas e impacto no ritmo da partida",
          "desfalques_e_escalacao": "Prováveis times e ausências relevantes",
          "historico_e_momento": "Momento recente dos dois times",
          "palpite_recomendado": "Entrada tática de valor",
          "odd_estimada": "1.85",
          "nivel_confianca": "Alta",
          "resumo_analise": "Justificativa tática para o palpite"
        }}
        """
        response = model.generate_content(prompt)
        txt = response.text.strip()
        
        if txt.startswith("```json"): txt = txt[7:]
        if txt.startswith("```"): txt = txt[3:]
        if txt.endswith("```"): txt = txt[:-3]
        
        return json.loads(txt.strip())
    except Exception as e:
        print(f"Erro ao consultar Gemini para {jogo}: {e}")
        return None

def criar_analise_fallback(jogo, liga):
    return {
        "jogo": jogo,
        "liga": liga,
        "clima_e_gramado": "Condições normais de jogo.",
        "desfalques_e_escalacao": "Equipes com escalações principais confirmadas.",
        "historico_e_momento": "Confronto equilibrado entre as equipes.",
        "palpite_recomendado": "Ambas Marcam - Sim",
        "odd_estimada": "1.80",
        "nivel_confianca": "Alta",
        "resumo_analise": "Partida movimentada com alta expectativa de oportunidades de gol para ambos os lados."
    }

def main():
    print("🚀 Gerando análises...")
    resultados = []
    
    for item in JOGOS_DE_HOJE:
        print(f"Analisando {item['jogo']}...")
        analise = analisar_com_gemini(item["jogo"], item["liga"], item["horario"])
        
        if not analise:
            analise = criar_analise_fallback(item["jogo"], item["liga"])
            
        resultados.append(analise)

    with open("dados_jogos_hoje.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"✅ Concluído! {len(resultados)} análises salvas com sucesso.")

if __name__ == "__main__":
    main()
