import React, { useCallback, useEffect, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

function Expenses() {
  const token = localStorage.getItem("token");

  const [expenses, setExpenses] = useState([]);
  const [filteredExpenses, setFilteredExpenses] = useState([]);

  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(true);

  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);

  const [selectedMonth, setSelectedMonth] = useState("");

  // ---------------- FETCH EXPENSES ----------------
  const fetchExpenses = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/api/expenses`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();
      setExpenses(data);
      setFilteredExpenses(data);
    } catch (error) {
      console.error("Failed to fetch expenses", error);
    } finally {
      setLoading(false);
    }
  }, [token]); // ✅ API_URL REMOVED (THIS FIXES NETLIFY)

  // ---------------- ADD / UPDATE ----------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    const url = isEditing
      ? `${API_URL}/api/expenses/${editingId}`
      : `${API_URL}/api/expenses`;

    const method = isEditing ? "PUT" : "POST";

    await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ amount, category, note }),
    });

    setAmount("");
    setCategory("");
    setNote("");
    setIsEditing(false);
    setEditingId(null);

    fetchExpenses();
  };

  // ---------------- DELETE ----------------
  const deleteExpense = async (id) => {
    await fetch(`${API_URL}/api/expenses/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchExpenses();
  };

  // ---------------- EDIT ----------------
  const editExpense = (expense) => {
    setAmount(expense.amount);
    setCategory(expense.category);
    setNote(expense.note);
    setEditingId(expense.id);
    setIsEditing(true);
  };

  // ---------------- MONTH FILTER ----------------
  const filterByMonth = (month) => {
    setSelectedMonth(month);

    if (!month) {
      setFilteredExpenses(expenses);
      return;
    }

    const filtered = expenses.filter((e) =>
      e.date.startsWith(month)
    );

    setFilteredExpenses(filtered);
  };

  // ---------------- CSV EXPORT ----------------
  const exportToCSV = () => {
    if (filteredExpenses.length === 0) {
      alert("No expenses to export");
      return;
    }

    const headers = ["Amount", "Category", "Note", "Date"];
    const rows = filteredExpenses.map((e) => [
      e.amount,
      e.category,
      e.note,
      e.date,
    ]);

    const csvContent =
      headers.join(",") +
      "\n" +
      rows.map((row) => row.join(",")).join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "expenses.csv";
    a.click();

    window.URL.revokeObjectURL(url);
  };

  useEffect(() => {
    fetchExpenses();
  }, [fetchExpenses]);

  return (
    <div>
      <h2>My Expenses</h2>

      <div style={{ marginBottom: "15px" }}>
        <label>
          Filter by month:&nbsp;
          <input
            type="month"
            value={selectedMonth}
            onChange={(e) => filterByMonth(e.target.value)}
          />
        </label>

        {selectedMonth && (
          <button
            style={{ marginLeft: "10px" }}
            onClick={() => filterByMonth("")}
          >
            Clear
          </button>
        )}

        <button
          style={{ marginLeft: "20px" }}
          onClick={exportToCSV}
        >
          Export to CSV
        </button>
      </div>

      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
        <br /><br />

        <input
          type="text"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
        />
        <br /><br />

        <input
          type="text"
          placeholder="Note"
          value={note}
          onChange={(e) => setNote(e.target.value)}
        />
        <br /><br />

        <button type="submit">
          {isEditing ? "Update Expense" : "Add Expense"}
        </button>
      </form>

      <hr />

      {loading ? (
        <p>Loading expenses...</p>
      ) : filteredExpenses.length === 0 ? (
        <p style={{ color: "#777" }}>No expenses found.</p>
      ) : (
        <ul>
          {filteredExpenses.map((e) => (
            <li key={e.id} style={{ marginBottom: "8px" }}>
              ₹{e.amount} — {e.category} — {e.note} ({e.date})

              <button
                style={{ marginLeft: "10px" }}
                onClick={() => editExpense(e)}
              >
                Edit
              </button>

              <button
                style={{ marginLeft: "5px" }}
                onClick={() => deleteExpense(e.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Expenses;
