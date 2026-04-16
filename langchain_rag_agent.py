import os
import requests
import pdfplumber
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# Charge le CV
def lire_pdf(chemin):
    texte = ""
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            texte += page.extract_text() or ""
    return texte

cv_text = lire_pdf("cv_anas.pdf")

# ─────────────────────────────────────────
# OUTILS SIMPLES — sans RAG dans l'outil
# ─────────────────────────────────────────
@tool
def meteo(ville: str) -> str:
    """Récupère la météo actuelle d'une ville."""
    return requests.get(f"https://wttr.in/{ville}?format=3").text

@tool
def calculatrice(expression: str) -> str:
    """Calcule une expression mathématique comme '2+2' ou '15*8'."""
    try:
        return str(eval(expression))
    except:
        return "Expression invalide"

# Agent SANS outil RAG
agent = create_react_agent(llm, [meteo, calculatrice])

# ─────────────────────────────────────────
# ROUTER — décide si RAG ou Agent
# ─────────────────────────────────────────
def repondre(question):
    mots_cv = ["anas", "cv", "compétence", "formation", 
                "projet", "école", "nom", "langue", "expérience"]
    
    # Si la question parle du CV → RAG direct
    if any(mot in question.lower() for mot in mots_cv):
        prompt = f"""Voici le CV :
{cv_text}

Question : {question}
Réponds en français."""
        reponse = llm.invoke([HumanMessage(content=prompt)])
        return reponse.content
    
    # Sinon → Agent avec outils
    else:
        reponse = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })
        return reponse['messages'][-1].content

# ─────────────────────────────────────────
# INTERFACE
# ─────────────────────────────────────────
print("🤖 Agent RAG prêt !")
print("="*50)

while True:
    question = input("\n❓ Ta question : ")
    if question.lower() == "quit":
        break
    try:
        print(f"\n✅ {repondre(question)}")
    except Exception as e:
        print(f"⚠️ Erreur : {e}")