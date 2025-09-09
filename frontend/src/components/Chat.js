import React, { useState, useEffect } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hey 👋, how are you feeling today?" }
  ]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);

  const sendMessage = async () => {
    if (!input) return;

    setMessages(prev => [...prev, { sender: "user", text: input }]);
    setInput("");
    setTyping(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: "demo_user", text: input })
      });
      const data = await res.json();

      // Simulate typing delay
      setTimeout(() => {
        setMessages(prev => [...prev, { sender: "bot", text: data.reply }]);
        setTyping(false);
      }, 700 + Math.random() * 500);

    } catch {
      setTimeout(() => {
        setMessages(prev => [...prev, { sender: "bot", text: "Error contacting server (mock mode)." }]);
        setTyping(false);
      }, 500);
    }
  };

  return (
    <div className="card">
      <h3>Chat</h3>
      <div className="chatBox">
        {messages.map((m, idx) => (
          <div key={idx} className={m.sender === "bot" ? "botBubble" : "userBubble"}>
            {m.text}
          </div>
        ))}
        {typing && <div className="botBubble">Typing...</div>}
      </div>
      <div className="chatInput">
        <input 
          type="text" 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          onKeyDown={e => e.key === "Enter" && sendMessage()} 
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
