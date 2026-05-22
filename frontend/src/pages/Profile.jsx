import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";
import { useAuth } from "../context/AuthContext";

export default function Profile() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [loginHistory, setLoginHistory] = useState([]);

  useEffect(() => {
    if (!user) navigate("/login");
    else loadProfile();
  }, [user]);

  const loadProfile = async () => {
    const { data } = await supabase
      .from("profiles")
      .select("*")
      .eq("id", user.id)
      .single();

    if (data) {
      setProfile(data);
      setFullName(data.full_name || "");
    }

    // Load login history
    const { data: history } = await supabase
      .from("login_history")
      .select("*")
      .eq("user_id", user.id)
      .order("logged_in_at", { ascending: false })
      .limit(5);

    if (history) setLoginHistory(history);
  };

  const handleUpdateProfile = async () => {
    setLoading(true);
    setMessage("");

    const { error } = await supabase
      .from("profiles")
      .update({ full_name: fullName })
      .eq("id", user.id);

    if (!error) {
      setMessage("Profile updated successfully!");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navbar */}
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <button
          onClick={() => navigate("/dashboard")}
          className="text-gray-400 hover:text-white transition-all"
        >
          Back to Dashboard
        </button>
        <h1 className="text-xl font-bold">DocMind</h1>
        <button
          onClick={signOut}
          className="text-gray-400 hover:text-white text-sm"
        >
          Logout
        </button>
      </nav>

      <div className="max-w-2xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-bold mb-8">Your Profile</h2>

        {/* Profile Card */}
        <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 mb-6">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl font-bold">
              {fullName?.charAt(0) || user?.email?.charAt(0)}
            </div>
            <div>
              <p className="font-semibold text-lg">{fullName}</p>
              <p className="text-gray-400 text-sm">{user?.email}</p>
            </div>
          </div>

          {message && (
            <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-3 mb-4">
              <p className="text-green-400 text-sm">{message}</p>
            </div>
          )}

          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2">
              Full Name
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full bg-gray-800 text-white border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 transition-all"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-400 text-sm mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={user?.email}
              disabled
              className="w-full bg-gray-800/50 text-gray-400 border border-gray-700 rounded-xl px-4 py-3 cursor-not-allowed"
            />
          </div>

          <button
            onClick={handleUpdateProfile}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-xl transition-all disabled:opacity-50"
          >
            {loading ? "Saving..." : "Save Changes"}
          </button>
        </div>

        {/* Login History */}
        <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
          <h3 className="font-semibold mb-4">Recent Login History</h3>

          {loginHistory.length === 0 ? (
            <p className="text-gray-400 text-sm">No login history yet</p>
          ) : (
            <div className="space-y-3">
              {loginHistory.map((login) => (
                <div
                  key={login.id}
                  className="flex items-center justify-between py-2 border-b border-gray-800 last:border-0"
                >
                  <p className="text-gray-300 text-sm">
                    {new Date(login.logged_in_at).toLocaleString()}
                  </p>
                  <span className="text-green-400 text-xs">Logged in</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
