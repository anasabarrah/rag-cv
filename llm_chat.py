import os
import pdfplumber
from groq import Groq

# ─────────────────────────────────────────
# ÉTAPE 1 : Connexion au LLM
# ─────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─────────────────────────────────────────
# ÉTAPE 2 : Lire le PDF
# ─────────────────────────────────────────
def lire_pdf(chemin):
    texte = ""
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            texte += page.extract_text() or ""
    return texte

document = lire_pdf("cv_anas.pdf")
print(f"📄 PDF lu ! {len(document)} caractères trouvés")

# ─────────────────────────────────────────
# ÉTAPE 3 : La fonction RAG
# ─────────────────────────────────────────
def rag(question):
    prompt = f"""
Tu es un assistant qui répond UNIQUEMENT en utilisant le contexte fourni.
Si la réponse n'est pas dans le contexte, dis "Je ne sais pas".

CONTEXTE :
{document}

QUESTION : {question}

RÉPONSE :
"""
    reponse = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return reponse.choices[0].message.content

# ─────────────────────────────────────────
# ÉTAPE 4 : Interface interactive
# ─────────────────────────────────────────
print("\n🤖 RAG Bot prêt ! Pose des questions sur ton CV !")
print("(tape 'quit' pour quitter)")
print("="*50)

while True:
    question = input("\n❓ Ta question : ")
    if question.lower() == "quit":
        print("👋 Au revoir !")
        break
    print("\n🔍 Recherche dans le CV...")
    reponse = rag(question)
    print(f"\n✅ Réponse : {reponse}")