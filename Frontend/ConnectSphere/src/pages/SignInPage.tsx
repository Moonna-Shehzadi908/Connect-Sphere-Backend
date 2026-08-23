import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Auth.css";

export default function SignInPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      const response = await api.post("/auth/login/", {
        email,
        password,
      });

      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      alert("Login Successful!");
      navigate("/home");
    } catch (error: any) {
      console.log(error);

      if (error.response?.data) {
        alert(JSON.stringify(error.response.data));
      } else {
        alert("Invalid email or password");
      }
    }
  };

  const googleLogin = () => {
    alert("Google Sign In will be connected later.");
  };

  const appleLogin = () => {
    alert("Apple Sign In coming soon.");
  };

  return (
    <div className="authContainer">
      <div className="authCard">
        <h1>ConnectSphere</h1>

        <p>Enter your email and password</p>

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
          autoComplete="current-password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={login}>
          Sign In →
        </button>

        <div className="divider">
          <span >Or continue with</span>
        </div>

        <div className="socialBtns">
          <button onClick={googleLogin}>Google</button>
          <button onClick={appleLogin}>Apple</button>
        </div>

        <p className="bottomText">
          Don't have an account?{" "}
          <span onClick={() => navigate("/signup")}>
            Create Account
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