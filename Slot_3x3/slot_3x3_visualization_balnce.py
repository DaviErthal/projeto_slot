import random
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# --- GAME CONFIGURATION (from your optimized results) ---

##### Configuração do Tigrinho
GAME_CONFIG = {
    'symbols': ['W', 'B', 'T', 'O', 'C', 'S', 'L'],
    'weights': [3, 1, 10, 21, 5, 26, 15],
    'paytable': {
        'W': 250, 'B': 100, 'T': 25, 'O': 15, 'C': 10, 'S': 8, 'L': 6,
    }
}

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
def run_player_simulations(config, num_players, max_spins, initial_balance):
    """
    Simulates multiple players, each with a unique 'cash-out' strategy,
    and calculates the total house profit.
    """
    print("Running simulations with player strategies...")
    start_time = time.time()
    
    machine = SlotMachine3x3(config)
    all_player_histories = []
    bet_per_spin = len(machine.paylines) * 1  # Assuming $1 per line
    
    winners = 0
    bankrupts = 0
    # NEW: Variable to track the house's earnings
    house_net_profit = 0.0

    for i in range(num_players):
        balance = initial_balance
        history = [balance]
        
        target_balance = initial_balance * random.uniform(1.5, 3.0)

        for _ in range(max_spins):
            if balance < bet_per_spin:
                # NEW: Player goes bankrupt, house keeps the initial deposit
                house_net_profit += initial_balance
                balance = 0
                bankrupts += 1
                break
            
            if balance >= target_balance:
                # NEW: Player wins, house pays out the player's profit
                player_profit = balance - initial_balance
                house_net_profit -= player_profit
                winners += 1
                break

            balance -= bet_per_spin
            grid = machine.spin()
            win = machine.calculate_wins(grid)
            balance += win
            history.append(balance)
        
        final_balance = history[-1]
        while len(history) < max_spins + 1:
            history.append(final_balance)
            
        all_player_histories.append(history)
        
    duration = time.time() - start_time
    print(f"Simulation completed in {duration:.2f} seconds.")
    print(f"--- Outcome Summary ---")
    print(f"Players who hit their target: {winners}")
    print(f"Players who went bankrupt:    {bankrupts}")
    print(f"Total House Net Profit:       ${house_net_profit:,.2f}")
    
    return all_player_histories

# --- VISUALIZATION LOGIC ---
def plot_histories(histories, max_spins):
    """Uses matplotlib to plot the balance histories of all players."""
    print("Generating plot...")
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 7))

    for history in histories:
        if history[-1] > history[0]:
             ax.plot(history, linewidth=1, alpha=0.8, color='lime')
        elif history[-1] <= 0:
             ax.plot(history, linewidth=1, alpha=0.6, color='red')
        else:
             ax.plot(history, linewidth=1, alpha=0.6, color='gray')

    ax.set_title(f'Player Balance Over Time with Strategies ({len(histories)} Players)', fontsize=16)
    ax.set_xlabel('Number of Spins', fontsize=12)
    ax.set_ylabel('Balance ($)', fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
    ax.set_xlim(0, max_spins)
    ax.set_ylim(bottom=0)

    plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # --- Simulation Settings ---
    NUM_PLAYERS = 500
    MAX_SPINS_PER_PLAYER = 10000
    INITIAL_BALANCE = 2500
    
    player_data = run_player_simulations(
        config=GAME_CONFIG,
        num_players=NUM_PLAYERS,
        max_spins=MAX_SPINS_PER_PLAYER,
        initial_balance=INITIAL_BALANCE
    )
    
    plot_histories(player_data, MAX_SPINS_PER_PLAYER)