import time
import numpy as np
from poker_engine.hand_eval import batch_evaluate  # Ensure your compiled .so or .pyd is importable under this name

# Generate synthetic input: 658_008 games, each with 6 players, each player has 7 cards
# Cards are integers from 0 to 51 (standard deck), 52 cards total
num_games = 658_008
num_players = 6
num_cards = 7


# For benchmarking, random data is sufficient
np.random.seed(42)  # For reproducibility
random_games = np.random.randint(0, 52, size=(num_games, num_players, num_cards), dtype=np.int32)

# Convert to nested lists of arrays for compatibility with pybind11 input expectations
formatted_games = random_games.tolist()

# Convert to format: List[Array[Array[int, 7], 6]]
# (i.e., List of games, each game is a list of 6 players, each player has 7 cards)
formatted_games = [
    [player for player in game] for game in formatted_games
]

# Time the batch evaluation
start = time.perf_counter()
results = batch_evaluate(formatted_games)
end = time.perf_counter()

print(f"Evaluated {num_games} games in {end - start:.4f} seconds")
print(f"Average time per game: {(end - start) / num_games * 1e6:.2f} microseconds")