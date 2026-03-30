"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.85, "tempo_bpm": 120},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.6, "tempo_bpm": 78},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.5, "tempo_bpm": 150},
        "Adversarial Conflicted": {"genre": "pop", "mood": "sad", "energy": 0.9, "valence": 0.2, "tempo_bpm": 130},
    }

    for label, user_prefs in profiles.items():
        print(f"\n=== Profile: {label} ===")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f} | {explanation}")
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
