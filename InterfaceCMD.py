from Function import Global

def afficher_menu():
    print("\nInterface CMD Basique")
    print("1. Afficher un texte")
    print("2. Addition")
    print("3. Soustraction")
    print("4. Multiplication")
    print("5. Division")
    print("6. Quitter")

def obtenir_entree_utilisateur():
    choix = input("Choisir une option: ")
    return choix

def executer_choix(choix):
    if choix == '1':
        texte = input("Entrez le texte à afficher : ")
        Global.Afficher(texte)
    elif choix == '2':
        a = float(input("Entrez le premier nombre : "))
        b = float(input("Entrez le second nombre : "))
        print(f"Résultat : {Global.Ajouter(a, b)}")
    elif choix == '3':
        a = float(input("Entrez le premier nombre : "))
        b = float(input("Entrez le secondd nombre : "))
        print(f"Résultat : {Global.Soustraire(a, b)}")
    elif choix == '4':
        a = float(input("Entrez le premier nombre : "))
        b = float(input("Entrez le second nombre : "))
        print(f"Résultat : {Global.Multiplier(a, b)}")
    elif choix == '5':
        a = float(input("Entrez le premier nombre : "))
        b = float(input("Entrez le second nombre : "))
        print(f"Résultat : {Global.Diviser(a, b)}")
    elif choix == '6':
        print("Fermeture")
        return False
    else:
        print("Choix non valide. Réessayez : )
    return True

def main():
    print('Interface CMD basique pour naviguer et utiliser des fonctions')
    continuer = True
    while continuer:
        afficher_menu()
        choix = Input()
        continuer = Choix(choix)

if __name__ == "__main__":
    main()