import os
import json
import google.generativeai as genai

# Configuração da API do Gemini via variável de ambiente segura
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise ValueError("Chave GEMINI_API_KEY não encontrada nas configurações!")

genai.configure(api_key=GEMINI_KEY)

# Modelo utilizado para análises rápidas e eficientes
model = genai.GenerativeModel('gemini-1.5-flash')

def gerar_analise_profunda_do_jogo(jogo, liga, horario, odds_base):
    """
    Função que solicita à IA uma análise minuciosa com fatores externos
    (clima, desfalques, estado do gramado, momento tático).
    """
    prompt = f"""
    Você é um analista profissional de apostas esportivas e estatístico sênior.
    Analise o seguinte confronto para hoje de forma extremamente aprofundada:
    
    - Partida: {jogo}
    - Liga/Campeonato: {liga}
    - Horário: {horario}
    - Odds de Referência: {odds_base}
    
    Crie um relatório completo estruturado exatamente em formato JSON com as seguintes chaves:
    {{
      "jogo": "{jogo}",
      "liga": "{liga}",
      "clima_e_gramado": "Detalhamento das condições climáticas previstas (chuva, vento, temperatura) e o impacto direto no ritmo do jogo ou tendência de gols",
      "desfalques_e_escalacao": "Análise de desfalques importantes, peças-chave e como isso afeta a tática dos times",
      "historico_e_momento": "Momento recente das equipes, sequência de resultados e retrospecto direto",
      "palpite_recomendado": "Nome do mercado específico recomendado (ex: Flamengo ML, Ambas Marcam Não, Under 2.5)",
      "odd_estimada": "Cotação estimada do palpite (ex: 1.85)",
      "nivel_confianca": "Alta, Média ou Ousada",
      "stake_sugerida_reais": "Valor em R$ recomendado para este jogo baseado numa banca de R$ 550 com objetivo de R$ 1.700",
      "resumo_analise": "Justificativa tática e minuciosa conectando clima + desfalques + estatística para provar o valor do palpite"
    }}
    
    Responda EXCLUSIVAMENTE o código JSON válido, sem texto explicativo adicional fora do JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpa possíveis formatações de markdown na resposta da IA
        texto_limpo = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(texto_limpo)
    except Exception as e:
        print(f"Erro ao processar análise para {jogo}: {e}")
        return None

def main():
    print("🚀 Iniciando o Robô de Análise Esportiva Profunda...")
    
    # Exemplo de grade diária (Na Fase 2, estes jogos virão automaticamente da API da Betano/Flashscore)
    jogos_hoje = [
        {"jogo": "Flamengo vs Chapecoense", "liga": "Brasileirão Série A", "horario": "21:30", "odds": "Fla 1.55 / Empate 3.80 / Chape 6.50"},
        {"jogo": "Coritiba vs Palmeiras", "liga": "Brasileirão Série A", "horario": "19:30", "odds": "Coxa 3.60 / Empate 3.40 / Verdão 2.10"},
        {"jogo": "Ind. Medellín vs Vasco", "liga": "Copa Sul-Americana", "horario": "19:00", "odds": "DIM 2.10 / Empate 3.20 / Vasco 3.50"}
    ]
    
    relatorio_diario = []
    
    for partida in jogos_hoje:
        print(f"🔍 Analisando: {partida['jogo']}...")
        analise = gerar_analise_profunda_do_jogo(
            jogo=partida["jogo"],
            liga=partida["liga"],
            horario=partida["horario"],
            odds_base=partida["odds"]
        )
        if analise:
            relatorio_diario.append(analise)
            
    # Salva o arquivo JSON com todas as análises prontas para o site consumir
    with open("dados_jogos_hoje.json", "w", encoding="utf-8") as f:
        json.dump(relatorio_diario, f, ensure_ascii=False, indent=2)
        
    print("✅ Relatório de análises gerado com sucesso em 'dados_jogos_hoje.json'!")

if __name__ == "__main__":
    main()
