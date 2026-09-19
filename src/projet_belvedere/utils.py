import sys
from pathlib import Path

def resource_path(relative_path: str) -> Path:
    """
    Retourne le chemin absolu vers une ressource de l'application.

    Fonctionne :
    - en développement avec Python ;
    - avec un exécutable créé par PyInstaller.
    """

    if getattr(sys, "frozen", False):
        # Exécution depuis l'EXE PyInstaller
        base_path = Path(sys._MEIPASS)
    else:
        # Exécution depuis le projet Python
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / relative_path


def print_chat(question, answer, sources=None):
    """Pretty-print one question/answer exchange, with its sources if provided.

    Arguments:
    question -- the user's question, as a string
    answer -- the generated answer, as a string
    sources -- optional DataFrame of retrieved chunks, with columns title and score
    """
    print(f"Client   : {question}")
    if sources is not None:
        titles = ", ".join(f"{row.title} ({row.score:.2f})" for row in sources.itertuples())
        print(f"Sources  : {titles}")
    print(f"Assistant: {answer}")
    print("-" * 80)


