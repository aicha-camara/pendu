import random
import os

# Constantes
FICHIER_MOTS = "mots.txt"
FICHIER_SCORES_GLOBAUX = "scores_globaux.txt"
MAX_ERREURS = 5
POINTS_FACILE = 10
POINTS_MOYEN = 20
POINTS_DIFFICILE = 30

class Pendu:
    def __init__(self, nom_joueur):
        self.nbr_erreur = 0
        self.lettres_trouvees = ""
        self.nom_joueur = nom_joueur

    def lire_mots(self, fichier):
        mots_faciles, mots_moyens, mots_difficiles = [], [], []

        if os.path.exists(fichier):
            with open(fichier, "r", encoding="utf-8") as file:
                mots = [line.strip() for line in file]

            for mot in mots:
                if len(mot) < 5:
                    mots_faciles.append(mot)
                elif 5 <= len(mot) <= 7:
                    mots_moyens.append(mot)
                elif len(mot) > 7:
                    mots_difficiles.append(mot)

        return mots_faciles, mots_moyens, mots_difficiles

    def generer_mot_aleatoire(self, liste_de_mots):
        return random.choice(liste_de_mots)

    def ajouter_mot(self, mot, fichier):
        with open(fichier, "a", encoding="utf-8") as file:
            file.write("\n" + mot)

    def afficher_mot(self, mot):
        affichage = ""
        for lettre in mot:
            if lettre in self.lettres_trouvees:
                affichage += lettre
            else:
                affichage += "_"
        return affichage

    def ajouter_score(self, points, fichier_scores):
        with open(fichier_scores, "a", encoding="utf-8") as file:
            file.write("{}: {}\n".format(self.nom_joueur, points))

    def ajouter_points(self, points, fichier_scores_globaux):
        scores_globaux = {}

        # Charger les scores existants depuis le fichier
        if os.path.exists(fichier_scores_globaux):
            with open(fichier_scores_globaux, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    # Vérifier que la ligne n'est pas vide et contient exactement un ":"
                    if line.strip() and line.count(":") == 1:
                        nom, score = line.strip().split(": ")
                        scores_globaux[nom] = int(score)

        # Ajouter les nouveaux points (basés sur la difficulté du mot)
        scores_globaux[self.nom_joueur] = scores_globaux.get(self.nom_joueur, 0) + points

        # Réinitialiser le fichier
        with open(fichier_scores_globaux, "w", encoding="utf-8") as file:
            for nom, score in scores_globaux.items():
                file.write("{}: {}\n".format(nom, score))

    def ajouter_utilisateur(self):
        nouveau_nom = input("Entrez le nom du nouvel utilisateur : ")

        # Mettre à jour le nom du joueur actuel
        self.nom_joueur = nouveau_nom

        # Ajouter le nouvel utilisateur au fichier des scores globaux avec un score initial de 0
        with open(FICHIER_SCORES_GLOBAUX, "a", encoding="utf-8") as file:
            file.write("{}: 0\n".format(nouveau_nom))

        print("Le nouvel utilisateur '{}' a été ajouté.".format(nouveau_nom))

    def choisir_difficulte(self):
        print("\nNiveaux de difficulté :")
        print("1. Facile (Mots de moins de 5 lettres)")
        print("2. Moyen (Mots de 5 à 7 lettres)")
        print("3. Difficile (Mots de plus de 7 lettres)")

        choix = input("Choisissez un niveau de difficulté (1/2/3) : ")
        if choix == "1":
            return self.lire_mots(FICHIER_MOTS)[0], POINTS_FACILE
        elif choix == "2":
            return self.lire_mots(FICHIER_MOTS)[1], POINTS_MOYEN
        elif choix == "3":
            return self.lire_mots(FICHIER_MOTS)[2], POINTS_DIFFICILE
        else:
            print("Option invalide. Choisissez une option valide.")
            return self.choisir_difficulte()

    def afficher_scores_globaux(self):
        print("\nScores globaux :")
        with open(FICHIER_SCORES_GLOBAUX, "r", encoding="utf-8") as file:
            scores_globaux = file.readlines()
            for score in scores_globaux:
                print(score.strip())

    def jouer(self):
        print("\nBienvenue sur le pendu")

        mots_disponibles, points_gagnes = self.choisir_difficulte()
        mot_aleatoire = self.generer_mot_aleatoire(mots_disponibles)
        print(self.afficher_mot(mot_aleatoire))

        while True:
            x = input("\nChoisissez une lettre : ").lower()

            if x in mot_aleatoire:
                print("\nVous avez trouvé une lettre : {}".format(x))
                self.lettres_trouvees += x
            else:
                self.nbr_erreur += 1
                print("\nCette lettre ne fait pas partie du mot")

            affichage = self.afficher_mot(mot_aleatoire)
            print("\nMot actuel : {}".format(affichage))

            if set(affichage) == set(mot_aleatoire):
                print("\nFélicitations, vous avez gagné ! Le mot était : {}".format(mot_aleatoire))
                self.ajouter_points(points_gagnes, FICHIER_SCORES_GLOBAUX)
                break

            if self.nbr_erreur >= MAX_ERREURS:
                print("\nVous avez perdu. Le mot était : {}".format(mot_aleatoire))
                break

        rejouer = input("\nVoulez-vous rejouer ? (oui/non) ")
        if rejouer.lower() == "oui":
            self.__init__(self.nom_joueur)  # Réinitialiser les attributs pour une nouvelle partie
            self.jouer()
        else:
            quit()

def main():
    nom_joueur = input("Entrez votre nom : ")
    pendu_game = Pendu(nom_joueur)

    while True:
        print("\nMenu:")
        print("1. Jouer")
        print("2. Afficher les scores globaux")
        print("3. Insérer un mot dans le fichier")
        print("4. Ajouter un nouvel utilisateur")
        print("5. Quitter")

        choix = input("Choisissez une option (1/2/3/4/5) : ")

        if choix == "1":
            pendu_game.jouer()
        elif choix == "2":
            pendu_game.afficher_scores_globaux()
        elif choix == "3":
            nouveau_mot = input("Entrez le nouveau mot : ")
            pendu_game.ajouter_mot(nouveau_mot, FICHIER_MOTS)
            print("Le mot a été ajouté au fichier.")
        elif choix == "4":
            pendu_game.ajouter_utilisateur()
        elif choix == "5":
            quit()
        else:
            print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()
