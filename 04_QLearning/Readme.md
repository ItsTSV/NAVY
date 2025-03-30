# 4. Q-Learning
Pro řešení tohoto problému jsem implementoval vlastní Q-Learning algoritmus a využil jej pro trénování agenta
na prostředí z knihovny Gymnasium. Agenta jsem trénoval pro hru FrozenLake-v1 v deterministické verzi, která má 4 akce 
a 16 možných stavů. Agent se po pár stovkách epizod natrénoval.

Prostředí jsem dále rozšířil na velikost 8x8 a implementoval custom wrapper, který mi dovolil nastavovat
odměny dle vlastního uvážení; odměny jsem tedy nastavil takto:

- Dosažení cíle: +1000 (velká pozitivní odměna, jelikož agent dosáhl cíle)
- Pád do díry: -250 (velká negativní odměna, jelikož agent selhal)
- Krok vpřed: -1 (malá negativní odměna, aby agent zbytečně nebloudil)

Počet kroků jsem omezil na 256; urychlí to trénování, protože se agent nemůže "ztratit".

Implementace je trochu rozšířenější než ta z přednášky.
Agent využívá Q-table pro ukládání Q-values (ty říkají, jak dobré je provést konkrétní akci v daném stavu)
a epsilon-greedy rozhodování, kterým řeší exploration vs. exploitation problém. Tradeoff okamžitých vs. 
budoucích odměn je pak řešen pomocí discount factoru gamma. Agent nevyužívá replay memory, protože by to
při klasickém Q-learningu bez neuronových sítí nejspíš nemělo smysl.

Nutno nainstalovat:
- ```gymnasium```
- ```gymnasium[toy_text]```

![Vysledek](../random_imgs/frozenlake.gif)

![Vysledek](../random_imgs/frozenlake_bigger.gif)