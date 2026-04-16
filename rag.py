
import pdfplumber
def lire_pdf(chemin):
    texte = ""
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            texte += page.extract_text() or ""
    return texte
# Charge ton PDF
# Après avoir lu le PDF, ajoute ça
document = lire_pdf("cv_anas.pdf")
print(f"📄 PDF lu ! {len(document)} caractères trouvés")
print(f"Aperçu : {document[:200]}")  # affiche les 200 premiers caractères

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