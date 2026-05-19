import { useState } from "react";
import { supabase } from "../services/supabase";
function Loginform() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loggedIn, setloggedIn] = useState(false);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email.includes("@")) {
      return setError("Not valid email");
    }

    if (password.length < 6) {
      return setError("Password length should be atleast 6 characters");
    }
    setSubmitted(true);
  };
  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
    });
    if (error) {
      return setError(error.message);
    }
  };

  if (submitted) {
    return (
      <div>
        <h2>Welcome</h2>
        <p> Logged in with {email}</p>
      </div>
    );
  }
  return (
    <form onSubmit={handleSubmit}>
      <h2> Simple login</h2>
      {error && <p style={{ color: "RED" }}>{error}</p>}

      <input
        type="text"
        placeholder="Your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type={showPassword ? "text" : "password"}
        placeholder="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="button" onClick={signInWithGoogle}>
        Sign in with Google
      </button>
      <button type="submit">Login</button>
    </form>
  );
}
export default Loginform;
