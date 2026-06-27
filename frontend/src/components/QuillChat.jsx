import { useState, useRef, useEffect } from "react";
import "./../styles/QuillChat.css";
import MessageBubble from "./MessageBubble";

const API_URL = import.meta.env.VITE_API_URL;

function QuillChat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi. I'm Quill 🪶\n\nI am Divya's agent made by her to assist you.\n\nAsk anything you want to know about her!"
    }
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input };
    const currentInput = input;
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setMessages(prev => [...prev, { role: "assistant", content: "" }]);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: currentInput })
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      // Check if it's a streaming response or plain JSON
      const contentType = response.headers.get("content-type") || "";

      if (contentType.includes("application/json")) {
        // Non-streamed fallback 
        const data = await response.json();
        setMessages(prev => [
          ...prev.slice(0, -1),
          { role: "assistant", content: data.response }
        ]);
      } else {
        // Streamed response — read chunks and update the last message live
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulated = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          accumulated += decoder.decode(value, { stream: true });

          setMessages(prev => [
            ...prev.slice(0, -1),
            { role: "assistant", content: accumulated }
          ]);
        }
      }
    } catch (error) {
      console.error("ERROR:", error);
      setMessages(prev => [
        ...prev.slice(0, -1),
        { role: "assistant", content: "Connection failed." }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="quill-container">
      <div className="quill-header">
        <div>
          <h1>🪶 Quill</h1>
          <p>Portfolio AI + Writer Companion</p>
        </div>
      </div>

      <div className="messages">
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            role={msg.role}
            content={msg.content}
            isStreaming={
              loading &&
              index === messages.length - 1 &&
              msg.role === "assistant" &&
              msg.content !== ""
            }
          />
        ))}

        {/* Only show "thinking" before the first chunk arrives */}
        {loading && messages[messages.length - 1]?.content === "" && (
          <div className="typing">Quill is thinking...</div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask Quill anything..."
          disabled={loading}
          onKeyDown={e => {
            if (e.key === "Enter") sendMessage();
          }}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default QuillChat;