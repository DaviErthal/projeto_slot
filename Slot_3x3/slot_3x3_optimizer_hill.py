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

# --- NEW: OPTIMIZER LOGIC (Hill Climbing) ---
def generate_initial_config(base_config):
    """Generates the first random configuration to start the search."""
    new_config = copy.deepcopy(base_config)
    new_weights = []
    for symbol in new_config['symbols']:
        if symbol == 'W': new_weights.append(random.randint(1, 5))
        elif symbol == 'B': new_weights.append(random.randint(3, 10))
        elif symbol == 'T': new_weights.append(random.randint(5, 15))
        else: new_weights.append(random.randint(15, 30))
    new_config['weights'] = new_weights
    return new_config

def mutate_config(config):
    """
    Creates a 'neighbor' configuration by making a small change to one weight.
    This is the "small step" in our Hill Climbing analogy.
    """
    mutated_config = copy.deepcopy(config)
    # Pick a random weight to change
    index_to_change = random.randint(0, len(mutated_config['weights']) - 1)
    # Add or subtract 1 from the weight
    change = random.choice([-1, 1])
    
    mutated_config['weights'][index_to_change] += change
    # Ensure the weight doesn't fall to 0 or below
    if mutated_config['weights'][index_to_change] < 1:
        mutated_config['weights'][index_to_change] = 1
        
    return mutated_config

def find_optimal_config(base_config, target_rtp, tolerance, max_attempts, spins_per_attempt):
    """
    The main optimizer loop using a Hill Climbing algorithm.
    """
    print("--- Starting RTP Optimizer (Hill Climbing Method) ---")
    print(f"Target RTP: {target_rtp:.2%}")
    print(f"Tolerance: +/- {tolerance:.2%}")
    print(f"Spins per attempt: {spins_per_attempt:,}")
    print("-" * 30)
    
    # 1. Start at a random point on the "hill"
    best_config = generate_initial_config(base_config)
    best_rtp = run_simulation(best_config, spins_per_attempt, quiet=True)
    print(f"Initial Guess: Weights={best_config['weights']} -> RTP: {best_rtp:.4%}")
    
    for i in range(max_attempts):
        # 2. Take a small step to create a "neighbor"
        neighbor_config = mutate_config(best_config)
        
        # 3. Check the neighbor's RTP
        neighbor_rtp = run_simulation(neighbor_config, spins_per_attempt, quiet=True)
        
        # 4. Decide if the step was an improvement
        if abs(neighbor_rtp - target_rtp) < abs(best_rtp - target_rtp):
            best_rtp = neighbor_rtp
            best_config = neighbor_config
            print(f"Attempt #{i + 1}: Improvement! Weights={best_config['weights']} -> RTP: {best_rtp:.4%}")
        else:
            # Optional: print a message for non-improvements to see the process
            # print(f"Attempt #{i + 1}: No improvement.")
            pass

        # 5. Check if we've reached the target
        if abs(best_rtp - target_rtp) < tolerance:
            print("\n--- SUCCESS! ---")
            print(f"Found a configuration within the target range after {i + 1} attempts.")
            print(f"Final RTP: {best_rtp:.4%}")
            print(f"Optimal Weights: {best_config['weights']}")
            print("Running a full, high-accuracy simulation on this config...")
            final_rtp_check = run_simulation(best_config, spins_per_attempt * 10)
            print(f"High-Accuracy RTP Confirmation: {final_rtp_check:.4%}")
            return best_config
            
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
            'W': 250, 'B': 50, 'T': 25, 'O': 20, 'C': 15, 'S': 12, 'L': 8,
        }
    }
    
    # --- Optimizer Settings ---
    TARGET_RTP = 0.96  # 96%
    TOLERANCE = 0.005  # +/- 0.5% (i.e., find between 95.5% and 96.5%)
    MAX_ATTEMPTS = 500 # We can try more attempts now as the search is more efficient
    SPINS_PER_ATTEMPT = 1_000_000 # Use 1M for speed, then confirm with 10M

    find_optimal_config(BASE_GAME_CONFIG, TARGET_RTP, TOLERANCE, MAX_ATTEMPTS, SPINS_PER_ATTEMPT)
