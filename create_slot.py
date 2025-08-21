import random
import itertools
from collections import Counter

class SlotMachine:
    """
    A class to define and simulate a simple 3-reel slot machine.

    This implementation is a Pythonic adaptation of the JavaScript example,
    focusing on clarity, reusability, and object-oriented design.
    """
    def __init__(self, config):
        """
        Initializes the SlotMachine with a given configuration.
        
        Args:
            config (dict): A dictionary containing symbols, weights, and the paytable.
        """
        print("--- Initializing Slot Machine ---")
        self.symbols = config['symbols']
        self.weights = config['weights']
        self.paytable = config['paytable']
        
        # Build the reel strip used for all three reels
        self.reel = self._build_reel()
        self.reel_length = len(self.reel)
        print(f"Reel length: {self.reel_length} stops")
        # An example slice of the generated reel
        print(f"Reel strip sample: {''.join(self.reel[:70])}...")
        print("-" * 35)

    def _build_reel(self):
        """
        Builds a single reel strip based on symbol weights.

        This method replicates the logic from the JS example to create a
        deterministic, evenly distributed reel strip, then inserts blanks.
        """
        # Create a string with all non-blank symbols
        symbol_counts = {self.symbols[i]: self.weights[i] for i in range(len(self.symbols))}
        total_symbols = sum(self.weights)
        
        reel_string = ""
        # This loop creates a distributed (not random) string of symbols
        while len(reel_string) < total_symbols:
            for i, symbol in enumerate(self.symbols):
                # Desired proportion of this symbol at the current length
                target_count = self.weights[i] / total_symbols * len(reel_string)
                current_count = reel_string.count(symbol)
                
                if current_count < self.weights[i] and current_count <= target_count:
                    reel_string += symbol
        
        # Intersperse blanks ('-') between every symbol
        final_reel = list("".join([char + '-' for char in reel_string]))
        
        return final_reel

    def _tally_wins(self, payline):
        """
        Calculates the win for a given payline based on the paytable.
        This is a more readable version of the JS tallyWins() function.
        
        Args:
            payline (tuple): A tuple of 3 symbols, e.g., ('C', 'C', 'C').
            
        Returns:
            int: The payout amount for the given payline.
        """
        payline_str = "".join(payline)

        # 1. Check for three-of-a-kind (triplets)
        if payline[0] == payline[1] == payline[2]:
            symbol = payline[0]
            if symbol in self.paytable['triplets']:
                return self.paytable['triplets'][symbol]

        # 2. Check for "Any Bar" combination
        # The original JS check was tricky. This is a clearer way to do it.
        bar_symbols = {'1', '2', '3'}
        if all(symbol in bar_symbols for symbol in payline):
            return self.paytable['any_bar']
            
        # 3. Check for Cherry combinations
        cherry_count = payline.count('C')
        if cherry_count == 2:
            return self.paytable['cherries']['two']
        if cherry_count == 1:
            return self.paytable['cherries']['one']

        # No win
        return 0

    def spin(self):
        """
        Simulates a single spin of the slot machine.

        Returns:
            tuple: A tuple containing the payline (3 symbols) and the win amount.
        """
        # Select a random stop for each of the three reels
        reel1_stop = random.choice(self.reel)
        reel2_stop = random.choice(self.reel)
        reel3_stop = random.choice(self.reel)
        
        payline = (reel1_stop, reel2_stop, reel3_stop)
        win = self._tally_wins(payline)
        
        return payline, win

    def calculate_theoretical_rtp(self):
        """
        Calculates the theoretical RTP by iterating through every possible combination.
        This is a "full cycle" test and is computationally intensive.
        """
        print("--- Calculating Theoretical RTP (Full Cycle Test) ---")
        print("This may take a moment...")
        
        total_wins = 0
        total_combinations = self.reel_length ** 3
        
        # Use itertools.product to efficiently get all combinations
        all_possible_paylines = itertools.product(self.reel, repeat=3)
        
        for payline in all_possible_paylines:
            total_wins += self._tally_wins(payline)
            
        rtp = total_wins / total_combinations
        print(f"Total Combinations: {total_combinations:,}")
        print(f"Total Wins over one cycle: {total_wins:,}")
        print(f"Programmed Theoretical RTP: {rtp:.6%}")
        print("-" * 35)
        return rtp

    def run_simulation(self, num_spins):
        """
        Runs a Monte Carlo simulation of many spins to find the empirical RTP.
        
        Args:
            num_spins (int): The number of spins to simulate.
        """
        print(f"--- Running Simulation ({num_spins:,} spins) ---")
        
        total_wins = 0
        # Assuming 1 credit bet per spin
        total_bet = num_spins
        
        for _ in range(num_spins):
            _, win = self.spin()
            total_wins += win
            
        empirical_rtp = total_wins / total_bet
        print(f"Total Amount Bet: {total_bet:,}")
        print(f"Total Amount Won: {total_wins:,}")
        print(f"Empirical RTP from simulation: {empirical_rtp:.6%}")
        print("-" * 35)
        return empirical_rtp

# --- Main Execution ---
if __name__ == "__main__":
    # Define the PAR sheet (Paytable and Reel Sheet) in a configuration dictionary
    # This is based on "Easy Vegas" PAR sheet #1 from the original JS code.
    GAME_CONFIG = {
        'symbols': ['J', '7', '3', '2', '1', 'C'], # Jackpot, 7, Triple/Double/Single Bar, Cherry
        'weights': [6,   8,   9,  11,  22,   8], # Number of times each symbol appears on the 64-stop symbol reel
        'paytable': {
            'triplets': {
                'J': 1199,
                '7': 200,
                '3': 100,
                '2': 90,
                '1': 40,
                'C': 40,
            },
            'any_bar': 10,
            'cherries': {
                'one': 1,
                'two': 5,
            }
        }
    }

    # 1. Create an instance of our slot machine
    my_slot_machine = SlotMachine(GAME_CONFIG)

    # 2. Calculate the exact, theoretical RTP by checking every possible outcome
    my_slot_machine.calculate_theoretical_rtp()

    # 3. Run a simulation of 10 million spins to see how close the real-world results get
    my_slot_machine.run_simulation(num_spins=10_000_000)