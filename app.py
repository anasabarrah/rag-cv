import os
import pdfplumber
from groq import Groq
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# ─────────────────────────────────────────
# ÉTAPE 1 : Setup
# ─────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = FastAPI()

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
print(f"📄 PDF lu ! {len(document)} caractères")

# ─────────────────────────────────────────
# ÉTAPE 3 : Fonction RAG
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
# ÉTAPE 4 : Interface web HTML
# ─────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def interface():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAG Bot - CV Anas</title>
        <style>
            body { font-family: Arial; max-width: 700px; margin: 50px auto; padding: 20px; }
            h1 { color: #1a3a5c; }
            input { width: 80%; padding: 10px; font-size: 16px; border: 2px solid #1a3a5c; border-radius: 5px; }
            button { padding: 10px 20px; background: #1a3a5c; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            #reponse { margin-top: 20px; padding: 15px; background: #e8f1f8; border-radius: 5px; min-height: 50px; }
            .loading { color: gray; font-style: italic; }
        </style>
    </head>
    <body>
        <h1>🤖 RAG Bot — CV Anas Abarrah</h1>
        <p>Pose des questions sur le CV d'Anas !</p>
        
        <input type="text" id="question" placeholder="Ex: Quelles sont ses compétences ?" />
        <button onclick="poser()">Envoyer</button>
        
        <div id="reponse">La réponse apparaîtra ici...</div>
        
        <script>
            async function poser() {
                const question = document.getElementById('question').value;
                const div = document.getElementById('reponse');
                
                div.innerHTML = '<span class="loading">🔍 Recherche en cours...</span>';
                
                const res = await fetch('/question', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: question})
                });
                
                const data = await res.json();
                div.innerHTML = '✅ ' + data.reponse;
            }
            
            // Envoyer avec la touche Entrée
            document.getElementById('question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') poser();
            });
        </script>
    </body>
    </html>
    """

# ─────────────────────────────────────────
# ÉTAPE 5 : Endpoint API pour les questions
# ─────────────────────────────────────────
class Question(BaseModel):
    question: str

@app.post("/question")
def repondre(q: Question):
    reponse = rag(q.question)
    return {"reponse": reponse}