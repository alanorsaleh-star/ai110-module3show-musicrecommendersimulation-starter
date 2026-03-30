# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This simulation is a simplified content-based music recommender. It uses song metadata from `data/songs.csv` and a user taste profile to assign similarity scores to each track, then ranks songs by that score. In the real world, recommender systems blend content signals, collaborative usage patterns (likes/skips), and context (time of day, activity) to suggest music that matches a listener’s current vibe.

Key ideas in this version:

- Each `Song` has categorical and numeric features describing its vibe.
- User preference is represented as a `UserProfile` with preferred genre, mood, and numeric targets for energy, valence, and tempo.
- The `Recommender` applies a scoring rule per song (distance from user numerical preference plus matching bonuses) and then uses a ranking rule to return top-N songs.

### Features used for each `Song`
- id, title, artist (metadata)
- genre (categorical)
- mood (categorical)
- energy (0.0-1.0)
- tempo_bpm
- valence (0.0-1.0)
- danceability (0.0-1.0)
- acousticness (0.0-1.0)

### Features used for `UserProfile`
- favorite_genre
- favorite_mood
- target_energy (0.0-1.0)
- target_valence (0.0-1.0)
- target_tempo_bpm
- weights: genre_weight, mood_weight, numeric_weight (or individual numeric weights)

### Algorithm Recipe (Scoring + Ranking)
1. genre_score = 2.0 if `song.genre == profile.favorite_genre` else 0.0
2. mood_score = 1.0 if `song.mood == profile.favorite_mood` else 0.0
3. energy_score = (1 - abs(song.energy - profile.target_energy)) * 1.5
4. valence_score = (1 - abs(song.valence - profile.target_valence)) * 1.2
5. tempo_score = max(0, 1 - abs(song.tempo_bpm - profile.target_tempo_bpm)/40) * 1.0
6. Optional: danceability_score = song.danceability * 0.5 or user preference distance
7. Optional: acousticness_score = (1 - abs(song.acousticness - profile.target_acousticness)) * 0.5
8. total_score = genre_score + mood_score + energy_score + valence_score + tempo_score

Ranking rule: sort candidates by `total_score` descending, return top K.

Potential bias note:
- This system may over-prioritize genre and mood matches, which can hide “good” songs from other genres that are close in energy and valence. It also assumes a single static taste profile per session and ignores collaborative signals like what other users on similar profiles enjoy.

---

## 1. Reflection

This project showed that even a simple scoring engine can make predictions by translating preferences into numerical distances and categorical matches. For example, the system assigns +2 for genre match and +1 for mood match, then adds similarity-based energy/valence/tempo scores. This made recommendations that mostly felt right for clear profiles (e.g., Chill Lofi still returned lofi tracks), but it also surfaced bias: pop/rock songs dominated because genre bonus is strong and the catalog is small.

Bias and unfairness happen when the scoring formula is unbalanced. In our exercise, conflicting input (high-energy + sad mood) tended to favor intensity and genre over mood, which can push reasonable “sad” recommendations out of the top results. That mirrors real systems where “filter bubbles” form from high-weighted signals and unbalanced data distribution.

---

## 2. Intended Use

This recommender prototype is designed to pick 3 to 5 songs from a small catalog by comparing each track to a user’s stated taste profile. It's meant for classroom exploration, learning, and demo purposes, not for production use.

---

## 3. How It Works (Short Explanation)

This recommender ranks songs by comparing each song’s attributes to user preferences:

- Song features considered: genre, mood, energy, tempo_bpm, valence, (optionally danceability/acousticness).
- User information: preferred genre, preferred mood, target energy, target valence, target tempo.
- Scoring method: add a genre bonus (+2 for exact match), mood bonus (+1 for exact match), and closeness points for energy/valence/tempo (bigger points for smaller difference). The system sums these into a total score.

The final recommendations are the top-scoring songs, sorted highest to lowest.


---

## 4. Data

- How many songs are in `data/songs.csv`: 10 songs in the starter data.
- Did you add or remove any songs: I suggested expanding with additional songs in the plan, but core dataset remains 10 rows by default.
- What kinds of genres or moods are represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop; moods include happy, chill, intense, relaxed, moody, focused.
- Whose taste does this data mostly reflect: the dataset is synthetic and varied, but it is biased toward energetic pop/rock and chill lofi, and doesn’t cover many niche tastes.

---

## 5. Strengths

- Works well for clear profiles: Chill Lofi users get lofi chill songs, high-energy pop users get energetic pop.
- Easy to understand and modify: weights are explicit, and each contribution to score is traceable.
- Provides good feedback to developer in explain mode: reasons like "genre match (+2.0)" make behavior clear.

---

## 6. Limitations and Bias

This recommender struggles in a few predictable ways:

- It can under-represent genres/moods that do not match the explicit favorite values, because genre (+2) and mood (+1) bonuses are strong compared to numeric differences.
- It treats every profile as a single vector (one taste shape), so it cannot capture users with mixed or evolving preferences.
- It has a mild bias toward higher numeric similarity and mostly popular/energetic songs in the catalog, especially when the catalog is small and unbalanced (more pop/rock than niche types).
- In a real product, this could look unfair by repeatedly serving the same narrow set of songs and suppressing underrepresented artists or cultural styles for users whose preferences are not in the majority.
- It also ignores collaborative signals (play history, skips, social proof), lyrics, and context (time of day, activity), so it may miss what the user actually wants in real sessions.

---

## 7. Evaluation

I validated the system by running multiple hard-coded profiles in `src/main.py` and checking whether the top-3 songs aligned with the stated preferences:
- A chill lo-fi profile returned mostly lofi/chill tracks with moderate tempo and low energy.
- A high-energy pop profile returned pop/rock songs with high tempo and valence.
- A focused ambient profile returned ambient/relaxed tracks with low tempo and high acousticness.

I also implemented unit tests in `tests/test_recommender.py` covering profile-to-song scoring and ranking logic, which helped catch edge cases (e.g., exact match vs. near match). I did not use a single scalar metric, but I observed score separation (higher profile match => higher total score) as the quality check.

---

## 8. Future Work

- Add collaborative filtering signals (user listening history, item co-occurrence) to complement content-based scoring.
- Implement diversity constraints (e.g., promote underrepresented genres on the ranked list) to reduce filter bubble bias.
- Expand the dataset to hundreds of songs and include additional features (lyrics sentiment, artist popularity, release year) for richer modeling.
- Add online learning: update user taste vector from skip/like events instead of fixed static profiles.

---

## 9. Personal Reflection

Building this project reinforced that even a straightforward formula can produce plausible recommendations, but simple systems are very sensitive to weight tuning and data balance. It was surprising how strong categorical bonuses (genre/mood) dominated numeric similarity in a tiny catalog, which is a nice lesson in engineering tradeoffs.

In real recommenders, human judgment is still vital for defining fairness and diversity guardrails, and for validating that scored outputs actually meet user intent in context (e.g., mood vs. activity).

