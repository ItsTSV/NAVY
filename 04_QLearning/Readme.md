# 4. Q-Learning
Pro řešení tohoto problému jsem implementoval vlastní Q-Learning algoritmus a využil jej pro trénování agenta
na prostředí z knihovny Gymnasium. Agenta jsem trénoval pro hru FrozenLake-v1 v deterministické verzi, která má 4 akce 
a 16 možných stavů. Agent se po pár stovkách epizod natrénoval. Použití pokročilejších technik, jako je paměť,
by zřejmě bylo v kombinaci s Q-table zbytečné -- k tomu by byla vhodná spíše neuronová síť DQN.

Nutno nainstalovat:
- ```gymnasium```
- ```gymnasium[toy_text]```

![Vysledek](../random_imgs/frozenlake.gif)