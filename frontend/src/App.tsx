import React from "react";
import Navbar from "./components/Navbar";
import MainContent from "./components/MainContent";
import "./styles.css";

function App() {
  return (
    <div className="app">
      <Navbar />
      <MainContent />
    </div>
  );
}

export default App;
