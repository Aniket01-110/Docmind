import { useState } from "react";

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const addMessage = (message) => {
    setMessages((prev) => [...prev, message]);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return {
    messages,
    setMessages,
    addMessage,
    clearChat,
    loading,
    setLoading,
  };
};
