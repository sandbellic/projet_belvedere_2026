

import time

import transformers
from sentence_transformers import SentenceTransformer
transformers.logging.set_verbosity_error()  # masque les avertissements techniques, pour garder un affichage lisible
from sklearn.manifold import TSNE

from projet_belvedere.utils import print_chat, resource_path
from projet_belvedere.embedding_documents import embedding_docs, sources_pdf
from projet_belvedere.rag import answer_question


LLM_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

questions_hotel = [
        "A quelle heure commence le check-in ?",
        "A quelle heure ouvre la réception ?",
        "Le wifi est-il gratuit ?",
        "Combien coute une chambre Classique en basse saison ?",
        "Est-ce que vous acceptez les paiements en Bitcoin ?",
    ]


def main():
    #chargement des modèles de llm et de transformation en vecteurs 
    # pour la génération du llm on crée un pipeline de génération de texte avec le modèle "Qwen/Qwen2.5-0.5B-Instruct" 
    generator = transformers.pipeline("text-generation", model=LLM_MODEL)  
    # Charge le modèle `EMBEDDING_MODEL` avec la classe `SentenceTransformer`, et le stocke dans la variable `embedder`. 
    # (ce modèle va servir à vectoriser les questions et les documents d'entreprise)
    embedder = SentenceTransformer(EMBEDDING_MODEL) 


    # dossier racine du projet_belvedere
    BASE_DIR = resource_path("")  # chemin absolu vers le dossier racine du projet_belvedere

    # on extrait les documents entreprise qui vont nous servir comme contexte dans notre prompt
    pages = sources_pdf(BASE_DIR)
    # et on les encode en vecteurs
    chunks_embedded = embedding_docs(pages, embedder)

    # test du RAG 
    start = time.time()
    for question in questions_hotel:
        answer, sources = answer_question(question, pages, chunks_embedded, embedder, generator)
        print_chat(question, answer, sources)
    print(f"Temps total : {time.time() - start:.0f} secondes pour {len(questions_hotel)} questions")


if __name__ == "__main__":
    main()