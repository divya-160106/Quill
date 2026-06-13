import { useState } from "react";
import "./../styles/QuillChat.css";

import MessageBubble from "./MessageBubble";

function QuillChat() {

  const [input,setInput] = useState("");

  const [messages,setMessages] = useState([
    {
      role:"assistant",
      content:
        "Hi. I'm Quill 🪶\n\nI know everything about Divyasree's projects, experience and skills.\n\nI'm also a writing assistant for plots, characters and worldbuilding."
    }
  ]);

  const [loading,setLoading] = useState(false);

  const sendMessage = async () => {

    if(!input.trim()) return;

    const userMessage = {
      role:"user",
      content:input
    };

    setMessages(prev => [...prev,userMessage]);

    const currentInput = input;

    setInput("");
    setLoading(true);

    try{

      const response = await fetch(
        "http://localhost:8000/chat",
        {
          method:"POST",
          headers:{
            "Content-Type":"application/json"
          },
          body:JSON.stringify({
            message:currentInput
          })
        }
      );

      const data = await response.json();

      setMessages(prev => [
        ...prev,
        {
          role:"assistant",
          content:data.response
        }
      ]);

    }catch(error){

      setMessages(prev => [
        ...prev,
        {
          role:"assistant",
          content:"Connection failed."
        }
      ]);

    }

    setLoading(false);
  };

  return (
    <div className="quill-container">

      <div className="quill-header">

        <div>
          <h1>🪶 Quill</h1>

          <p>
            Portfolio AI + Writer Companion
          </p>
        </div>

      </div>

      <div className="messages">

        {messages.map((msg,index)=>(
          <MessageBubble
            key={index}
            role={msg.role}
            content={msg.content}
          />
        ))}

        {loading && (
          <div className="typing">
            Quill is thinking...
          </div>
        )}

      </div>

      <div className="input-area">

        <input
          value={input}
          onChange={(e)=>setInput(e.target.value)}
          placeholder="Ask Quill anything..."
          onKeyDown={(e)=>{
            if(e.key==="Enter"){
              sendMessage();
            }
          }}
        />

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

    </div>
  );
}

export default QuillChat;