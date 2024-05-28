def calculer_duree_totale(taches):

    total_minutes = 0

    for heures, minutes in taches:
        total_minutes += heures * 60 + minutes

    heures_totales = total_minutes // 60
    minutes_restantes = total_minutes % 60

    return f"Durée totale: {heures_totales} heures et {minutes_restantes} minutes"

if __name__ == "__main__":
    taches = [
        (1, 30),
        (2, 45),
        (0, 50),
        (1, 20) 
    ]
    
    print(calculer_duree_totale(taches))
