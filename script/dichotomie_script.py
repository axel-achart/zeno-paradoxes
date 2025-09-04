# Terminal Version

import time

def dichotomie():
    print("\n- - - Dichotomie Paradox - - -")
    print("\nStart (Rock) : O")
    print("Goal (Tree)  : X\n")

    distance_total = 8.0
    distance_restante = distance_total
    etape = 1

    print("O" + "-" * (50) + "X")
    print("Distance totale : 8.000 m")
    print()
    time.sleep(1.5)

    while distance_restante > 0.01:
        distance_restante = distance_restante / 2
        position = distance_total - distance_restante

        progress = int((position / distance_total) * 50)
        print("-" * progress + "O" + "-" * (50 - progress) + "X")

        print(f"Étape {etape} = distance restante : {distance_restante:.3f} m\n")
        etape += 1
        time.sleep(1.5)

    print("\nLa pierre est (presque) arrivée à l'arbre mais il reste toujours une petite distance !\n")
    print()

dichotomie()