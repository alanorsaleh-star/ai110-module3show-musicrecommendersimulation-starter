from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_tempo_bpm: float = 100.0

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, str]:
        """Score a song in the OO recommender and return a score plus reasons."""
        minimum_profile = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'valence': getattr(user, 'target_valence', None),
            'tempo_bpm': getattr(user, 'target_tempo_bpm', None),
            'genre_weight': 2.0,
            'mood_weight': 1.0,
            'energy_weight': 1.5,
            'valence_weight': 1.2,
            'tempo_weight': 1.0,
        }
        song_dict = {
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'valence': song.valence,
            'tempo_bpm': song.tempo_bpm,
        }
        score, reasons = score_song(minimum_profile, song_dict)
        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Rank songs and return the top-k recommendations."""
        scored = []
        for song in self.songs:
            song_score, reason = self._score_song(user, song)
            scored.append((song_score, reason, song))

        scored_sorted = sorted(scored, key=lambda entry: entry[0], reverse=True)
        return [entry[2] for entry in scored_sorted[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain how a particular song score was computed."""
        _, reasons = self._score_song(user, song)
        return reasons

def load_songs(csv_path: str) -> List[Dict]:
    """Load song rows from a CSV path and convert numerical fields."""
    songs: List[Dict] = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = __import__('csv').DictReader(csvfile)
        for row in reader:
            try:
                row['id'] = int(row['id'])
                row['energy'] = float(row.get('energy', 0.0))
                row['tempo_bpm'] = float(row.get('tempo_bpm', 0.0))
                row['valence'] = float(row.get('valence', 0.0))
                row['danceability'] = float(row.get('danceability', 0.0))
                row['acousticness'] = float(row.get('acousticness', 0.0))
            except (ValueError, TypeError):
                continue
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences with reasons."""
    score = 0.0
    reasons: List[str] = []

    genre_weight = user_prefs.get('genre_weight', 2.0)
    mood_weight = user_prefs.get('mood_weight', 1.0)
    energy_weight = user_prefs.get('energy_weight', 1.5)
    valence_weight = user_prefs.get('valence_weight', 1.2)
    tempo_weight = user_prefs.get('tempo_weight', 1.0)

    user_genre = user_prefs.get('genre', '').strip().lower()
    song_genre = str(song.get('genre', '')).strip().lower()
    if user_genre and song_genre == user_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    user_mood = user_prefs.get('mood', '').strip().lower()
    song_mood = str(song.get('mood', '')).strip().lower()
    if user_mood and song_mood == user_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    if 'energy' in song and user_prefs.get('energy') is not None:
        target_energy = float(user_prefs.get('energy'))
        diff = abs(song['energy'] - target_energy)
        energy_score = max(0.0, 1.0 - diff) * energy_weight
        score += energy_score
        reasons.append(f"energy proximity (+{energy_score:.2f})")

    if 'valence' in song and user_prefs.get('valence') is not None:
        target_valence = float(user_prefs.get('valence'))
        diff = abs(song['valence'] - target_valence)
        valence_score = max(0.0, 1.0 - diff) * valence_weight
        score += valence_score
        reasons.append(f"valence proximity (+{valence_score:.2f})")

    if 'tempo_bpm' in song and user_prefs.get('tempo_bpm') is not None:
        target_tempo = float(user_prefs.get('tempo_bpm'))
        diff = abs(song['tempo_bpm'] - target_tempo)
        tempo_score = max(0.0, 1.0 - min(diff / 40.0, 1.0)) * tempo_weight
        score += tempo_score
        reasons.append(f"tempo proximity (+{tempo_score:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Recommend top-k songs based on score_song ranking."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song)
        scored.append((song, song_score, '; '.join(reasons)))

    sorted_songs = sorted(scored, key=lambda entry: entry[1], reverse=True)
    return sorted_songs[:k]

