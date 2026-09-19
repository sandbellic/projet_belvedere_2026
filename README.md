Projet_Belvedere_2026 est réalisé à partir des mini-projets Data / IA proposés par le site ** Machine Learnia Ltd ** durant l'été 2026.

Guillaume Saint-Cirgue, Fondateur du site et Senior Data Scientist avec plus de 10 ans d’expérience dans les secteurs de la tech, l’aviation, la robotique, l’énergie, et les usines connectées nous fait partager ses connaissances dans le domaine de l’intelligence artificielle.

Au travers de projets partagés, guidés étape par étape, avec des explications claires, il aborde des sujets relatifs :
 * à RAG et LLM - Projet hôtel Belvédère

J'ai réalisé ce projet et ai décidé de le modifier librement en ajoutant mes propres commentaires et codes.

Environnement : 
1 . Utilisation de uv comme outil de gestion de l'environnement de Python : pour créer facilement un environnement virtuel,
décrire le projet et gérer mes dépendances via le fichier pyproject.toml 
2 . Présence d'un folder scripts permettant de générer une version exécutable .exe du projet dans le repertoire dist (simple .exe ou possibilité d'avoir un setup)

********************************************

Dans ce projet, on veut créer un assistant virtuel pour un hotel qui soit capable de répondre aux questions basiques portant sur les services et prestations proposés par l'hotel.

Pour ne pas entâcher la réputation de l'hôtel, l'assistant ne doit pas inventer des choses: promettre un service inexistant, inventer un tarif, ... 

1. **Le LLM tout seul** ne fonctionne pas. 
   En effet, l'utilisation d'un modèle de langage générique n'est pas adapté : il ne connaît rien de l'Hôtel Le Belvédère, il ne peut donc que deviner à partir d'autres données sur lesquelles il a été entraîné, voire halluciner une réponse plausible mais fausse. 
   
2. **Le RAG** (Retrieval-Augmented Generation) est la solution.
   On va donner au modèle un accès à la vraie documentation de l'hôtel. 
   Celle-ci va être transformée en vecteurs de sens (les embeddings). 
   Dans le prompt, pour chaque question, on va fournir au LLM, en contexte, les bonnes rubriques de la documentation par proximité de sens avec la question (ie les informations parmi "les plus pertinentes"). 
   Ainsi le modèle ne lit que l'essentiel, répond plus vite, peut citer ses sources, et sait dire « je ne sais pas ». 


Limites de ce prototype. 
Le modèle de génération n'a que 500 millions de paramètres : c'est minuscule pour un LLM (les modèles de production en comptent des dizaines, voire des centaines de milliards). Il lui arrive donc d'être maladroit, trop prudent, ou de passer à côté d'un détail pourtant présent dans le contexte. 
Avec un modèle plus gros, les deviennent fiables.
Mais globalement on retrouve toujours les mêmes étapes, la partie recherche est solide.
Seule l'échelle change.
Pour un vrai projet : 
* la documentation comptera bien plus que 15 rubriques courtes (on sera plutôt sur des milliers), 
* les données importées seront de différents types : textes, images, vidéos, avec différents formats
* l'étape de chunking nécessitera un découpage des documents longs selon l'une des différentes méthodes : longueurs fixes (caractères ou tokens) avec recoupement, par phrases, par structures (markown), par sens, ...
* et surtout une vraie base de données vectorielle pour enregistrer et retrouver rapidement les vecteurs de sens.


### Pour aller plus loin

Quelques idées à explorer :

- remplacer le tableau `numpy` par une vraie solution de recherche vectorielle comme FAISS ou Chroma, et comparer les temps de recherche sur un corpus bien plus gros
- utiliser un modèle de génération plus costaud (un Qwen plus grand, Mistral, ou une API comme Claude) et comparer la qualité des réponses
- ajouter une vraie étape de chunking : découper des documents longs en morceaux qui se chevauchent, et observer l'effet sur la recherche
- construire un jeu de questions d'évaluation et mesurer le taux de bonnes récupérations (le « recall@k »), comme on évalue un modèle de Machine Learning classique
- construire une vraie interface de chat avec `gradio` ou `streamlit`, et ajouter une mémoire conversationnelle (garder les échanges précédents dans le prompt)