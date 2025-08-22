import random
import time
import copy

# --- SLOT MACHINE ENGINE (from previous script) ---
# This part remains unchanged as it's the core of the simulation.
class SlotMachine3x3:
    """
    A non-interactive, high-performance version of the 3x3 slot machine
    engine, optimized for running simulations.
    """
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

# --- SIMULATION FUNCTION (from previous script) ---
def run_simulation(config, num_spins, quiet=False):
    """Runs a Monte Carlo simulation for a given game configuration."""
    if not quiet:
        print(f"--- Testing Config: weights={config['weights']} ---")
    
    machine = SlotMachine3x3(config)
    total_won = 0
    total_bet_per_spin = len(machine.paylines) # Bet per line is 1
    total_wagered = total_bet_per_spin * num_spins
    
    for _ in range(num_spins):
        total_won += machine.calculate_wins(machine.spin())
        
    empirical_rtp = total_won / total_wagered if total_wagered > 0 else 0
    
    if not quiet:
        print(f"Result: Empirical RTP = {empirical_rtp:.4%}\n")
        
    return empirical_rtp

# --- NEW: OPTIMIZER LOGIC ---
def generate_random_config(base_config):
    """
    Generates a new game configuration by randomly adjusting the weights.
    We keep the paytable constant and only search for the right weights.
    """
    new_config = copy.deepcopy(base_config)
    new_weights = []
    
    # Generate new random weights within a reasonable range
    # These ranges can be tuned to guide the search
    for symbol in new_config['symbols']:
        if symbol == 'W': # Wild should be the rarest
            new_weights.append(random.randint(1, 5))
        elif symbol == 'B':
            new_weights.append(random.randint(3, 10))
        elif symbol == 'T':
            new_weights.append(random.randint(5, 15))
        else: # Common symbols
            new_weights.append(random.randint(15, 30))
            
    new_config['weights'] = new_weights
    return new_config

def find_optimal_config(base_config, target_rtp, tolerance, max_attempts, spins_per_attempt):
    """
    The main optimizer loop that searches for a configuration with the desired RTP.
    """
    print("--- Starting RTP Optimizer ---")
    print(f"Target RTP: {target_rtp:.2%}")
    print(f"Tolerance: +/- {tolerance:.2%}")
    print(f"Spins per attempt: {spins_per_attempt:,}")
    print("-" * 30)
    
    best_config = None
    best_rtp = 0
    
    for i in range(max_attempts):
        print(f"Attempt #{i + 1}/{max_attempts}")
        
        # 1. Generate a new random configuration
        current_config = generate_random_config(base_config)
        
        # 2. Run a simulation to get its RTP
        current_rtp = run_simulation(current_config, spins_per_attempt, quiet=True)
        
        print(f"  Weights: {current_config['weights']} -> RTP: {current_rtp:.4%}")
        
        # 3. Check if we found a winner
        if abs(current_rtp - target_rtp) < tolerance:
            print("\n--- SUCCESS! ---")
            print(f"Found a configuration within the target range after {i + 1} attempts.")
            print(f"Final RTP: {current_rtp:.4%}")
            print(f"Optimal Weights: {current_config['weights']}")
            print("Running a full, high-accuracy simulation on this config...")
            run_simulation(current_config, spins_per_attempt * 10) # Run a longer test
            return current_config
            
        # Keep track of the best result so far
        if abs(current_rtp - target_rtp) < abs(best_rtp - target_rtp):
            best_rtp = current_rtp
            best_config = current_config

    print("\n--- Optimizer Finished ---")
    print(f"Could not find a perfect match after {max_attempts} attempts.")
    print(f"The closest RTP found was: {best_rtp:.4%}")
    print(f"With weights: {best_config['weights']}")
    return best_config

if __name__ == "__main__":
    # The base configuration. We will keep the paytable fixed.
    BASE_GAME_CONFIG = {
        'symbols': ['W', 'B', 'T', 'O', 'C', 'S','L'],
        'weights': [], # Weights will be generated by the optimizer
        'paytable': {
            'W': 250, 'B': 100, 'T': 25, 'O': 10, 'C': 8, 'S': 5, 'L': 3,
        }
    }
    
    # --- Optimizer Settings ---
    TARGET_RTP = 0.96  # 96%
    TOLERANCE = 0.005  # +/- 0.5% (i.e., find between 95.5% and 96.5%)
    MAX_ATTEMPTS = 100 # How many different configurations to try
    SPINS_PER_ATTEMPT = 1_000_000 # Use 1M for speed, then confirm with 10M

    find_optimal_config(BASE_GAME_CONFIG, TARGET_RTP, TOLERANCE, MAX_ATTEMPTS, SPINS_PER_ATTEMPT)
