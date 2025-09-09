import React from "react";

export default function Toolkit(){
  const playBreath = () => alert("Start a 2-min breathing exercise (demo).");
  return (
    <div className="card">
      <h3>Wellness Toolkit</h3>
      <div className="toolGrid">
        <button onClick={playBreath}>🧘 Breathing Exercise</button>
        <button onClick={()=>alert("Meditation started (demo).")}>🎧 Meditation</button>
        <button onClick={()=>alert("Affirmations shown (demo).")}>💡 Affirmations</button>
        <button onClick={()=>alert("Yoga tips (demo).")}>🤸 Yoga</button>
      </div>
      <div style={{marginTop:10}}>
        <strong>Emergency</strong>
        <div>NIMHANS Helpline: 080-265-xxxx</div>
        <div>AASRA: 91-9820466726</div>
      </div>
    </div>
  )
}
