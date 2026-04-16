import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# ─────────────────────────────────────────
# ÉTAPE 1 : Le modèle
# ─────────────────────────────────────────
llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# ─────────────────────────────────────────
# ÉTAPE 2 : Template avec mémoire
# MessagesPlaceholder = emplacement pour
# l'historique de la conversation
# ─────────────────────────────────────────
template = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant utile qui répond en français."),
    MessagesPlaceholder(variable_name="historique"),
    ("human", "{question}")
])

# ─────────────────────────────────────────
# ÉTAPE 3 : La chain
# ─────────────────────────────────────────
chain = template | llm | StrOutputParser()

# ─────────────────────────────────────────
# ÉTAPE 4 : L'historique
# On garde en mémoire tous les messages
# ─────────────────────────────────────────
historique = []

print("🤖 Chatbot avec mémoire ! (tape 'quit' pour quitter)")
print("="*50)

while True:
    question = input("\n👤 Toi : ")
    
    if question.lower() == "quit":
        break
    
    # Envoie la question avec l'historique
    reponse = chain.invoke({
        "historique": historique,
        "question": question
    })
    
    print(f"\n🤖 Bot : {reponse}")
    
    # Ajoute à l'historique
    historique.append(HumanMessage(content=question))
    historique.append(AIMessage(content=reponse))