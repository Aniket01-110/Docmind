import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";
import { useAuth } from "../context/AuthContext";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import ChatWindow from "../components/ChatWindow";
import FileUploader from "../components/FileUploader";

export default function Dashboard() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  // redirect if not logged in
  useEffect(() => {
    if (!user) navigate("/login");
  }, [user]);

  // load docs
  useEffect(() => {
    if (user) loadDocuments();
  }, [user]);

  const loadDocuments = async () => {
    const { data } = await supabase
      .from("documents")
      .select("*")
      .eq("user_id", user.id)
      .order("created_at", { ascending: false });

    if (data) setDocuments(data);
  };

  // upload file
  const handleFileUpload = async (file) => {
    if (!file) return;

    setUploading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/documents/upload`,
        {
          method: "POST",
          body: formData,
        },
      );

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Upload failed");

      await supabase.from("documents").insert({
        user_id: user.id,
        filename: file.name,
        file_type: file.type,
        document_id: data.document_id,
      });

      await loadDocuments();

      // ⭐ AUTO OPEN CHAT (IMPORTANT)
      const { data: insertedDoc } = await supabase
        .from("documents")
        .select("*")
        .eq("document_id", data.document_id)
        .single();

      setSelectedDoc(insertedDoc);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      {/* SIDEBAR */}
      <Sidebar
        documents={documents}
        onSelectDoc={setSelectedDoc}
        onUpload={handleFileUpload}
      />

      {/* MAIN AREA */}
      <div className="flex-1 flex flex-col">
        {/* TOP BAR */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800">
          <Navbar />

          <div className="flex items-center gap-4">
            <FileUploader onUpload={handleFileUpload} loading={uploading} />

            <span className="text-gray-400 text-sm">{user?.email}</span>

            <button
              onClick={signOut}
              className="text-gray-400 hover:text-white text-sm"
            >
              Logout
            </button>
          </div>
        </div>

        {/* CHAT AREA */}
        <div className="flex-1 overflow-hidden">
          {selectedDoc ? (
            <ChatWindow document={selectedDoc} />
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              Select or upload a document to start chatting
            </div> 
          )}
        </div>
      </div>
    </div>
  );
}
