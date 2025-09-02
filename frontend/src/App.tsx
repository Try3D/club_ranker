import { useState, useEffect } from "react";
import "./App.css";

function capitalize(val: string) {
  return (
    String(val).charAt(0).toUpperCase() + String(val).slice(1).replace("_", " ")
  );
}

function App() {
  const [clubs, setClubs] = useState<[string, string] | null>(null);
  const [clicked, setClicked] = useState(false);
  const [data, setData] = useState({});

  const [pair, setPair] = useState<[string, string] | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/clubs")
      .then((data) => data.json())
      .then((clubData) => {
        setClubs(clubData);
      });
  }, []);

  useEffect(() => {
    if (!clubs) {
      return;
    }

    setClubPair();
  }, [clubs]);

  function setClubPair() {
    if (!clubs) {
      return;
    }
    let newPair: [string, string] | null = null;

    const club1 = clubs[Math.floor(Math.random() * 100) % clubs.length];
    let club2 = null;
    while (club2 === null || club2 === club1) {
      club2 = clubs[Math.floor(Math.random() * 100) % clubs.length];
    }

    newPair = [club1, club2];
    setPair(newPair);
  }

  if (clubs === null) {
    return <></>;
  }

  async function handleClick(i: number) {
    const j = i === 1 ? 0 : 1;
    await fetch(`http://localhost:8000/result/${pair[i]}/${pair[j]}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        setData({ ...res, winningIdx: i });
      });

    setClicked(true);
  }

  function handleNext() {
    setClicked(false);
    setClubPair();
  }

  return (
    <>
      <h1>Which club do you prefer?</h1>
      <div style={{ display: "flex", flexDirection: "row", gap: "10px" }}>
        <button
          style={{
            fontSize: "50px",
            color: "white",
            borderRadius: "20px",
            backgroundColor: clicked
              ? "rgb(255, 27, 63, 0.5)"
              : "rgb(255, 27, 63)",
            height: "80vh",
            width: "50vw",
            textAlign: "center",
            verticalAlign: "middle",
          }}
          onClick={() => {
            handleClick(0);
          }}
          disabled={clicked}
        >
          <>
            <div>{pair && capitalize(pair[0])}</div>
            {clicked &&
              (data.winningIdx === 0 ? (
                <>
                  <div>Rating: {Math.round(data.new_rating_winner)}</div>
                  <div>
                    Probability: {Math.round(data.new_winner_probability * 100)}
                    %
                  </div>
                </>
              ) : (
                <>
                  <div>Rating: {Math.round(data.new_rating_loser)}</div>
                  <div>
                    Probability: {Math.round(data.new_loser_probability * 100)}%
                  </div>
                </>
              ))}
          </>
        </button>
        <button
          style={{
            fontSize: "50px",
            color: "white",
            borderRadius: "20px",
            backgroundColor: clicked
              ? "rgb(0, 114, 255, 0.5)"
              : "rgb(0, 114, 255)",
            height: "80vh",
            width: "50vw",
            textAlign: "center",
            verticalAlign: "middle",
          }}
          onClick={() => {
            handleClick(1);
          }}
          disabled={clicked}
        >
          {pair && capitalize(pair[1])}
          {clicked &&
            (data.winningIdx === 1 ? (
              <>
                <div>Rating: {Math.round(data.new_rating_winner)}</div>
                <div>
                  Probability: {Math.round(data.new_winner_probability * 100)}%
                </div>
              </>
            ) : (
              <>
                <div>Rating: {Math.round(data.new_rating_loser)}</div>
                <div>
                  Probability: {Math.round(data.new_loser_probability * 100)}%
                </div>
              </>
            ))}
        </button>
      </div>

      <button
        onClick={handleNext}
        style={{ position: "absolute", bottom: "100px", right: "100px" }}
      >
        Next
      </button>
    </>
  );
}

export default App;
