import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Polygon,
  Popup,
} from "react-leaflet";
import { cellToBoundary } from "h3-js";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import {
  Map,
  Activity,
  Users,
  Store,
  LayoutDashboard,
  MapPinned,
  TrendingUp,
} from "lucide-react";
import "leaflet/dist/leaflet.css";
import "./App.css";

const zones = [
  { name: "BKC", pings: 23859 },
  { name: "Andheri", pings: 22050 },
  { name: "Dadar", pings: 20522 },
  { name: "Fort", pings: 17163 },
  { name: "Powai", pings: 16406 },
];

const hourlyData = [
  { hour: "12 AM", traffic: 2500 },
  { hour: "4 AM", traffic: 1200 },
  { hour: "8 AM", traffic: 10203 },
  { hour: "12 PM", traffic: 4200 },
  { hour: "4 PM", traffic: 6500 },
  { hour: "6 PM", traffic: 10110 },
  { hour: "10 PM", traffic: 3500 },
];

const metricStyles = {
  total_pings: {
    label: "Total GPS Pings",
    stroke: "#0369a1",
    low: "#bae6fd",
    mid: "#0ea5e9",
    high: "#075985",
  },
  unique_devices: {
    label: "Unique Devices",
    stroke: "#7e22ce",
    low: "#e9d5ff",
    mid: "#a855f7",
    high: "#581c87",
  },
};

function App() {
  const [h3Cells, setH3Cells] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mapMetric, setMapMetric] = useState("total_pings");

  useEffect(() => {
    fetch("/data/h3_mobility_aggregation.csv")
      .then((response) => {
        if (!response.ok) {
          throw new Error("H3 dataset could not be loaded");
        }
        return response.text();
      })
      .then((csv) => {
        const rows = csv.trim().split(/\r?\n/).slice(1);
        const cells = rows
          .filter((row) => row.trim() !== "")
          .map((row) => {
            const [
              h3_index,
              total_pings,
              unique_devices,
              avg_latitude,
              avg_longitude,
            ] = row.split(",");

            return {
              h3_index,
              total_pings: Number(total_pings),
              unique_devices: Number(unique_devices),
              avg_latitude: Number(avg_latitude),
              avg_longitude: Number(avg_longitude),
            };
          })
          .filter(
            (cell) =>
              cell.h3_index &&
              Number.isFinite(cell.total_pings) &&
              Number.isFinite(cell.unique_devices),
          );

        setH3Cells(cells);
      })
      .catch((err) => {
        console.error("H3 loading error:", err);
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const metricStyle = metricStyles[mapMetric];
  const maxMetricValue = Math.max(
    1,
    ...h3Cells.map((cell) => cell[mapMetric] || 0),
  );

  return (
    <div className="app">
      <aside className="sidebar">
        <h2 className="logo">
          Geo<span>Pulse</span>
        </h2>
        <p className="subtitle">RETAIL MOBILITY ANALYTICS</p>

        <nav>
          <button className="active">
            <LayoutDashboard /> Overview
          </button>
          <button>
            <MapPinned /> Mobility Map
          </button>
          <button>
            <Store /> Store Analytics
          </button>
          <button>
            <TrendingUp /> Footfall Trends
          </button>
        </nav>

        <div className="sidebar-footer">
          <Activity size={18} />
          <span>GeoPulse Analytics</span>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>Mobility Overview</h1>
            <p>Hyper-local retail intelligence · Mumbai, India</p>
          </div>
          <span className="live">● SYSTEM ONLINE</span>
        </header>

        <section className="kpis">
          <div className="kpi">
            <Activity />
            <p>Total GPS Pings</p>
            <h2>100,000</h2>
            <small>Across 5 Mumbai zones</small>
          </div>
          <div className="kpi">
            <Users />
            <p>Unique Devices</p>
            <h2>10,000</h2>
            <small>10 pings per device</small>
          </div>
          <div className="kpi">
            <Store />
            <p>Retail Stores</p>
            <h2>10</h2>
            <small>Across 5 zones</small>
          </div>
          <div className="kpi">
            <Map />
            <p>Peak Traffic</p>
            <h2>8 AM</h2>
            <small>10,203 GPS pings</small>
          </div>
        </section>

        <section className="content-grid">
          <div className="panel map-panel">
            <div className="panel-heading">
              <div>
                <h3>Mumbai H3 Hotspot Map</h3>
                <p>Hexagonal GPS activity distribution</p>
              </div>
              <MapPinned />
            </div>

            {loading && <p>Loading H3 hotspots...</p>}
            {error && <p>{error}</p>}

            <div className="map-controls">
              <label htmlFor="mapMetric">View hotspots by:</label>
              <select
                id="mapMetric"
                value={mapMetric}
                onChange={(event) => setMapMetric(event.target.value)}
              >
                <option value="total_pings">Total GPS Pings</option>
                <option value="unique_devices">Unique Devices</option>
              </select>
            </div>

            <MapContainer
              center={[19.076, 72.8777]}
              zoom={11}
              scrollWheelZoom
              className="mobility-map"
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {h3Cells.map((cell) => {
                const boundary = cellToBoundary(cell.h3_index);
                const selectedValue = Math.max(0, cell[mapMetric] || 0);
                const intensity = Math.sqrt(selectedValue / maxMetricValue);
                const fillOpacity = 0.18 + intensity * 0.72;

                return (
                  <Polygon
                    key={cell.h3_index}
                    positions={boundary}
                    pathOptions={{
                      color: metricStyle.stroke,
                      weight: 1.5,
                      fillColor: metricStyle.mid,
                      fillOpacity,
                    }}
                  >
                    <Popup>
                      <strong>H3 Cell</strong>
                      <br />
                      {cell.h3_index}
                      <br />
                      <br />
                      <strong>GPS Pings:</strong>{" "}
                      {cell.total_pings.toLocaleString()}
                      <br />
                      <strong>Unique Devices:</strong>{" "}
                      {cell.unique_devices.toLocaleString()}
                      <br />
                      <strong>Latitude:</strong>{" "}
                      {cell.avg_latitude.toFixed(5)}
                      <br />
                      <strong>Longitude:</strong>{" "}
                      {cell.avg_longitude.toFixed(5)}
                    </Popup>
                  </Polygon>
                );
              })}
            </MapContainer>

            <div className="map-legend">
              <span>Low {metricStyle.label.toLowerCase()}</span>
              <div
                className="legend-gradient"
                style={{
                  background: `linear-gradient(to right, ${metricStyle.low}, ${metricStyle.mid}, ${metricStyle.high})`,
                }}
              />
              <span>High {metricStyle.label.toLowerCase()}</span>
            </div>

            <p>H3 cells loaded: {h3Cells.length}</p>
          </div>

          <div className="panel">
            <div className="panel-heading">
              <div>
                <h3>Hourly Traffic</h3>
                <p>GPS activity distribution</p>
              </div>
              <Activity />
            </div>

            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={hourlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#263449" />
                <XAxis dataKey="hour" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Bar
                  dataKey="traffic"
                  fill="#38bdf8"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel zone-panel">
          <h3>Zone-wise Mobility Analysis</h3>
          <p>GPS ping distribution by location</p>

          <table>
            <thead>
              <tr>
                <th>Zone</th>
                <th>Total Pings</th>
                <th>Share</th>
              </tr>
            </thead>
            <tbody>
              {zones.map((zone) => (
                <tr key={zone.name}>
                  <td>{zone.name}</td>
                  <td>{zone.pings.toLocaleString()}</td>
                  <td>{((zone.pings / 100000) * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default App;