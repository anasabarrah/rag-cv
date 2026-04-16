import os
import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ─────────────────────────────────────────
# ÉTAPE 1 : Le modèle
# ─────────────────────────────────────────
llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# ─────────────────────────────────────────
# ÉTAPE 2 : Les outils
# @tool = dit à LangChain que c'est un outil
# que l'agent peut utiliser
# ─────────────────────────────────────────
@tool
def meteo(ville: str) -> str:
    """Récupère la météo actuelle d'une ville."""
    reponse = requests.get(f"https://wttr.in/{ville}?format=3")
    return reponse.text

@tool
def calculatrice(expression: str) -> str:
    """Calcule une expression mathématique. Ex: '2 + 2' ou '10 * 5'"""
    try:
        resultat = eval(expression)
        return f"Résultat : {resultat}"
    except:
        return "Expression invalide"

@tool
def info_github(username: str) -> str:
    """Récupère les infos d'un utilisateur GitHub."""
    data = requests.get(f"https://api.github.com/users/{username}").json()
    return f"Nom: {data.get('name')}, Repos: {data.get('public_repos')}, Followers: {data.get('followers')}"

# ─────────────────────────────────────────
# ÉTAPE 3 : Créer l'agent
# On lui donne les outils disponibles
# Il décide SEUL lequel utiliser
# ─────────────────────────────────────────
outils = [meteo, calculatrice, info_github]
agent = create_react_agent(llm, outils)

# ─────────────────────────────────────────
# ÉTAPE 4 : Tester l'agent
# ─────────────────────────────────────────
print("🤖 Agent LangChain prêt !")
print("="*50)

questions = [
    "Quelle est la météo à Bordeaux ?",
    "Combien fait 15 * 8 + 42 ?",
    "Donne-moi les infos GitHub de anasabarrah"
]

for question in questions:
    print(f"\n❓ Question : {question}")
    reponse = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    print(f"✅ Réponse : {reponse['messages'][-1].content}")
    