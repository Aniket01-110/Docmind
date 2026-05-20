// building fakesignup
import { useState } from "react";
function FakeSignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [submit, setSubmitted] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email.includes("@")) {
      return setError("not an valid email");
    }

    if (password.length < 6) {
      return setError("Password must be atleast 6 characters");
    }
    setSubmitted(true);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
    }, 2000);
  };
  if (success) {
    <div>
      <h2>Account created</h2>
      <p> Welcome {email}</p>
    </div>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>FakeSignUp</h2>
      {error && <p style={{ color: "RED" }}> {error}</p>}

      <input
        type="text"
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type={showPassword ? "text" : "password"}
        placeholder="enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Creating Account.." : "SignUp"}
      </button>
    </form>
  );
}
export default FakeSignUp;
