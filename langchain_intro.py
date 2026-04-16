# ─────────────────────────────────────────
# LANGCHAIN INTRO — Les concepts de base
# ─────────────────────────────────────────

import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# ─────────────────────────────────────────
# ÉTAPE 1 : Créer le modèle LLM
# C'est comme créer le client Groq
# mais avec LangChain qui gère tout
# ─────────────────────────────────────────
llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# ─────────────────────────────────────────
# ÉTAPE 2 : Envoyer des messages
# SystemMessage = instructions secrètes
# HumanMessage = message de l'utilisateur
# ─────────────────────────────────────────
messages = [
    SystemMessage(content="Tu es un assistant expert en Python qui répond en français."),
    HumanMessage(content="Explique-moi c'est quoi une liste en Python en 2 phrases.")
]

reponse = llm.invoke(messages)

print("✅ Réponse :")
print(reponse.content)

# ─────────────────────────────────────────
# ÉTAPE 3 : Prompt Templates
# Au lieu d'écrire les messages à la main
# on crée des templates réutilisables
# ─────────────────────────────────────────
from langchain_core.prompts import ChatPromptTemplate

# Template avec variable {sujet}
template = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert en programmation qui répond en français."),
    ("human", "Explique-moi {sujet} en 2 phrases simples.")
])

# On remplit le template avec une valeur
prompt = template.invoke({"sujet": "les dictionnaires Python"})
reponse2 = llm.invoke(prompt)

print("\n✅ Réponse avec template :")
print(reponse2.content)

# ─────────────────────────────────────────
# ÉTAPE 4 : Chains (chaînes)
# C'est le coeur de LangChain !
# On connecte template → llm → output
# avec le symbole |
# ─────────────────────────────────────────
from langchain_core.output_parsers import StrOutputParser

# Chain = template | llm | parser
chain = template | llm | StrOutputParser()

# On invoque la chain directement
reponse3 = chain.invoke({"sujet": "les fonctions Python"})

print("\n✅ Réponse avec Chain :")
print(reponse3)