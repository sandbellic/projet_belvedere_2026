from pypdf import PdfReader
from pathlib import Path
import pandas as pd

def _load_pdf(BASE_DIR):
    """
    Liste les fichiers pdf contenus dans le dossier data sous la racine du projet 
    Arguments:
    BASE_DIR -- réertoire racine du projet 
    
    Returns
    pdf_files -- liste des fichiers pdf contenus dans path_data
    """
    path_data = BASE_DIR / "data"

    # p, valide que chemin menant à data existe et que c'est bien un répertoire avant de lire les fichiers qu'il contient
    if not path_data.exists():
        raise ValueError(f"Erreur: le chemin '{path_data}' n'existe .")
    elif not path_data.is_dir():
        raise ValueError(f"Erreur: '{path_data}' n'est pas un répertoire.")
    else:
        # liste tous les fichiers pdf du répertoire
        pdf_files = [f for f in path_data.glob("*.pdf") if f.is_file()]

    if not pdf_files:
        raise ValueError(f"Aucun fichier .pdf trouvé dans '{path_data}.")

    return pdf_files


def _read_pdf_to_dataframe(pdf_files):
    """
    lit le contenu des fichiers pdf, et stocke les informations les lignes d'un dataframe
    Arguments:
    pdf_files -- liste de fichiers pdf 
    Returns:
    pages -- DataFrame contenant pour chaque fichier pdf, les infos extraites des pages (1 row / page)
    """
    rows = []
    for file in pdf_files:
        reader = PdfReader(file)
        for page in reader.pages:
            lines = page.extract_text().split("\n")
            rows.append({
                "source": file.name,             # le fichier PDF d'origine => toujours besoin avec RAG de savoir d'où vient l'information
                "title": lines[0],               # la première ligne de la page est le titre de la rubrique
                "text": "\n".join(lines[1:-1]),  # le texte, sans la ligne de titre ni le pied de page
            })
    #on obtient une liste de dictionnaires, 1 dictionnaire par page extraite (rubrique), avec le nom du fichier source, le titre de la rubrique et le texte de la rubrique
    pages = pd.DataFrame(rows)   # on transforme la liste de dictionnaires en DataFrame pandas 
    # on crée une nouvelle colonne section qui contient le titre et le texte de la rubrique, formaté en markdown    
    pages["section"] = "## " + pages["title"] + "\n\n" + pages["text"]      
    return pages



def sources_pdf(BASE_DIR):
    """
    Arguments:
    BASE_DIR -- répertoire racine du projet 
    Returns:
    pages --
    """
    pdf_files = _load_pdf(BASE_DIR)
    pages = _read_pdf_to_dataframe(pdf_files)
    return pages



def _chunk_pdf(pages):
    """
    Découpage des textes des pages en chunks : 3 méthodes possibles - longueur fixe avec recouvrement, phrases et markdown
    Arguments:
    pages -- DataFrame contenant pour chaque fichier pdf, les infos extraites des pages (1 row / page)
    Returns:
    chunks -- liste des éléments de texte découpés
    """
    # on repart du DataFrame pages, qui contient les 15 rubriques extraites des PDF, et 4 colonnes : source, title, text et section en markdown
    # le découpage en chunk va suivre ici le découpage naturel donné par les sections markdown, 1 chunk par page
    chunks = pages["section"].tolist()  # on récupère la colonne section du DataFrame sous forme de liste
    return chunks


def _embedding_chunks(chunks, embedding_model):
    """
    chaque chunk va être vectorisé selon le modèle embedding_model
    Arguments:
    chunks -- liste des éléments découpés en chunk
    embedding_model -- modèle d'embedding permettant de vectoriser les chunks
    Returns:
    chunk_embedded -- la même liste vectorisée
    """
    # on a un découpage en chunk par section => pour chacun on va créer un embedding (1 par section : dans notre cas 15 embeddings au total)
    # .encode() attend en paramètre une liste de textes, 
    # et renvoie un tableau numpy de vecteurs
    chunk_embedded =  embedding_model.encode(chunks, normalize_embeddings=True)  # on encode la liste des chuncks/sections en vecteurs, normalisés
                        # On passe le paramètre `normalize_embeddings=True` pour que tous les vecteurs aient une longueur de 1
    return chunk_embedded


def embedding_docs(pages, embedding_model):
    """
    Arguments:
    pages -- 
    embedding_model -- modèle d'embedding permettant de vectoriser les chunks
    Returns:
    retrieved_chunks -- chunks vectorisés
    """
    chunks = _chunk_pdf(pages)
    chunks_embedded = _embedding_chunks(chunks, embedding_model)

    return chunks_embedded