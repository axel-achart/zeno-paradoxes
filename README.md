# Zénon Paradoxes

Ce dépôt propose trois simulations Pygame illustrant visuellement les célèbres paradoxes de Zénon d'Élée :
- **Achille et la tortue**
- **La dichotomie**
- **La flèche en vol**</br>
Un menu principal permet de choisir la simulation à lancer, ainsi qu’un mode pédagogique “Zénon” pour visualiser le raisonnement du mouvement pas à pas.

---

### Simulations disponibles

#### 1. Achille et la tortue

Montre le déplacement d’Achille vers une tortue en figure statique.
Paradoxe théorique : la tortue est toujours devant, mais en temps réel, Achille la rattrape.

#### 2. La dichotomie

La pierre parcourt d’abord la moitié d’un segment, puis la moitié de la distance restante, etc. Théoriquement, il y a une infinité de “demi-distances”, mais la somme converge concrètement.

#### 3. La flèche en vol

Montre la trajectoire d’une flèche lancée, vue en pas à pas : à chaque instant, la flèche est fixe (posé du mouvement), mais l’enchaînement discret produit un déplacement. Un mode “Zénon” te permet de visualiser Δs, Δt, et la vitesse instantanée pour chaque intervalle discret.

### Détails des paradoxes

#### Achille & la tortue

Programme Python qui simule la course entre Achille et la tortue.

- Positions d'Achille et de la tortue
- Calcul des distances à parcourir
- Interface graphique qui présente le paradoxe

Idée : À chaque étape, Achille atteint l’endroit où se trouvait la tortue, mais celle-ci a déjà avancé. On obtient une somme infinie de distances.

Résolution : En réalité, cette somme infinie converge. On calcule le moment exact où Achille rattrape puis dépasse la tortue.

#### Dichotomie

Programme Python qui illustre le parcours d’un segment en le divisant en moitiés successives.

- Simulation étape par étape
- Visualisation graphique de la progression

Idée : Pour atteindre un point, il faut d’abord parcourir la moitié du chemin, puis la moitié de ce qui reste… On obtient une infinité d’étapes.

Résolution : La somme des moitiés (1/2 + 1/4 + 1/8 + …) converge vers 1. Un déplacement fini peut résulter d’une infinité d’étapes théoriques.

#### Flèche en vol

Programme Python (avec Pygame) qui simule la trajectoire d’une flèche lancée.

- Vitesse initiale et angle de tir
- Gravité et déplacement par petits intervalles de temps
- Position affichée à chaque instant
- Interface avec un mode Zénon : pas à pas (Δt)

Idée : À tout instant, la flèche occupe une position précise et est immobile. Donc, si le temps est une suite d’instants, la flèche ne devrait jamais bouger.

Résolution : Le mouvement existe car c’est l’enchaînement des instants qui crée le déplacement. Le calcul différentiel permet de définir une vitesse instantanée non nulle, même si chaque photo isolée montre une flèche figée.

---

# Zeno Paradoxes (English)

This repository offers three Pygame simulations visually illustrating the famous paradoxes of Zeno of Elea:

- **Achilles and the Tortoise**
- **The Dichotomy**
- **The Arrow in Flight**

A main menu lets you choose which simulation to launch, and a pedagogical “Zeno mode” highlights the step-by-step reasoning of motion.

---

### Available Simulations

#### 1. Achilles and the Tortoise

Shows Achilles moving towards a static tortoise.
Theoretical paradox: the tortoise is always ahead, but in real time, Achilles catches up.

#### 2. The Dichotomy

The rock first covers half a segment, then half the remaining distance, etc. Theoretically, there are infinitely many “half-distances”, but the sum converges in practice.

#### 3. The Arrow in Flight

Shows the trajectory of a launched arrow, step by step: at each instant, the arrow is fixed (motion posed), but the discrete sequence produces movement. A “Zeno mode” lets you visualize Δs, Δt, and instantaneous speed for each discrete interval.

### Paradox Details

#### Achilles & the Tortoise

Python program simulating the race between Achilles and the tortoise.

- Positions of Achilles and the tortoise
- Calculation of distances to cover
- Graphical interface presenting the paradox

Idea: At each step, Achilles reaches the spot where the tortoise was, but the tortoise has already moved forward. This produces an infinite sum of distances.

Resolution: In reality, this infinite sum converges. The exact moment when Achilles catches up and overtakes the tortoise is calculated.

#### The Dichotomy

Python program illustrating the traversal of a segment by successive halvings.

- Step-by-step simulation
- Graphical visualization of progression

Idea: To reach a point, you must first cover half the distance, then half of what remains… This produces an infinite sequence of steps.

Resolution: The sum of halves (1/2 + 1/4 + 1/8 + …) converges to 1. A finite movement can result from an infinite number of theoretical steps.

#### Arrow in Flight

Python program (with Pygame) simulating the trajectory of a launched arrow.

- Initial speed and launch angle
- Gravity and movement by small time intervals
- Position displayed at each instant
- Interface with Zeno mode: step by step (Δt)

Idea: At every instant, the arrow occupies a precise position and is motionless. So, if time is a sequence of instants, the arrow should never move.

Resolution: Movement exists because it’s the succession of instants that creates displacement. Differential calculus allows us to define a non-zero instantaneous speed, even if each isolated snapshot shows a still arrow.
