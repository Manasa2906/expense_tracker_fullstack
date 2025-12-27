import React, { useEffect, useState } from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const API_URL = process.env.REACT_APP_API_URL;

function Analytics() {
  const token = localStorage.getItem("token");

  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    if (!token) return;

    const headers = {
      Authorization: `Bearer ${token}`,
    };

    // Fetch total
    fetch(`${API_URL}/api/analytics/total`, { headers })
      .then((res) => res.json())
      .then((data) => setTotal(data.total || 0))
      .catch(() => setTotal(0));

    // Fetch categories
    fetch(`${API_URL}/api/analytics/categories`, { headers })
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch(() => setCategories([]));
  }, [token]);

  const chartData = {
    labels: categories.map((c) => c.category),
    datasets: [
      {
        data: categories.map((c) => c.amount),
        backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
      },
    ],
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h2>Analytics Dashboard</h2>
      <h3>Total Expense: ₹{total}</h3>

      {categories.length > 0 && (
        <Pie data={chartData} />
      )}
    </div>
  );
}

export default Analytics;
