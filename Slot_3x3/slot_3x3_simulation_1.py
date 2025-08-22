import random
import time

class SlotMachine3x3:
    """
    A non-interactive, high-performance version of the 3x3 slot machine
    engine, optimized for running simulations.
    """
    def __init__(self, config):
        """Initializes the machine with a given configuration."""
        self.symbols = config['symbols']
        self.weights = config['weights']
        self.paytable = config['paytable']
        self.reel_strip = self._build_reel_strip()
        
        self.paylines = [
            [(0, 0), (0, 1), (0, 2)],  # Top row
            [(1, 0), (1, 1), (1, 2)],  # Middle row
            [(2, 0), (2, 1), (2, 2)],  # Bottom row
            [(0, 0), (1, 1), (2, 2)],  # Diagonal TL-BR
            [(2, 0), (1, 1), (0, 2)],  # Diagonal BL-TR
        ]

    def _build_reel_strip(self):
        """Builds a single, long reel strip based on symbol weights."""
        strip = []
        for i, symbol in enumerate(self.symbols):
            strip.extend([symbol] * self.weights[i])
        # No need to shuffle for simulation, as random.choice handles it
        return strip

    def spin(self):
        """Generates a 3x3 grid of symbols."""
        grid = [['' for _ in range(3)] for _ in range(3)]
        reel_len = len(self.reel_strip)
        for col in range(3):
            start_index = random.randint(0, reel_len - 1)
            for row in range(3):
                symbol_index = (start_index + row) % reel_len
                grid[row][col] = self.reel_strip[symbol_index]
        return grid

    def calculate_wins(self, grid):
        """Calculates the total win for a given grid, including wild logic."""
        total_win = 0
        for line_coords in self.paylines:
            line_symbols = [grid[r][c] for r, c in line_coords]
            
            target_symbol = None
            if line_symbols[0] == line_symbols[1] == line_symbols[2]:
                target_symbol = line_symbols[0]
            else:
                non_wild_symbols = [s for s in line_symbols if s != 'W']
                if not non_wild_symbols:
                    target_symbol = 'W'
                elif len(set(non_wild_symbols)) == 1:
                    target_symbol = non_wild_symbols[0]

            if target_symbol and target_symbol in self.paytable:
                total_win += self.paytable[target_symbol]
        return total_win

def run_simulation(config, num_spins):
    """
    Runs a Monte Carlo simulation for a given game configuration.

    Args:
        config (dict): The game configuration (symbols, weights, paytable).
        num_spins (int): The number of spins to simulate.

    Returns:
        float: The calculated empirical Return to Player (RTP).
    """
    print(f"--- Starting Simulation ---")
    print(f"Configuration: {config['symbols']}")
    print(f"Number of Spins: {num_spins:,}")
    
    start_time = time.time()
    
    machine = SlotMachine3x3(config)
    
    total_won = 0
    bet_per_line = 1
    num_lines = len(machine.paylines)
    total_bet_per_spin = bet_per_line * num_lines
    
    # The main simulation loop
    for _ in range(num_spins):
        grid = machine.spin()
        win_amount = machine.calculate_wins(grid)
        total_won += win_amount
        
    total_wagered = total_bet_per_spin * num_spins
    empirical_rtp = total_won / total_wagered if total_wagered > 0 else 0
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n--- Simulation Results ---")
    print(f"Total Amount Wagered: ${total_wagered:,.2f}")
    print(f"Total Amount Won:     ${total_won:,.2f}")
    print(f"Empirical RTP:        {empirical_rtp:.6%}")
    print(f"Simulation Duration:  {duration:.2f} seconds")
    
    return empirical_rtp

if __name__ == "__main__":
    # The game configuration we want to test
    GAME_CONFIG_TO_TEST = {
        'symbols': ['W', 'B', 'T', 'O', 'C', 'S','L'],
        'weights': [3, 1, 10, 21, 5, 26, 15], 
        'paytable': {
            'W': 250, 'B': 100, 'T': 25, 'O': 15, 'C': 10, 'S': 8, 'L': 6,
        }
    }
    
    # Number of spins for the simulation
    # 10 million is a good number for high accuracy
    SPINS = 10_000_000
    
    run_simulation(GAME_CONFIG_TO_TEST, SPINS)
