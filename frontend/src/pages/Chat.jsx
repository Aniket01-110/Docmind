import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";
import { useAuth } from "../context/AuthContext";

export default function Chat() {
  const { documentId } = useParams();
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);

  // Redirect if not logged in
  useEffect(() => {
    if (!user) navigate("/login");
  }, [user]);

  // Load chat sessions for sidebar
  useEffect(() => {
    if (user) loadSessions();
  }, [user]);

  // Load messages for current document
  useEffect(() => {
    if (user && documentId) loadOrCreateSession();
  }, [user, documentId]);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadSessions = async () => {
    const { data } = await supabase
      .from("chat_sessions")
      .select("*")
      .eq("user_id", user.id)
      .order("last_message_at", { ascending: false });

    if (data) setSessions(data);
  };

  const loadOrCreateSession = async () => {
    // Check if session exists
    let { data: session } = await supabase
      .from("chat_sessions")
      .select("*")
      .eq("user_id", user.id)
      .eq("document_id", documentId)
      .single();

    // Create session if not exists
    if (!session) {
      const { data: newSession } = await supabase
        .from("chat_sessions")
        .insert({
          user_id: user.id,
          document_id: documentId,
          document_name: documentId,
        })
        .select()
        .single();

      session = newSession;
    }

    setCurrentSession(session);
    loadMessages(session.id);
  };

  const loadMessages = async (sessionId) => {
    const { data } = await supabase
      .from("chat_messages")
      .select("*")
      .eq("session_id", sessionId)
      .order("created_at", { ascending: true });

    if (data) setMessages(data);
  };

  const handleSend = async () => {
    if (!question.trim() || loading) return;

    const userMessage = question.trim();
    setQuestion("");
    setLoading(true);

    // Add user message to UI immediately
    const tempUserMsg = {
      id: Date.now(),
      role: "user",
      content: userMessage,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      // Call FastAPI backend
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/chat/query`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question: userMessage,
            document_id: documentId,
            user_id: user.id,
          }),
        },
      );
      console.log("STATUS:", response.status);

      const data = await response.json();
      console.log(data);

      // Add AI response to UI
      const aiMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.answer,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);

      // Save both messages to Supabase
      if (currentSession) {
        await supabase.from("chat_messages").insert([
          {
            session_id: currentSession.id,
            user_id: user.id,
            role: "user",
            content: userMessage,
          },
          {
            session_id: currentSession.id,
            user_id: user.id,
            role: "assistant",
            content: data.answer,
            sources: data.sources,
          },
        ]);

        // Update last_message_at
        await supabase
          .from("chat_sessions")
          .update({ last_message_at: new Date().toISOString() })
          .eq("id", currentSession.id);

        // Reload sidebar sessions
        loadSessions();
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: "Error connecting to backend. Is it running?",
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-gray-950 flex overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
        {/* Logo */}
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-lg font-bold text-white">DocMind</h1>
        </div>

        {/* New Chat Button */}
        <div className="p-4">
          <button
            onClick={() => navigate("/dashboard")}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-xl transition-all"
          >
            + New Document
          </button>
        </div>

        {/* Chat Sessions */}
        <div className="flex-1 overflow-y-auto px-2">
          <p className="text-gray-500 text-xs px-2 mb-2 uppercase tracking-wider">
            Recent Chats
          </p>
          {sessions.map((session) => (
            <button
              key={session.id}
              onClick={() => navigate(`/chat/${session.document_id}`)}
              className={`w-full text-left px-3 py-2 rounded-xl mb-1 text-sm transition-all
                                ${
                                  session.document_id === documentId
                                    ? "bg-gray-700 text-white"
                                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                                }`}
            >
              <p className="truncate">
                {session.document_name || session.document_id}
              </p>
              <p className="text-xs text-gray-500 mt-0.5">
                {new Date(session.last_message_at).toLocaleDateString()}
              </p>
            </button>
          ))}
        </div>

        {/* User + Logout */}
        <div className="p-4 border-t border-gray-800">
          <p className="text-gray-400 text-xs truncate mb-2">{user?.email}</p>
          <button
            onClick={signOut}
            className="text-gray-500 hover:text-white text-xs transition-all"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="border-b border-gray-800 px-6 py-4">
          <p className="text-gray-300 font-medium">
            Document: {documentId?.slice(0, 8)}...
          </p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-20 text-gray-500">
              <p className="text-4xl mb-4">💬</p>
              <p className="font-medium text-gray-300 mb-2">
                Start chatting with your document
              </p>
              <p className="text-sm">
                Ask any question about the uploaded file
              </p>
            </div>
          )}

          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-2xl px-4 py-3 rounded-2xl text-sm
                                    ${
                                      msg.role === "user"
                                        ? "bg-blue-600 text-white rounded-br-sm"
                                        : "bg-gray-800 text-gray-100 rounded-bl-sm"
                                    }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 px-4 py-3 rounded-2xl rounded-bl-sm">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-gray-800 px-6 py-4">
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Ask a question about your document..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              disabled={loading}
              className="flex-1 bg-gray-800 text-white border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 transition-all placeholder-gray-500 disabled:opacity-50"
            />
            <button
              onClick={handleSend}
              disabled={loading || !question.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
