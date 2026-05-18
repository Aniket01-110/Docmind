//practing simple form using react js
import { useState } from "react";

function SimpleForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!name || !email) {
      setError("All fields are required");
      return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Invalid email — enter a valid email like name@gmail.com");
      return;
    }
    setError("");
    setSubmitted(true);
  };
  if (submitted) {
    return (
      <div>
        <h2>Welcome {name}!</h2>
        <p> Signed up with {email}</p>
      </div>
    );
  }
  return (
    <form onSubmit={handleSubmit}>
      <h2> Simple Signup</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <input
        type="text"
        placeholder="Your name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="text"
        placeholder="Your Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button type="submit">SignUp</button>
    </form>
  );
}
export default SimpleForm;
