import React, { useEffect, useState } from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function Analytics() {
  // ✅ Hooks MUST be at top level
  const token = localStorage.getItem("token");

  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [unauthorized, setUnauthorized] = useState(false);

  useEffect(() => {
    if (!token) {
      setUnauthorized(true);
      return;
    }

    const fetchTotal = async () => {
      const res = await fetch("https://expense-tracker-backend-74vg.onrender.com/api/analytics/total", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.status === 401) {
        setUnauthorized(true);
        return;
      }

      const data = await res.json();
      setTotal(data.total_expense);
    };

    const fetchCategories = async () => {
      const res = await fetch("https://expense-tracker-backend-74vg.onrender.com/api/analytics/categories", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.status === 401) {
        setUnauthorized(true);
        return;
      }

      const data = await res.json();
      setCategories(Array.isArray(data) ? data : []);
    };

    const fetchMonthly = async () => {
      const res = await fetch("https://expense-tracker-backend-74vg.onrender.com/api/analytics/monthly", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.status === 401) {
        setUnauthorized(true);
        return;
      }

      const data = await res.json();
      setMonthly(Array.isArray(data) ? data : []);
    };

    fetchTotal();
    fetchCategories();
    fetchMonthly();
  }, [token]);

  // ✅ Safe rendering AFTER hooks
  if (unauthorized) {
    localStorage.removeItem("token");
    window.location.reload();
    return null;
  }

  const pieData = {
    labels: categories.map((c) => c.category),
    datasets: [
      {
        data: categories.map((c) => c.total),
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4CAF50",
          "#9C27B0",
        ],
      },
    ],
  };

  return (
    <div style={{ width: "600px", margin: "40px auto" }}>
      <h2>Analytics Dashboard</h2>

      <h3>Total Expense: ₹{total}</h3>

      <h3>Category-wise Spending</h3>
      {categories.length > 0 ? <Pie data={pieData} /> : <p>No data</p>}

      <h3>Monthly Summary</h3>
      <ul>
        {monthly.map((m, index) => (
          <li key={index}>
            {m.month} : ₹{m.total}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Analytics;
