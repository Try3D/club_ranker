# Club Ranker: A Dynamic ELO-Based Club Ranking System

This project implements a dynamic club ranking system for Shiv Nadar University Chennai, using the ELO rating system. It provides a web interface for users to compare and vote for clubs, which in turn updates their rankings in real-time. The project also includes scripts for analyzing club performance and clustering clubs based on their descriptions.

## Features

*   **ELO-based Ranking:** Clubs are ranked using the ELO rating system, which is a method for calculating the relative skill levels of players in zero-sum games.
*   **Web Interface:** A simple and intuitive web interface for users to vote for their favorite clubs.
*   **Real-time Updates:** Club rankings are updated in real-time after each vote.
*   **REST API:** A FastAPI backend provides a REST API for accessing club data and rankings.
*   **Data Analysis:** Scripts for analyzing club performance and generating reports.
*   **Club Clustering:** A script for clustering clubs based on their descriptions using sentence transformers and K-Means clustering.

## How it works

The ELO rating system is the core of this project. Each club starts with an initial ELO rating of 1000. When a user votes for a club in a head-to-head comparison, the winning club gains ELO points, and the losing club loses them. The number of points gained or lost depends on the difference in the clubs' ratings before the vote.

The project consists of a backend server, a frontend web application, and a set of scripts for data analysis.

### Backend

The backend is a FastAPI application that provides the following API endpoints:

*   `GET /clubs`: Returns a list of all the clubs.
*   `GET /ranking`: Returns the current ELO rankings of all the clubs.
*   `GET /probability/{club1}/{club2}`: Returns the probability of each club winning against the other.
*   `POST /result/{winner}/{loser}`: Records the result of a vote and updates the ELO ratings of the clubs.

The backend uses a SQLite database to store club information and match results. The database schema is defined in `database.py`, and the database is initialized in `init_db.py`.

### Frontend

The frontend is a React application that allows users to vote for their favorite clubs. It fetches the list of clubs from the backend and presents the user with a choice between two randomly selected clubs. When the user clicks on a club, it sends the result to the backend and displays the new ratings and the probability of each club winning against the other.

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Install the backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Install the frontend dependencies:**
    ```bash
    cd frontend
    npm install
    ```
4.  **Initialize the database:**
    ```bash
    python init_db.py
    ```
5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
6.  **Run the frontend application:**
    ```bash
    cd frontend
    npm run dev
    ```

## Usage

1.  Open your web browser and go to `http://localhost:5173`.
2.  You will be presented with a choice between two clubs.
3.  Click on the club you prefer.
4.  The rankings will be updated, and you will see the new ratings and the probability of each club winning against the other.
5.  Click the "Next" button to vote for another pair of clubs.

## Future Scope

*   Add user authentication to prevent users from voting multiple times.
*   Add a leaderboard to display the top-ranked clubs.
*   Add more data sources for club analysis, such as social media engagement and event attendance.
*   Improve the club clustering algorithm to provide more accurate and meaningful clusters.
*   Deploy the application to a cloud platform so that it can be accessed by everyone.
