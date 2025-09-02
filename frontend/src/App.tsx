import "./App.css";

function App() {
  return (
    <>
      <h1>Which club do you prefer?</h1>
      <div style={{ display: "flex", flexDirection: "row", gap: "10px" }}>
        <div
          style={{
            borderRadius: "20px",
            backgroundColor: "rgb(255, 27, 63)",
            height: "80vh",
            width: "50vw",
          }}
        ></div>
        <div
          style={{
            borderRadius: "20px",
            backgroundColor: "rgb(0, 114, 255)",
            height: "80vh",
            width: "50vw",
            display: "flex",
          }}
        ></div>
      </div>
    </>
  );
}

export default App;
