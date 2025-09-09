import React from "react";

export default function MoodTracker(){
  const moods = ["😊","😟","😔","😡","😴"];
  const saveMood = async (mood) => {
    await fetch("http://localhost:8000/mood", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({user_id:"demo_user", mood})
    });
    alert("Mood saved!");
  }
  return (
    <div className="card">
      <h3>Mood Tracker</h3>
      <div className="moodRow">
        {moods.map((m, idx) => (
          <button key={idx} className="moodBtn" onClick={()=>saveMood(m)}>{m}</button>
        ))}
      </div>
    </div>
  )
}
