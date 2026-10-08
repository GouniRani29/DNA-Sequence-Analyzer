import { useState } from "react";
import { loginUser } from "../services/authService";

function Login({ onLogin, onSignUp, onBack }) {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {

    e.preventDefault();

    setError("");

    if (!username || !password) {
      setError("Please enter username and password.");
      return;
    }

    try {

      setLoading(true);

      const data = await loginUser(
        username,
        password
      );

      console.log("Login successful:", data);

      localStorage.setItem(
        "userId",
        data.userId
      );

      localStorage.setItem(
        "username",
        data.username
      );

      onLogin(data);

    } catch (err) {

      console.error("Login error:", err);

      setError(
        err.message ||
        "Invalid username or password."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="auth-page">

      <div className="auth-glow auth-glow-one"></div>
      <div className="auth-glow auth-glow-two"></div>


      <div className="login-wrapper">

        {/* LEFT SIDE */}

        <div className="auth-info">

          <div className="auth-logo">
            🧬
          </div>

          <h1>
            DNA
            <span> Analyzer</span>
          </h1>

          <p>
            Unlock intelligent DNA sequence analysis
            powered by Deep Learning and Transformer
            technology.
          </p>

          <div className="auth-features">

            <div>
              <span>🧬</span>
              <p>Advanced DNA Analysis</p>
            </div>

            

            <div>
              <span>🔒</span>
              <p>Secure & Private</p>
            </div>

          </div>

        </div>


        {/* LOGIN CARD */}

        <div className="auth-card login-card">

          <div className="auth-card-header">

            <div className="auth-small-icon">
              ✨
            </div>

            <h2>
              Welcome Back
            </h2>

            <p>
              Sign in to continue DNA analysis
            </p>

          </div>


          <form onSubmit={handleLogin}>

            {/* USERNAME */}

            <div className="auth-field">

              <label>
                Username
              </label>

              <div className="input-wrapper">

                <span>👤</span>

                <input
                  type="text"
                  value={username}
                  onChange={(e) =>
                    setUsername(e.target.value)
                  }
                  placeholder="Enter username"
                />

              </div>

            </div>


            {/* PASSWORD */}

            <div className="auth-field">

              <label>
                Password
              </label>

              <div className="input-wrapper">

                <span>🔒</span>

                <input
                  type="password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  placeholder="Enter password"
                />

              </div>

            </div>


            {error && (

              <div className="auth-error">
                ⚠️ {error}
              </div>

            )}


            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >

              {loading
                ? "Signing In..."
                : "Sign In →"
              }

            </button>

          </form>


          {/* SIGN UP */}

          <div className="auth-switch">

            <span>
              Don't have an account?
            </span>

            <button
              type="button"
              onClick={onSignUp}
            >
              Sign Up
            </button>

          </div>


          {/* BACK HOME */}

          <button
            type="button"
            className="back-home"
            onClick={onBack}
          >
            ← Back to Home
          </button>

        </div>

      </div>

    </div>

  );
}

export default Login;