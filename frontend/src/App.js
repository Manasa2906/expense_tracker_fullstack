import React, { useState } from "react";
import Login from "./components/Login";
import Expenses from "./components/Expenses";
import Analytics from "./components/Analytics";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogin = (newToken) => {
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1 style={{ textAlign: "center" }}>Expense Tracker</h1>

      {token ? (
        <>
          <button
            onClick={logout}
            style={{
              float: "right",
              background: "red",
              color: "white",
              padding: "8px",
            }}
          >
            Logout
          </button>

          <Expenses />
          <Analytics />
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
