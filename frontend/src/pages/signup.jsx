//Practicing first simple form building before full fledged signup system

import { useState } from "react";

function SimpleForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    //Simple validation
    if (!name || !email) {
      setError("All fields required");
      return;
    }

    if (!email.includes("@")) {
      setError("Invalid email");
      return;
    }
    setError("");
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div>
        <h2>Welcome {name}!</h2>
        <p>Signed up with: {email}</p>
      </div>
    );
  }
  return (
    <form onSubmit={handleSubmit}>
      <h2> Simple Signup</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <input
        type="text"
        placeholder="Your Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Your Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button type="submit">Sign Up</button>
    </form>
  );
}
export default SimpleForm;
