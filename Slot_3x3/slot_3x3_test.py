import random
import os
import time

# Helper function to clear the terminal screen for a clean UI
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class SlotMachine3x3:
    """
    Represents a 3x3 video slot machine based on "Jogo do Tigrinho" rules,
    including a 'W' (Wild) symbol.
    """
    def __init__(self, config):
        """
        Initializes the machine with a configuration and defines the paylines.
        """
        print("--- Initializing 3x3 Slot Machine (Tigrinho Rules) ---")
        self.symbols = config['symbols']
        self.weights = config['weights']
        self.paytable = config['paytable']
        
        # The reel strip is a long virtual reel from which the visible grid is taken.
        self.reel_strip = self._build_reel_strip()
        
        self.paylines = [
            # Horizontal Lines
            [(0, 0), (0, 1), (0, 2)],  # Top row
            [(1, 0), (1, 1), (1, 2)],  # Middle row
            [(2, 0), (2, 1), (2, 2)],  # Bottom row
            # Diagonal Lines
            [(0, 0), (1, 1), (2, 2)],  # Top-left to bottom-right
            [(2, 0), (1, 1), (0, 2)],  # Bottom-left to top-right
        ]
        print(f"{len(self.paylines)} paylines have been configured.")
        print("The 'W' symbol is WILD!")
        print("-" * 35)

    def _build_reel_strip(self):
        """Builds a single, long reel strip based on symbol weights."""
        strip = []
        for i, symbol in enumerate(self.symbols):
            strip.extend([symbol] * self.weights[i])
        random.shuffle(strip) # Shuffle to make it feel random
        return strip

    def spin(self):
        """
        Generates a 3x3 grid of symbols.
        Each column is a continuous 3-symbol segment from the reel strip.
        """
        grid = [['' for _ in range(3)] for _ in range(3)]
        reel_len = len(self.reel_strip)
        
        for col in range(3):
            start_index = random.randint(0, reel_len - 1)
            for row in range(3):
                symbol_index = (start_index + row) % reel_len
                grid[row][col] = self.reel_strip[symbol_index]
                
        return grid

    def calculate_wins(self, grid):
        """
        Calculates the total win and identifies winning lines from a grid.
        Includes logic for the 'W' (Wild) symbol.
        """
        total_win = 0
        winning_lines_info = []

        for i, line_coords in enumerate(self.paylines):
            line_symbols = [grid[r][c] for r, c in line_coords]
            
            # Identify the target symbol for a potential win
            target_symbol = None
            if line_symbols[0] == line_symbols[1] == line_symbols[2]:
                # Standard 3-of-a-kind
                target_symbol = line_symbols[0]
            else:
                # Check for wild card substitutions
                non_wild_symbols = [s for s in line_symbols if s != 'W']
                if not non_wild_symbols:
                    # All three are Wilds
                    target_symbol = 'W'
                elif len(set(non_wild_symbols)) == 1:
                    # All non-wild symbols are the same (e.g., [O, W, O] or [W, C, W])
                    target_symbol = non_wild_symbols[0]

            # If a winning combination was found, calculate the pay
            if target_symbol and target_symbol in self.paytable:
                win_amount = self.paytable[target_symbol]
                total_win += win_amount
                winning_lines_info.append({
                    'line_index': i + 1,
                    'symbols': tuple(line_symbols),
                    'amount': win_amount
                })
                    
        return total_win, winning_lines_info

class Player:
    """Manages a player's balance and betting."""
    def __init__(self, initial_balance=200):
        self.balance = initial_balance
        self.history = [initial_balance]

    def place_bet(self, total_bet_amount):
        if self.balance < total_bet_amount:
            return False
        self.balance -= total_bet_amount
        return True

    def receive_winnings(self, amount):
        self.balance += amount
        self.history.append(self.balance)

def display_grid(grid):
    """Prints the 3x3 grid in a nice format."""
    print(" " * 5 + "--- Reels ---")
    for row in grid:
        print(" " * 5 + f"| {row[0]} | {row[1]} | {row[2]} |")
    print(" " * 5 + "-------------")

def game_loop(player, machine):
    """The main interactive game loop."""
    bet_per_line = 1
    num_lines = len(machine.paylines)
    total_bet = bet_per_line * num_lines

    while True:
        clear_screen()
        print("--- 3x3 Multi-Line Slot ---")
        print(f"Your Balance: ${player.balance:.2f}")
        print(f"Bet: ${bet_per_line} on {num_lines} lines (Total Bet: ${total_bet})")
        print("-" * 35)

        action = input("Press ENTER to spin, or type 'q' to quit: ").lower()
        if action == 'q':
            break

        if not player.place_bet(total_bet):
            print("Game Over! You've run out of money. �")
            break

        grid = machine.spin()
        
        print("\nSpinning...")
        time.sleep(0.5) # Pause for effect
        display_grid(grid)
        
        total_win, winning_lines = machine.calculate_wins(grid)

        if total_win > 0:
            print(f"\nCongratulations! You won a total of ${total_win}!")
            for win_info in winning_lines:
                print(f"  - Line {win_info['line_index']}: {' '.join(win_info['symbols'])} paid ${win_info['amount']}")
            player.receive_winnings(total_win)
        else:
            print("\nNo winning lines this time.")
        
        input("\nPress ENTER for the next spin...")

if __name__ == "__main__":
    # Configuration for our 3x3 machine, simplified for the new rules.
    GAME_CONFIG_3x3 = {
        'symbols': ['W', 'B', 'T', 'O', 'C', 'S','L'], # Wild, Bell, Tiger, Orange, Cherry, Sack, Lemon
        'weights': [3, 1, 10, 21, 5, 26, 15], 
        'paytable': {
            # Payout for 3-of-a-kind on any active payline
            'W': 250,   
            'B': 100,   
            'T': 25,   
            'O': 15,  
            'C': 10,
            'S': 8,
            'L': 6,
        }
    }

    # Initialize the machine and the player
    slot_machine_3x3 = SlotMachine3x3(GAME_CONFIG_3x3)
    human_player = Player(initial_balance=200)

    # Start the game
    game_loop(human_player, slot_machine_3x3)

    print("\n--- Thanks for playing! ---")
    print(f"You finished with a balance of ${human_player.balance:.2f}")
