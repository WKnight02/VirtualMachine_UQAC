# #_**TeamPoule** environment._

Bonjour, et merci d'utiliser l'environnement assembleur de la **Team Poule** !

Pour bien commencer, il vous faut une installation valide de `python 3.6+`, incluant les libs suivantes au minimum:
- `sys`
- `tkinter`
- `threading`
- `os` et `os.path`
- `unittest` pour les tests unitaires

Normalement, ces librairies font partie de l'environnement python de base...


## _#**Editeur** assembleur:_

Afin d'écrire / compiler / exécuter des programmes dans notre environnement, il est nécessaire de démarrer notre *éditeur* via le fichier `IDE.py`.

A partir d'ici vous pouvez écrire du code assembleur, l'enregistrer, le compiler, et exécuter des programmes sous forme compilée.

### _...Attention_:

Suite à une erreur de lecture de la spécification, mais aussi suite à ce que l'on pensait être du bon sens, les instructions sur les registres s'écrivent `OP REG1 REG2` et non `OPREG1 REG2`.

Par exemple:
- `ADDA B` devient `ADD A B`
- `STA 0x1547` devient `ST A 0x1547`

## _#**Machine Virtuelle**:_

Afin d'exécuter les programmes `.tpc` *(TeamPouleCompilé)*, vous devez instancier une machine virtuelle, soit depuis le bouton `Exécuter` de l'IDE, soit depuis le script `VM.py` via un invité de commande, avec en paramètre le chemin du fichier `.tpc` à charger et exécuter.

**Exemple:**
- `python VM.py chemin/vers/mon/programme.tpc`

## _#**Architecture** du projet:_

- _`#`**TeamPoule**` environment`_

    - `projet` : Les fichiers / modules du projet

        - _**Sous-packages**_:

            - `components` : Les composants de la machine virtuelle

            - `interfaces` : Les interfaces utilisateur

            - `logic` : Les éléments logiques du projet, principalement la définition des opérations

            - `utilities` : "Boite à outil" de dev, fonctions utiles d'ordre général

        - _**Modules**_:

            - `ArgParser` : Fonctions pratique pour parser les arguments de ligne de commande, nothing fancy...

            - `Compiler` : Les fonctions de compilation

            - `Display` : Fonctions d'affichage d'ordre général

            - `Virtual Machine` : Machine virtuelle pouvant exécuter du code compilé

    - `tests` : Les différents tests, organisés selon la même architecture qu'au sein du dossier `modules`

## _#**Tests**_:

Pour démarrer les tests du projet, il suffit de lancer le fichier `Tests.bat`, ou alors de lancer la commande `python -m unittest discover -p "*test.py"`.

Les tests sont situés dans `projet/tests/*`.
