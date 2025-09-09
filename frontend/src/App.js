import React from "react";
import Chat from "./components/Chat";
import MoodTracker from "./components/MoodTracker";
import Toolkit from "./components/Toolkit";
import "./styles.css";

function App(){
  return (
    <div className="app">
      <header className="header">MannMitra</header>
      <main className="main">
        <Chat />
        <MoodTracker />
        <Toolkit />
      </main>
    </div>
  )
}

export default App;
