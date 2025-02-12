import React, { useEffect, useRef } from 'react';

interface Message {
  sender: string;
  message: string;
}

interface ChatContainerProps {
  chatMessages: Message[];
}

const ChatContainer: React.FC<ChatContainerProps> = ({ chatMessages }) => {
  const chatBoxRef = useRef<HTMLDivElement | null>(null);

  // Scroll to the bottom when a new message comes in.
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatMessages]);

  return (
    <div className="chat-container">
      <h2>Chat</h2>
      <div className="chat-box" ref={chatBoxRef}>
        {chatMessages.map((msg, index) => (
          <div
            key={index}
            className={`chat-message ${msg.sender.toLowerCase() === 'agent' ? 'agent' : ''}`}
          >
            <strong>{msg.sender}:</strong> {msg.message}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatContainer;
