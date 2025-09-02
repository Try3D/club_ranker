import sqlite3
from google import genai
from clubs import CLUBS

client = genai.Client(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


conn = sqlite3.connect("club_rankings.db")
cursor = conn.cursor()

cursor.execute("SELECT name, elo_rating FROM clubs ORDER BY elo_rating DESC")
ratings = cursor.fetchall()
conn.close()

elo_ratings = {name: rating for name, rating in ratings}

files = []
for club in CLUBS:
    try:
        with open(f"reports/{club}.md", "r") as f:
            files.append(f.read())
    except FileNotFoundError:
        files.append(f"No documentation available for {club}")

elo_explanation = """
ELO Rating System for Clubs:

ELO is a rating system originally designed for chess that measures relative skill levels.
In the context of club rankings:

- Starting Rating: All clubs begin at 1000 ELO points
- Winning: When a club "wins" against another (through competitions, achievements, etc.), 
  it gains ELO points while the losing club loses points
- Rating Changes: The amount of points transferred depends on the rating difference
  - Beating a higher-rated club gains more points
  - Losing to a lower-rated club loses more points
- Interpretation: Higher ELO = stronger performance/achievements relative to other clubs

Current ELO ranges typically mean:
- 1200+: Top performing clubs
- 1000-1200: Average performers  
- Below 1000: Underperforming clubs
"""

scores = {}
for i, club in enumerate(CLUBS):
    elo = elo_ratings.get(club, 1000.0)
    doc = files[i]

    doc_length_score = min(len(doc) / 1000 * 50, 50)
    doc_quality_score = 50 if len(doc.split("\n")) > 10 else 25

    total_score = (elo * 0.7) + ((doc_length_score + doc_quality_score) * 0.3)

    scores[club] = {
        "elo": elo,
        "doc_quality": doc_length_score + doc_quality_score,
        "total_score": total_score,
    }

ranked_clubs = sorted(scores.items(), key=lambda x: x[1]["total_score"], reverse=True)

analysis_prompt = f"""
Analyze the following club rankings data and provide insights:

Rankings:
{chr(10).join([f"{i + 1}. {club}: ELO {data['elo']:.1f}, Doc Quality {data['doc_quality']:.1f}, Total {data['total_score']:.1f}" for i, (club, data) in enumerate(ranked_clubs)])}

Provide a brief analysis of:
1. Which clubs are performing best and why
2. Patterns in the data
3. Recommendations for improvement
"""

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=analysis_prompt,
)
print(response.text)
