pour lancer le serveur -> uvicorn server:app --reload

acceder au serveur -> http://127.0.0.1:8000/docs#/

// data base utilisateur 


utiliser le "Read User" (en cliquant sur "try out" et "execute") pour voir la base de donnée (à faire a chaque fois pour l'actualiser)

Login.py pour le programme python (se connecter / créer un compte)

et index.html pour le site (meme fonctionnement) 

// data base transaction

utiliser le "Read Transaction" (en cliquant sur "try out" et "execute") pour voir la base de donnée (à faire a chaque fois pour l'actualiser)

transaction.html pour pouvoir créer des transactions

decrypt_db.py pour pouvoir decrypter les transactions 
    - il faut mettre la base de donnée dans un fichier "db.txt", il faut aussi mettre la clef privée dans un fichier "private_key.txt".
    - une DB sera créé sous le nom de "decrypted_db.csv"
    - Après utilisation : supprimer / cacher private_key.txt pour eviter qu'un hackeur la récupère 

//  - Utilisation d'un cryptage assymétrique avec clef privée et publique
//  - utilisation d'un hashage en rapport avec la transaction précedente pour garder un lien entre chaque transaction
//  - logiciel de verification affichant les incohérences et leur emplacement si présente 
// 
// pas de sécurité supplémentaire par rapport au cryptage en chaine car posant trop d'erreurs et ne protège pas d'une réécriture totale des données (ce qui ne le rend donc pas plus éfficace que le cryptage actuel)