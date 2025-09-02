from fastapi import FastAPI, HTTPException
from clubs import CLUBS

app = FastAPI()

elo = {club: 1000 for club in CLUBS}


@app.get("/clubs")
async def root():
    return CLUBS


@app.get("/ranking")
async def ranking():
    return {"rank": elo}


@app.get("/probability/{club1}/{club2}")
async def probability(club1: str, club2: str):
    if club1 not in elo or club2 not in elo:
        raise HTTPException(status_code=404, detail="Telemetry Not Found")

    rating1 = elo[club1]
    rating2 = elo[club2]

    prob1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    prob2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))

    return {club1: prob1, club2: prob2}


@app.post("/result/{winner}/{loser}")
async def result(winner: str, loser: str):
    if winner not in elo or loser not in elo:
        raise HTTPException(status_code=404, detail="Telemetry Not Found")

    K = 32
    rating_winner = elo[winner]
    rating_loser = elo[loser]

    prob_winner = 1 / (1 + 10 ** ((rating_loser - rating_winner) / 400))
    prob_loser = 1 / (1 + 10 ** ((rating_winner - rating_loser) / 400))

    elo[winner] = rating_winner + K * (1 - prob_winner)
    elo[loser] = rating_loser + K * (0 - prob_loser)

    return {
        "winner": winner,
        "new_rating_winner": elo[winner],
        "loser": loser,
        "new_rating_loser": elo[loser],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
