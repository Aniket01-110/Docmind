export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`w-full flex ${isUser ? "justify-end" : "justify-start"} mb-3`}
    >
      <div
        className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm whitespace-pre-wrap
        ${isUser ? "bg-blue-600 text-white" : "bg-gray-800 text-gray-100"}`}
      >
        {message.content}
      </div>
    </div>
  );
}
