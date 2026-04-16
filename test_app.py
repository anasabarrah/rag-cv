# Tests simples pour notre app RAG
import pytest

def test_addition():
    assert 2 + 2 == 4

def test_chaine_string():
    texte = "Anas Abarrah"
    assert "Anas" in texte
    assert len(texte) > 0

def test_dictionnaire():
    data = {"nom": "Anas", "ville": "Talence"}
    assert data["nom"] == "Anas"
    assert data["ville"] == "Talence"

def test_liste():
    competences = ["Python", "JavaScript", "C"]
    assert len(competences) == 3
    assert "Python" in competences