liste = ["""```
________________
|              |
|              |
|              |
|              |
|              |
|              |
________________```
""", """```
________________
|              |
|              |
|              |
|              |
|    /         |
|   /          |
________________```
""",
         """```
________________
|              |
|              |
|              |
|              |
|    /    \\    |
|   /      \\   |
________________```
""",
         """```
________________
|              |
|              |
|              |
|     __|_     |
|    /    \\    |
|   /      \\   |
________________```
""",
         """```
________________
|              |
|       O      |
|       |      |
|     __|_     |
|    /    \\    |
|   /      \\   |
________________```
""", """```
________________
|       |      |
|       O      |
|       |      |
|     __|_     |
|    /    \\    |
|   /      \\   |
________________```
"""]
dictionnaire = {
    "mer": ["bateau", "poisson", "vague", "pelle", "sable", "serviette", "plage", "écume", "océan", "mouiller", "coquillage", "eau", "château", "Bleu", "Jouer", "baigner", "reposer", "seau", "Plonger", "râteau", "Nager", "tamis"],
    "fournitures scolaires": ["stylo", "tracer", "crayon", "souligner", "écrire", "trousse", "colle", "ciseaux", "cahier", "compas", "règle", "livre", "feutre", "dictionnaire", "classeur", "pinceau", "ranger", "rouleau", "gomme", "peinture", "pochette", "colorier", "équerre", "taille-crayon"],
    "badminton": ['filet', 'rebond', 'raquette', 'perdre', 'taper', 'affronter', 'frapper', 'sol', 'déplacer', 'ligne', 'volant', 'échauffement', 'jongler', 'match', 'adversaire', 'tournoi', 'gagner', 'haut', 'service', 'lob', 'terrain', 'lancer', 'renvoyer', 'recevoir'],
    "automne": ['température', 'ramasser', 'froid', 'panier', 'diminuer', 'vent', 'feuille', 'flaque', 'tomber', 'botte', 'couleur', 'châtaigne', 'arbre', 'noisette', 'pluie', 'écureuil', 'forêt', 'bogue', 'Du', 'raisin', 'gland', 'champignon', 'imperméable', 'pomme', 'nature'],
    "etres_vivants": ['groupe', 'espèce', 'observer', 'classification', 'anatomie', 'nageoire', 'relever', 'collection', 'posséder', 'emboîté', 'commun', 'écaille', 'yeux', 'carapace', 'animal', 'membre', 'caractère', 'mamelle', 'partager', 'poil', 'ancêtre', 'plume', 'parenté', 'bouche'],
    "spectacle": ['instrument', 'émouvant', 'scène', 'costume', 'assister', 'histoire', 'regarder', 'salle', 'gradin', 'musique', 'écouter', 'rideau', 'batterie', 'musical', 'drôle', 'étonnant', 'comédien', 'tuba', 'théâtre', 'musicien', 'conte', 'percussion', 'triste', 'spectateur'],
    "les arts plastiques": ['artiste', 'craie', 'dessin', 'gras', 'grasse', 'créer', 'œuvre', 'auteur', 'fusain', 'découper', 'peinture', 'illustrateur', 'palette', 'dessiner', 'peindre', 'papier', 'colorier', 'encre', 'sculpter', 'technique', 'glaise', 'transparent', 'musée', 'médiathèque', 'exposition'],
    "handball": ['collectif', 'point', 'pratiquer', 'gardien', 'main', 'défenseur', 'équipe', 'cage', 'ballon', 'respecter', 'affronter', 'gymnase', 'largeur', 'attaquant', 'respecter', 'remplaçant', 'longueur', 'zone', 'joueur', 'touche', 'rectangulaire', 'manipuler', 'marquer', 'dribbler']
}
if __name__ == '__main__':
    for i in range(len(liste)):
        print(liste[i])
        print(dictionnaire)