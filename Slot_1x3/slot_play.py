import random
import itertools
import os

# This function helps clear the terminal screen for a better user experience
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- SLOT MACHINE CLASS (from our previous code) ---
class SlotMachine:
    """
    The engine of the slot machine. Holds the game logic.
    (Slightly simplified from the previous version for this script)
    """
    def __init__(self, config):
        self.symbols = config['symbols']
        self.weights = config['weights']
        self.paytable = config['paytable']
        self.reel = self._build_reel()

    def _build_reel(self):
        reel_string = ""
        total_symbols = sum(self.weights)
        while len(reel_string) < total_symbols:
            for i, symbol in enumerate(self.symbols):
                target_count = self.weights[i] / total_symbols * len(reel_string)
                if reel_string.count(symbol) < self.weights[i] and reel_string.count(symbol) <= target_count:
                    reel_string += symbol
        return list("".join([char + '-' for char in reel_string]))

    def _tally_wins(self, payline):
        payline_str = "".join(payline)
        if payline[0] == payline[1] == payline[2]:
            if payline[0] in self.paytable['triplets']:
                return self.paytable['triplets'][payline[0]]
        bar_symbols = {'1', '2', '3'}
        if all(symbol in bar_symbols for symbol in payline):
            return self.paytable['any_bar']
        cherry_count = payline.count('C')
        if cherry_count == 2: return self.paytable['cherries']['two']
        if cherry_count == 1: return self.paytable['cherries']['one']
        return 0

    def spin(self):
        payline = (random.choice(self.reel), random.choice(self.reel), random.choice(self.reel))
        win = self._tally_wins(payline)
        return payline, win

# --- PLAYER CLASS (New!) ---
class Player:
    """
    Manages a player's state, including their balance and bet history.
    """
    def __init__(self, initial_balance=100, bet_amount=1):
        self.balance = initial_balance
        self.bet_amount = bet_amount
        # History will store the balance after each spin
        self.history = [initial_balance]
        print(f"Welcome! You are starting with ${initial_balance}.")

    def place_bet(self):
        """Places a bet if the balance is sufficient."""
        if self.balance < self.bet_amount:
            return False
        self.balance -= self.bet_amount
        return True

    def receive_winnings(self, amount):
        """Adds winnings to the player's balance."""
        self.balance += amount

    def record_history(self):
        """Records the current balance to the history log."""
        self.history.append(self.balance)

# --- MAIN GAME LOOP ---
def game_loop(player, machine):
    """
    The main interactive loop for playing the game.
    """
    spin_count = 0
    while True:
        clear_screen()
        print("--- Jogo do Tigrinho Simulator ---")
        print(f"Your Balance: ${player.balance}")
        print(f"Bet Amount:   ${player.bet_amount}")
        print("-" * 35)
        
        # Get user input to spin or quit
        action = input("Press ENTER to spin, or type 'q' to quit: ").lower()
        if action == 'q':
            print("You are leaving the game. Thanks for playing!")
            break

        # Check if player can afford to play
        if not player.place_bet():
            print("Game Over! You've run out of money. 😥")
            break
            
        spin_count += 1
        payline, win = machine.spin()
        
        # Display the result of the spin
        print("\nSpinning...")
        print(f"  > | {payline[0]} | {payline[1]} | {payline[2]} | <")

        if win > 0:
            print(f"\nCongratulations! You won ${win}! 🥳")
            player.receive_winnings(win)
        else:
            print("\nNo win this time. Better luck next spin! 🤞")
        
        player.record_history()
        
        # A small pause to let the player see the result
        input("\nPress ENTER to continue to the next spin...")

    return spin_count

# --- Main Execution ---
if __name__ == "__main__":
    # Define the PAR sheet for our game
    GAME_CONFIG = {
        'symbols': ['J', '7', '3', '2', '1', 'C'],
        'weights': [6, 8, 9, 11, 22, 8],
        'paytable': {
            'triplets': {'J': 1199, '7': 200, '3': 100, '2': 90, '1': 40, 'C': 40},
            'any_bar': 10,
            'cherries': {'one': 1, 'two': 5}
        }
    }

    # 1. Initialize the machine and the player
    slot_machine = SlotMachine(GAME_CONFIG)
    human_player = Player(initial_balance=100, bet_amount=1)

    # 2. Start the interactive game
    starting_balance = human_player.balance
    total_spins = game_loop(human_player, slot_machine)
    
    # 3. Print a final summary
    print("\n--- Game Summary ---")
    print(f"You played for {total_spins} spins.")
    print(f"Starting Balance: ${starting_balance}")
    print(f"Ending Balance:   ${human_player.balance}")
    print("-" * 35)
    # This shows the data we'll use for plotting later!
    # print(f"Your balance history: {human_player.history}")