import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./ChatBot.css";

const ChatBot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false); // Add loading state

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { text: input, isUser: true };
    setMessages([...messages, userMessage]);
    setIsLoading(true); // Set loading state to true

    setInput("");
    try {
      const response = await axios.post("http://localhost:8000/ask", {
        userid: "akram@gmail.com",
        question: input,
      });

      const botMessage = {
        text: response.data.response.replace(/\*/g, ""), // Remove asterisks
        isUser: false,
      };
      setMessages([...messages, userMessage, botMessage]);
    } catch (error) {
      console.error("Error sending message", error);
      const errorMessage = {
        text: "Error: Could not get a response.",
        isUser: false,
      };
      setMessages([...messages, userMessage, errorMessage]);
    } finally {
      setIsLoading(false); // Set loading state back to false after response
    }

    // setInput('');
  };

  return (
    <div className="chat-container">
      <div
        className="d-flex flex-row justify-align-content-start align-items-center pt-2 pb-2 ps-1 pe-1"
        style={{ backgroundColor: "#C16A3F" }}
      >
        <div
          className="rounded-circle"
          style={{ width: "40px", height: "40px" }}
        >
          <img
            alt="chat-icon"
            src="https://miro.medium.com/v2/resize:fit:612/1*C_LFPy6TagD1SEN5SwmVRQ.jpeg"
            className="img-fluid rounded-circle"
          />
        </div>
        <div className=" d-flex align-items-center justify-content-center">
          <p className="fw-bold text-light ms-3 pt-2">AI-Driven Student Assistant</p>
        </div>
      </div>

      <div className="chat-container">
        <div className="message-list">
          {messages.length === 0 ? (
            <div className="flex flex-column justify-content-center align-items-center">
              <img alt="" src="/assets/images/chat.png" className="img-fluid" />
              <p style={{ textAlign: "center" }}>
                Hello there! 👋 It's nice to meet you!
              </p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.isUser ? "user" : "bot"}`}
              >
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => (e.key === "Enter" ? sendMessage() : null)}
          placeholder="Enter your question..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBot;
