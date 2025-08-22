import random
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# --- GAME CONFIGURATION (from your optimized results) ---
GAME_CONFIG = {
    'symbols': ['W', 'B', 'T', 'O', 'C', 'S', 'L'],
    'weights': [4, 4, 9, 22, 27, 18, 23],
    'paytable': {
        'W': 250, 'B': 50, 'T': 25, 'O': 20, 'C': 15, 'S': 12, 'L': 8,
    }
}
##### Configuração do Tigrinho
# GAME_CONFIG = {
#     'symbols': ['W', 'B', 'T', 'O', 'C', 'S', 'L'],
#     'weights': [3, 1, 10, 21, 5, 26, 15],
#     'paytable': {
#         'W': 250, 'B': 100, 'T': 25, 'O': 15, 'C': 10, 'S': 8, 'L': 6,
#     }
# }

# --- SLOT MACHINE ENGINE ---
# This is the same high-performance engine from our optimizer.
class SlotMachine3x3:
    def __init__(self, config):
        self.symbols = config['symbols']
        self.weights = config['weights']
        self.paytable = config['paytable']
        self.reel_strip = self._build_reel_strip()
        self.paylines = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(2, 0), (1, 1), (0, 2)],
        ]

    def _build_reel_strip(self):
        strip = []
        for i, symbol in enumerate(self.symbols):
            strip.extend([symbol] * self.weights[i])
        return strip

    def spin(self):
        grid = [['' for _ in range(3)] for _ in range(3)]
        reel_len = len(self.reel_strip)
        for col in range(3):
            start_index = random.randint(0, reel_len - 1)
            for row in range(3):
                grid[row][col] = self.reel_strip[(start_index + row) % reel_len]
        return grid

    def calculate_wins(self, grid):
        total_win = 0
        for line_coords in self.paylines:
            line_symbols = [grid[r][c] for r, c in line_coords]
            target_symbol = None
            if line_symbols[0] == line_symbols[1] == line_symbols[2]:
                target_symbol = line_symbols[0]
            else:
                non_wilds = [s for s in line_symbols if s != 'W']
                if not non_wilds: target_symbol = 'W'
                elif len(set(non_wilds)) == 1: target_symbol = non_wilds[0]
            if target_symbol in self.paytable: total_win += self.paytable[target_symbol]
        return total_win

# --- SIMULATION LOGIC ---
def run_player_simulations(config, num_players, num_spins, initial_balance):
    """Simulates multiple players and returns their balance histories."""
    print("Running simulations...")
    start_time = time.time()
    
    machine = SlotMachine3x3(config)
    all_player_histories = []
    bet_per_spin = len(machine.paylines) * 1  # Assuming $1 per line

    for i in range(num_players):
        balance = initial_balance
        history = [balance]
        for _ in range(num_spins):
            if balance < bet_per_spin:
                balance = 0  # Player is bankrupt
            else:
                balance -= bet_per_spin
                grid = machine.spin()
                win = machine.calculate_wins(grid)
                balance += win
            history.append(balance)
        all_player_histories.append(history)
        
    duration = time.time() - start_time
    print(f"Simulation for {num_players} players completed in {duration:.2f} seconds.")
    return all_player_histories

# --- VISUALIZATION LOGIC ---
def plot_histories(histories, num_spins):
    """Uses matplotlib to plot the balance histories of all players."""
    print("Generating plot...")
    
    # Setup the plot style
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot each player's history as a line on the graph
    for history in histories:
        ax.plot(history, linewidth=1, alpha=0.7)

    # Formatting the chart
    ax.set_title(f'Player Balance Over Time ({len(histories)} Players)', fontsize=16)
    ax.set_xlabel('Number of Spins', fontsize=12)
    ax.set_ylabel('Balance ($)', fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
    ax.set_xlim(0, num_spins)
    ax.set_ylim(bottom=0) # Start y-axis at 0

    # Show the plot
    plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # --- Simulation Settings ---
    NUM_PLAYERS = 50
    SPINS_PER_PLAYER = 20000
    INITIAL_BALANCE = 500
    
    # 1. Run the simulation to get the data
    player_data = run_player_simulations(
        config=GAME_CONFIG,
        num_players=NUM_PLAYERS,
        num_spins=SPINS_PER_PLAYER,
        initial_balance=INITIAL_BALANCE
    )
    
    # 2. Plot the results
    plot_histories(player_data, SPINS_PER_PLAYER)