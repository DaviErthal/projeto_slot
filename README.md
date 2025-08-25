# Slot Machine Mechanics: A Statistical Deep Dive

This project is a comprehensive exploration into the statistical and mathematical principles that govern slot machine games, inspired by the popular online game "Jogo do Tigrinho". The primary goal is to deconstruct the mechanics of these games from the ground up, moving from theoretical understanding to practical implementation, optimization, and analysis.

Through a series of Python scripts, we build, simulate, and analyze different types of slot machines to understand concepts like Return to Player (RTP), volatility, and player strategy.

## Project Goals

- Understand Core Mechanics: Learn how Random Number Generators (RNG), paytables, and symbol weights combine to create a predictable long-term return.

- Implement from Scratch: Build fully functional slot machine simulators in Python.

- Optimize for RTP: Develop algorithms to automatically adjust game parameters to achieve a desired RTP, mimicking the process of real-world game design.

- Analyze Volatility: Visualize and understand the player experience by simulating thousands of gameplay sessions and plotting their financial journeys.

- Study Player Strategy: Model how different player behaviors (e.g., setting profit goals) impact outcomes and the casino's overall earnings.

## Project Structure

The project is divided into two main parts, each focusing on a different type of slot machine.

`Slot_1x3/`

This directory contains the initial exploration of a classic, single-payline 3-reel slot machine.

- `first_slot_simulation.py`: A script that builds a 3x1 slot machine from a PAR sheet, calculates its theoretical RTP, and runs a Monte Carlo simulation to verify the result.

- `slot_play.py`: An interactive version of the 3x1 slot machine that allows a human player to play the game from the terminal.

`Slot_3x3/`

This directory contains the more advanced 3x3 (9-slot) multi-line video slot, which serves as the primary model for analysis.

- `slot_3x3_play.py`: An interactive game loop for the 3x3 machine, including "Wild" symbol logic.

- `slot_3x3_simulation_1.py`: A high-performance script for running millions of spins on a single game configuration to accurately calculate its empirical RTP.

- `slot_3x3_optimizer_bruteforce.py`: An automated tool that uses a random brute-force search to find a combination of symbol weights that results in a target RTP.

- `slot_3x3_optimizer_hill.py`: A more intelligent optimization tool that uses a Hill Climbing algorithm to efficiently search for a configuration with a target RTP.

- `slot_3x3_visualization_players.py`: The final analysis script. It simulates hundreds of players with different strategies (e.g., cashing out at a profit target) and uses matplotlib to generate a chart visualizing their balance over time. It also calculates the total net profit for the "house".

## How to Use

Prerequisites

1. Python 3: Ensure you have Python 3 installed on your system.

2. Dependencies: Install the required matplotlib library for visualization. On some systems, you may also need to install tkinter.

``` 
# Install matplotlib

pip install matplotlib

# On Debian/Ubuntu, you may need tkinter

sudo apt-get install python3-tk
 ```

Running the Scripts

Navigate to the project's root directory in your terminal and run any of the Python scripts.

```
# Example: Run the interactive 3x3 game

cd Slot_3x3/

python slot_3x3_play.py

# Example: Run the player volatility visualization

python slot_3x3_visualization_players.py
```

## Scripts Description

`slot_3x3_optimizer_hill.py`

This is the core tool for balancing the game. It starts with a base `paytable` and intelligently adjusts the `weights` of the symbols, running a 1-million-spin simulation for each adjustment. It continuously "climbs" towards the configuration that gets the RTP closest to the target (e.g., 96%), providing the final balanced parameters for use in the other scripts.

`slot_3x3_visualization_players.py`

This is the main analysis script. It takes the balanced game configuration and simulates a large number of players (`NUM_PLAYERS`). Each player has a unique strategy: they stop playing if they go bankrupt or if they reach a randomly assigned profit target.

Output:

1. A pop-up chart showing the balance of all players over time. Winning players are highlighted in green, and bankrupt players are in red.

2. A terminal summary detailing:

- The number of players who walked away as winners.

- The number of players who went bankrupt.

- The total net profit for the house across all simulated players.

## Future Work

- Advanced Strategies: Implement more complex player strategies, such as the Martingale system or changing bet sizes based on wins/losses.

- Paytable Optimization: Modify the optimization scripts to adjust the paytable values in addition to the weights.

- Volatility Index: Calculate and display a numerical volatility index for each game configuration, quantifying the game's risk.

- Web Interface: Create a simple web-based interface using a framework like Flask or Streamlit to allow for interactive configuration and visualization.

## Disclaimer

 This project is for educational and academic purposes only. It is an exercise in statistics, probability, and programming. Online gambling games can be deceptive and lead to financial loss. This project does not endorse or encourage participation in any form of gambling.