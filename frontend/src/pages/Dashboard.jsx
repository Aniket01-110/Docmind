import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);

  // Redirect if not logged in
  useEffect(() => {
    if (!user) navigate("/login");
  }, [user]);

  // Load user's documents
  useEffect(() => {
    if (user) loadDocuments();
  }, [user]);

  const loadDocuments = async () => {
    const { data, error } = await supabase
      .from("documents")
      .select("*")
      .eq("user_id", user.id)
      .order("created_at", { ascending: false });

    if (!error) setDocuments(data);
  };

  const handleFileUpload = async (file) => {
    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "audio/mpeg",
      "audio/wav",
      "image/jpeg",
      "image/png",
      "text/csv",
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Unsupported file type");
      return;
    }

    setUploading(true);
    setError("");

    try {
      // Create form data
      const formData = new FormData();
      formData.append("file", file);

      // Send to FastAPI backend
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/documents/upload`,
        {
          method: "POST",
          body: formData,
        },
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Upload failed");
        return;
      }

      // Save document record to Supabase
      await supabase.from("documents").insert({
        user_id: user.id,
        filename: file.name,
        file_type: file.type,
        document_id: data.document_id,
        total_pages: data.total_pages || 1,
      });

      // Reload documents
      await loadDocuments();

      // Navigate to chat
      navigate(`/chat/${data.document_id}`);
    } catch (err) {
      setError("Upload failed. Is backend running?");
    } finally {
      setUploading(false);
    }
  };

  const getFileIcon = (fileType) => {
    if (fileType?.includes("pdf")) return "📄";
    if (fileType?.includes("audio")) return "🎵";
    if (fileType?.includes("image")) return "🖼️";
    if (fileType?.includes("csv")) return "📊";
    return "📁";
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navbar */}
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">DocMind</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-400 text-sm">{user?.email}</span>
          <button
            onClick={signOut}
            className="text-gray-400 hover:text-white text-sm transition-all"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-bold mb-2">Your Documents</h2>
        <p className="text-gray-400 mb-8">
          Upload a document to start chatting with AI
        </p>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 mb-6">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}

        {/* Upload Area */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            const file = e.dataTransfer.files[0];
            handleFileUpload(file);
          }}
          className={`border-2 border-dashed rounded-2xl p-12 text-center mb-8 transition-all
                        ${
                          dragOver
                            ? "border-blue-500 bg-blue-500/10"
                            : "border-gray-700 hover:border-gray-500"
                        }`}
        >
          <div className="text-4xl mb-4">📁</div>
          <p className="text-gray-300 font-medium mb-2">
            Drag and drop your file here
          </p>
          <p className="text-gray-500 text-sm mb-6">
            Supports PDF, Audio, Images, CSV
          </p>

          <label className="cursor-pointer">
            <span
              className={`
                            px-6 py-3 rounded-xl font-medium transition-all
                            ${
                              uploading
                                ? "bg-gray-700 text-gray-400 cursor-not-allowed"
                                : "bg-blue-600 hover:bg-blue-700 text-white"
                            }`}
            >
              {uploading ? "Uploading..." : "Choose File"}
            </span>
            <input
              type="file"
              className="hidden"
              disabled={uploading}
              accept=".pdf,.mp3,.wav,.jpg,.jpeg,.png,.csv"
              onChange={(e) => handleFileUpload(e.target.files[0])}
            />
          </label>
        </div>

        {/* Documents List */}
        {documents.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <p className="text-4xl mb-4">📂</p>
            <p>No documents yet. Upload one to get started!</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {documents.map((doc) => (
              <div
                key={doc.id}
                onClick={() => navigate(`/chat/${doc.document_id}`)}
                className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex items-center gap-4 hover:border-blue-500 cursor-pointer transition-all"
              >
                <span className="text-3xl">{getFileIcon(doc.file_type)}</span>
                <div className="flex-1">
                  <p className="font-medium text-white">{doc.filename}</p>
                  <p className="text-gray-400 text-sm">
                    {new Date(doc.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className="text-blue-400 text-sm">Chat →</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
