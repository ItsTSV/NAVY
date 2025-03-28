# 5. Pole balancing problem
Na téma Deep Reinforcement Learningu jsem psal bakalářskou práci, takže se implementace tohoto úkolu
sestávala převážně z vyrabování, zjednodušení a refaktorizace kódu této práce ;) Největší změna
spočívala v zjednodušení architektury DQN, jelikož prostředí CartPole nepracuje s obrazovými, ale
vektorovými daty.

Model jsem nechal trénovat 200 epizod, což stačilo na to, aby se agent naučil hrát hru na docela dobré
úrovni (maximální skóré je 500; toho agent občas dosahoval, při testování se však většinou pohyboval okolo 300).

Pro spuštění je nutno mít pytorch, gym a numpy. Protože instalace torche může být trochu pain, přikládám soubor s 
vahami a výsledný gif jakožto důkaz funkčnosti.

![Vysledek](../random_imgs/cartpole.gif)