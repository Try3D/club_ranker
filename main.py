from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, init_db, Club, Match
from clubs import CLUBS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()
    db = next(get_db())
    try:
        for club_name in CLUBS:
            existing_club = db.query(Club).filter(Club.name == club_name).first()
            if not existing_club:
                club = Club(name=club_name, elo_rating=1000.0)
                db.add(club)
        db.commit()
    finally:
        db.close()


@app.get("/clubs")
async def root(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    return [club.name for club in clubs]


@app.get("/ranking")
async def ranking(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    rankings = {club.name: club.elo_rating for club in clubs}
    return {"rank": rankings}


@app.get("/probability/{club1}/{club2}")
async def probability(club1: str, club2: str, db: Session = Depends(get_db)):
    club1_obj = db.query(Club).filter(Club.name == club1).first()
    club2_obj = db.query(Club).filter(Club.name == club2).first()

    if not club1_obj or not club2_obj:
        raise HTTPException(status_code=404, detail="Club Not Found")

    rating1 = club1_obj.elo_rating
    rating2 = club2_obj.elo_rating

    prob1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    prob2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))

    return {club1: prob1, club2: prob2}


@app.post("/result/{winner}/{loser}")
async def result(winner: str, loser: str, db: Session = Depends(get_db)):
    winner_obj = db.query(Club).filter(Club.name == winner).first()
    loser_obj = db.query(Club).filter(Club.name == loser).first()

    if not winner_obj or not loser_obj:
        raise HTTPException(status_code=404, detail="Club Not Found")

    K = 32
    rating_winner = winner_obj.elo_rating
    rating_loser = loser_obj.elo_rating

    prob_winner = 1 / (1 + 10 ** ((rating_loser - rating_winner) / 400))
    prob_loser = 1 / (1 + 10 ** ((rating_winner - rating_loser) / 400))

    new_rating_winner = rating_winner + K * (1 - prob_winner)
    new_rating_loser = rating_loser + K * (0 - prob_loser)

    match = Match(
        winner=winner,
        loser=loser,
        winner_rating_before=rating_winner,
        loser_rating_before=rating_loser,
        winner_rating_after=new_rating_winner,
        loser_rating_after=new_rating_loser,
    )

    winner_obj.elo_rating = new_rating_winner
    loser_obj.elo_rating = new_rating_loser

    db.add(match)
    db.commit()

    prob_winner_new = 1 / (1 + 10 ** ((new_rating_loser - new_rating_winner) / 400))
    prob_loser_new = 1 / (1 + 10 ** ((new_rating_winner - new_rating_loser) / 400))

    return {
        "winner": winner,
        "new_rating_winner": new_rating_winner,
        "loser": loser,
        "new_rating_loser": new_rating_loser,
        "new_winner_probability": prob_winner_new,
        "new_loser_probability": prob_loser_new,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
