import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Auth.css";

export default function SignUpPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const createAccount = async () => {
    if (!username || !email || !password) {
      alert("Please fill all fields");
      return;
    }

    try {
      const response = await api.post("/auth/register/", {
        username,
        email,
        password,
        password2: password,
      });

      console.log("SUCCESS:", response.data);

      alert("Account created successfully!");
      navigate("/signin");

    } catch (error: any) {
      console.log("STATUS:", error.response?.status);
      console.log("DATA:", error.response?.data);
      console.log(error);

      if (error.response?.data) {
        alert(JSON.stringify(error.response.data));
      } else {
        alert("Registration failed");
      }
    }
  };

  return (
    <div className="authContainer">
      <div className="authCard">
        <h1>ConnectSphere</h1>
        <h2>Create Account</h2>

        <input
          type="text"
          placeholder="Enter Username"
          value={username}
          autoComplete="off"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="email"
          placeholder="Enter Email"
          value={email}
          autoComplete="email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          autoComplete="new-password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={createAccount}>
          Create Account →
        </button>

        <p className="bottomText">
          Already have account?{" "}
          <span onClick={() => navigate("/signin")}>
            Sign In
          </span>
        </p>

        <button
          className="backBtn"
          onClick={() => navigate(-1)}
        >
          ← Back
        </button>
      </div>
    </div>
  );
}