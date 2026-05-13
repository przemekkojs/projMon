import React, { useEffect, useState } from "react";
import "./style.css";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [form, setForm] = useState({
    power_kw: "",
    yearly_consumption_kwh: "",
    location: "",
    control_type: "",
    night_reduction_percent: ""
  });

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function analyze(e) {
    e.preventDefault();

    const res = await fetch(`${API}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        power_kw: Number(form.power_kw),
        yearly_consumption_kwh: Number(form.yearly_consumption_kwh),
        location: form.location,
        control_type: form.control_type,
        night_reduction_percent: Number(form.night_reduction_percent)
      })
    });

    const data = await res.json();
    setResult(data);
    loadHistory();
  }

  async function loadHistory() {
    const res = await fetch(`${API}/history`);
    const data = await res.json();
    setHistory(data);
  }

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>EnergyApp</h2>
        <p>Panel analizy instalacji</p>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <h1>Analiza zużycia energii</h1>
            <p>Obliczenia, walidacja i historia wyników</p>
          </div>
        </header>

        <section className="grid">
          <form className="card form-card" onSubmit={analyze}>
            <h2>Dane instalacji</h2>

            <input name="power_kw" placeholder="Moc instalacji [kW]" onChange={handleChange} />
            <input name="yearly_consumption_kwh" placeholder="Roczne zużycie [kWh]" onChange={handleChange} />
            <input name="location" placeholder="Lokalizacja" onChange={handleChange} />
            <input name="control_type" placeholder="Typ sterowania" onChange={handleChange} />
            <input name="night_reduction_percent" placeholder="Redukcja nocna [%]" onChange={handleChange} />

            <button>Przeanalizuj instalację</button>
          </form>

          {result && (
            <div className="card result-card">
              <h2>Wynik analizy</h2>

              <div className="stats">
                <div>
                  <span>Roczne zużycie</span>
                  <strong>{result.yearly_consumption.toFixed(2)} kWh</strong>
                </div>

                <div>
                  <span>Szacowana moc</span>
                  <strong>{result.estimated_power.toFixed(2)} kW</strong>
                </div>

                <div>
                  <span>Status</span>
                  <strong className={`status ${result.status.toLowerCase()}`}>
                    {result.status}
                  </strong>
                </div>
              </div>

              <h3>Miesięczne zużycie</h3>
              <BarChart data={result.monthly_consumption} />
            </div>
          )}
        </section>

        <section className="card">
          <h2>Historia analiz</h2>

          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Moc</th>
                <th>Zużycie</th>
                <th>Status</th>
                <th>Data</th>
              </tr>
            </thead>

            <tbody>
              {history.map((x) => (
                <tr key={x.id}>
                  <td>#{x.id}</td>
                  <td>{x.power_kw} kW</td>
                  <td>{x.yearly_consumption} kWh</td>
                  <td>
                    <span className={`badge ${x.status.toLowerCase()}`}>
                      {x.status}
                    </span>
                  </td>
                  <td>{String(x.timestamp).slice(0, 19)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

function BarChart({ data }) {
  const values = Object.values(data);
  const max = Math.max(...values);

  return (
    <div className="chart">
      {Object.entries(data).map(([month, value]) => (
        <div className="bar-wrapper" key={month}>
          <div
            className="bar"
            style={{ height: `${(value / max) * 140}px` }}
            title={`${value.toFixed(2)} kWh`}
          />
          <span>{month}</span>
        </div>
      ))}
    </div>
  );
}