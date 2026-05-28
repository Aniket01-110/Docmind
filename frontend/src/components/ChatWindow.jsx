import { useState } from "react";

export default function ChatWindow({ document }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    // Add user message instantly
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);

    setInput("");
    setLoading(true);

    try {
      console.log("Sending request...");
      console.log("Document:", document);

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/chat/query`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: userMessage,
            document_id: document.document_id,
            user_id: document.user_id || "temp-user",
          }),
        },
      );

      console.log("Response status:", response.status);

      const data = await response.json();

      console.log("Response data:", data);

      if (!response.ok) {
        throw new Error(data.detail || "Query failed");
      }

      // Add AI response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: `Error: ${err.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg max-w-lg ${
              msg.role === "user" ? "bg-blue-600 ml-auto" : "bg-gray-800"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-800 p-3 rounded-lg max-w-lg">Thinking...</div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-gray-800 p-4 flex gap-2">
        <input
          className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 px-4 py-2 rounded-lg disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
