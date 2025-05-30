# simulate_game.py
from src.core.hypergraph import Hypergraph
from src.core.game import TakeAwayGame


def run_simulation():
    print("Starting TakeAwayGame Simulation...\n")

    # 1. Initialize Hypergraph
    hg = Hypergraph()
    hg.add_vertex("A")
    hg.add_vertex("B")
    hg.add_vertex("C")
    hg.add_vertex("D")
    hg.add_edge({"A", "B"})
    hg.add_edge({"C", "D"})
    hg.add_face({"A", "C", "D"})  # A face connecting A, C, D

    print("Initial Hypergraph State:")
    print(hg)
    print("-" * 30)

    # 2. Initialize Game
    game = TakeAwayGame(hg)
    print(f"Game initialized. Current Player: {game.current_player}\n")

    # --- Game Play Simulation ---

    # Move 1: Player 1 removes vertex 'A'
    print(f"[{game.current_player}] attempts to move vertex 'A'")
    try:
        game.move_vertex("A")
        print("Vertex 'A' moved. Hypergraph state after move: ")
        print(game.hypergraph)
        print(f"Next Player: {game.current_player}")
        print(f"Game Over: {game.is_game_over()}")
        print("-" * 30)
    except ValueError as e:
        print(f"Error moving 'A': {e}")
        return

    if game.is_game_over():
        print(f"Game Over! Winner: {game.winner}")
        return

    # Move 2: Player 2 removes vertex 'C'
    print(f"[{game.current_player}] attempts to move vertex 'C'")
    try:
        game.move_vertex("C")
        print("Vertex 'C' moved. Hypergraph state after move: ")
        print(game.hypergraph)
        print(f"Next Player: {game.current_player}")
        print(f"Game Over: {game.is_game_over()}")
        print("-" * 30)
    except ValueError as e:
        print(f"Error moving 'C': {e}")
        return

    if game.is_game_over():
        print(f"Game Over! Winner: {game.winner}")
        return

    # Move 3: Player 1 tries to move 'B'
    print(f"[{game.current_player}] attempts to move vertex 'B'")
    try:
        game.move_vertex("B")
        print("Vertex 'B' moved. Hypergraph state after move: ")
        print(game.hypergraph)
        print(f"Next Player: {game.current_player}")
        print(f"Game Over: {game.is_game_over()}")
        print("-" * 30)
    except ValueError as e:
        print(f"Error moving 'B': {e}")
        return

    if game.is_game_over():
        print(f"Game Over! Winner: {game.winner}")
        return

    # Move 4: Player 2 tries to move the last remaining vertex 'D'
    print(f"[{game.current_player}] attempts to move vertex 'D'")
    try:
        game.move_vertex("D")
        print("Vertex 'D' moved. Hypergraph state after move: ")
        print(game.hypergraph)
        print(f"Next Player: {game.current_player}")
        print(f"Game Over: {game.is_game_over()}")
        print("-" * 30)
    except ValueError as e:
        print(f"Error moving 'D': {e}")
        return

    if game.is_game_over():
        print(f"Game Over! Winner: {game.winner}")
        print("\n--- Simulation Complete ---")
        return

    print("\nSimulation ended without a winner (game not over yet).")


if __name__ == "__main__":
    run_simulation()
