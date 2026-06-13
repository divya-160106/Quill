import "../styles/MessageBubble.css";
import ReactMarkdown from "react-markdown";

function MessageBubble({role,content}){

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
    </div>
  );
}

export default MessageBubble;