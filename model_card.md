# Ìæß Model Card: Music Recommender Simulation

## 1. Model Name
VibeFinder 1.0

---

## 2. Goal / Task
Suggest 3-5 songs from a small catalog that best match a user taste profile (genre, mood, energy, valence, tempo). Predict which tracks fit the requested vibe.

---

## 3. Data Used
- Catalog size: 10 songs from `data/songs.csv`.
- Features: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness.
- Limits: small dataset, no behavior data, no lyrics or artist similarity.

---

## 4. Algorithm Summary
- +2.0 points for genre exact match.
- +1.0 point for mood exact match.
- Energy closeness adds up to ~1.5 points (more when closer).
- Valence closeness adds up to ~1.2 points.
- Tempo closeness adds up to ~1.0 point.
- Total score is the sum; recommend top N by descending score.

---

## 5. Observed Behavior / Biases
- Strong genre weighting can cause repeated top songs across profiles.
- ‚ÄúGym Hero‚Äù and ‚ÄúStorm Runner‚Äù often appear for multiple personas because of strong numeric closeness and pop/rock representation.
- Conflicted profiles (high energy + sad mood) show that numeric scores can outvote mood label.
- The model lacks collaborative context, so it can miss diverse but valid recommendations.

---

## 6. Evaluation Process
- Tested user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Adversarial Conflicted.
- Ran `python -m src.main`; verified top-5 outputs and scored explanations.
- Experimented with weight shift: doubled energy weight and halved genre weight.
- Observed where recommendations changed and described surprises.

---

## 7. Intended Use and Non-Intended Use
- Intended for classroom exploration and understanding scored content-based recommendation.
- Not intended for production deployment or fully reliable music personalization.
- Not intended for demographic fairness or replacing human-curated playlists.

---

## 8. Ideas for Improvement
- Add collaborative filtering signals (likes, listens, skips).
- Add serendipity/diversity methods to avoid over-concentrating on one song.
- Add user context (time of day, activity) and dynamic feedback.
- Include more moods and genres to reduce dataset bias.

---

## 9. Personal Reflection
Biggest learning moment: small explicit weights and distance measures can already produce useful recommendations, but they also reveal clear bias easily. AI generated prompt suggestions helped structure the feature and scoring design, yet I needed to double-check calculations and logic manually. It was surprising that this simple system could feel either right or wrong depending on weight tuning; it mimics real recommender tradeoffs. Next I would add real user behavior data and an exploration mechanism to balance close fit vs novelty.
