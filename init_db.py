from database import init_db, SessionLocal, Club
from scripts.clubs import CLUBS


def initialize_database():
    print("Creating database tables...")
    init_db()
    
    db = SessionLocal()
    try:
        for club_name in CLUBS:
            existing_club = db.query(Club).filter(Club.name == club_name).first()
            if not existing_club:
                club = Club(name=club_name, elo_rating=1000.0)
                db.add(club)
        
        db.commit()
        print(f"Initialized {len(CLUBS)} clubs in database")
        
        clubs = db.query(Club).all()
        for club in clubs:
            print(f"{club.name}: {club.elo_rating}")
            
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()