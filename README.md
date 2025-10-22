# Battleship

This is a small terminal-based Python implementation of the popular "Battleship" game. 


## 🌟 Highlights

- Human vs Computer game
- "Smart" Computer player: first random search for ships, then targeting when ship is found
- Distinct player views (two boards)
- Comprehensive test suite using pytest to check game's accuracy.


## ℹ️ Overview

Although I have 6 years of experience using Python (as of October 2025), I have always dealt with statistics and data analysis of big datasets, without ever using object-oriented programming (OOP) in a conscious way. Since OOP is important in the industry world, I wanted to understand its basics and write a small game that features writing classes, the concepts of inheritance, encapsulation and polymorphism. In this sense, Battleship is a perfect and fun example.  

Each feature (ships, boards, players, game) are written as separated classes with their own attributes and methods. Only the Game class wraps everything up and runs the game.


### ✍️ Authors
My name is Vittoria Brugaletta, and I hold a PhD in Computational Astrophysics from the University of Cologne, Germany. 
I have a background in running large-scale HPC simulations, and performing data analysis on large datasets (> 100 Tb) using Python. You can find more information about me on my LinkedIn profile: www.linkedin.com/in/vittoria-brugaletta


## 🚀 Usage

This game has been developed using Python 3.10. To run the game:

```bash
git clone https://github.com/vittoria-brugaletta/Battleship.git
cd Battleship
python3 -m battleship.main
```

To run the tests the package *pytest* (https://docs.pytest.org/en/stable/) is needed. Once you have it installed, you can proceed as:
```bash
cd Battleship
python3 -m pytest -v
```


## 🧭 Future improvements

Some improvements could be added in the future. For example:
- A smarter Computer player (smarter targeting? Some AI player?)
- GUI version instead of printing on the terminal
- Possibility to save the game and resume at a later time
- Multiplayer version, possibly over network.


## 💭 Feedback and Contributing

You can open bugs/feature requests for this project. Any idea to improve the code is welcome! 
