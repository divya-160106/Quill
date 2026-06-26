import "../styles/MessageBubble.css";
import ReactMarkdown from "react-markdown";

function MessageBubble({ role, content, isStreaming = false }) {
  return (
    <div className={`bubble ${role}`}>
      <ReactMarkdown
        components={{
          a: (props) => (
            <a {...props} target="_blank" rel="noopener noreferrer" />
          )
        }}
      >
        {content}
      </ReactMarkdown>
      {isStreaming && <span className="cursor" aria-hidden="true" />}
    </div>
  );
}

export default MessageBubble;