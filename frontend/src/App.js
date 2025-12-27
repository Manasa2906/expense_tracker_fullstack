import React from "react";
import "./App.css";
import Login from "./components/Login";
import Expenses from "./components/Expenses";
import Analytics from "./components/Analytics";

function App() {
  // ✅ THIS LINE WAS MISSING
  const token = localStorage.getItem("token");

  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
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
        background: "#d32f2f",
        color: "white",
        padding: "8px 12px",
        border: "none",
        borderRadius: "4px",
        cursor: "pointer",
      }}
    >
      Logout
    </button>

    <div style={{ clear: "both", marginTop: "20px" }} />

    <div style={{ border: "1px solid #ddd", padding: "20px", marginBottom: "30px" }}>
      <Expenses />
    </div>

    <div style={{ border: "1px solid #ddd", padding: "20px" }}>
      <Analytics />
    </div>
  </>
) : (
  <Login />
    )}

    </div>
  );
}

export default App;
