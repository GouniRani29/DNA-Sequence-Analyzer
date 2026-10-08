import { useState } from "react";
import { registerUser } from "../services/authService";

function Register({
  onRegister,
  onBackToLogin,
  onBack
}) {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  const handleRegister = async (e) => {

    e.preventDefault();

    setError("");
    setSuccess("");


    if (
      !username ||
      !email ||
      !password ||
      !confirmPassword
    ) {

      setError("Please fill in all fields.");
      return;

    }


    if (password !== confirmPassword) {

      setError("Passwords do not match.");
      return;

    }


    if (password.length < 6) {

      setError(
        "Password must contain at least 6 characters."
      );

      return;

    }


    try {

      setLoading(true);

      const data = await registerUser(
        username,
        email,
        password
      );

      console.log(
        "Registration successful:",
        data
      );

      setSuccess(
        "Account created successfully! You can now login."
      );


      setTimeout(() => {

        onRegister();

      }, 1500);


    } catch (err) {

      console.error(
        "Registration error:",
        err
      );

      setError(
        err.message ||
        "Registration failed. Please try again."
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
              <span>🤖</span>
              <p>AI-Powered Predictions</p>
            </div>

            <div>
              <span>🔒</span>
              <p>Secure & Private</p>
            </div>

          </div>

        </div>


        {/* REGISTER CARD */}

        <div className="auth-card">

          <div className="auth-card-header">

            <div className="auth-small-icon">
              ✨
            </div>

            <h2>
              Create Account
            </h2>

            <p>
              Start analyzing DNA sequences with AI
            </p>

          </div>


          <form onSubmit={handleRegister}>

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


            {/* EMAIL */}

            <div className="auth-field">

              <label>
                Email
              </label>

              <div className="input-wrapper">

                <span>✉️</span>

                <input
                  type="email"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  placeholder="Enter email"
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
                  placeholder="Create password"
                />

              </div>

            </div>


            {/* CONFIRM PASSWORD */}

            <div className="auth-field">

              <label>
                Confirm Password
              </label>

              <div className="input-wrapper">

                <span>🔐</span>

                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) =>
                    setConfirmPassword(e.target.value)
                  }
                  placeholder="Confirm password"
                />

              </div>

            </div>


            {/* ERROR */}

            {error && (

              <div className="auth-error">
                ⚠️ {error}
              </div>

            )}


            {/* SUCCESS */}

            {success && (

              <div className="auth-success">
                ✓ {success}
              </div>

            )}


            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >

              {loading
                ? "Creating Account..."
                : "Create Account →"
              }

            </button>

          </form>


          {/* SIGN IN */}

          <div className="auth-switch">

            <span>
              Already have an account?
            </span>

            <button
              type="button"
              onClick={onBackToLogin}
            >
              Sign In
            </button>

          </div>


          {/* HOME */}

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

export default Register;