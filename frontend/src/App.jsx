import { useState } from "react";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [format, setFormat] = useState("pdf");
  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError("Please choose a file");
      return;
    }
    setError("");
    setStatus("uploading");

    const form = new FormData();
    form.append("file", file);

    const response = await fetch(
      `${API_BASE}/api/jobs?output_format=${format}`,
      { method: "POST", body: form }
    );

    if (!response.ok) {
      setStatus("error");
      setError("Failed to create job");
      return;
    }

    const data = await response.json();
    setJobId(data.job_id);
    setStatus("queued");
  };

  const refreshStatus = async () => {
    if (!jobId) return;
    const response = await fetch(`${API_BASE}/api/jobs/${jobId}`);
    if (!response.ok) {
      setError("Failed to fetch status");
      return;
    }
    const data = await response.json();
    setStatus(data.status);
  };

  return (
    <div className="page">
      <header>
        <h1>DocShift</h1>
        <p>Convert documents while keeping layout intact.</p>
      </header>
      <main>
        <form onSubmit={submit} className="card">
          <label>
            Choose file
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          </label>
          <label>
            Output format
            <select value={format} onChange={(e) => setFormat(e.target.value)}>
              <option value="pdf">PDF</option>
              <option value="docx">DOCX</option>
            </select>
          </label>
          <button type="submit">Start conversion</button>
          {error ? <p className="error">{error}</p> : null}
        </form>
        <section className="card">
          <h2>Job status</h2>
          <p>Status: {status}</p>
          <p>Job ID: {jobId || "-"}</p>
          <button type="button" onClick={refreshStatus} disabled={!jobId}>
            Refresh
          </button>
        </section>
      </main>
    </div>
  );
}
