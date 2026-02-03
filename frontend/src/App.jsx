import { useState } from "react";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [format, setFormat] = useState("pdf");
  const [keepLayout, setKeepLayout] = useState(true);
  const [quality, setQuality] = useState("standard");
  const [embedFonts, setEmbedFonts] = useState(false);
  const [imageResolution, setImageResolution] = useState("300");
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
    form.append("output_format", format);
    form.append("keep_layout", String(keepLayout));
    form.append("quality", quality);
    form.append("embed_fonts", String(embedFonts));
    if (imageResolution) {
      form.append("image_resolution", imageResolution);
    }

    const response = await fetch(`${API_BASE}/api/jobs`, {
      method: "POST",
      body: form
    });

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
          <label>
            Layout fidelity
            <select
              value={keepLayout ? "keep" : "simple"}
              onChange={(e) => setKeepLayout(e.target.value === "keep")}
            >
              <option value="keep">Keep layout</option>
              <option value="simple">Simplify</option>
            </select>
          </label>
          <label>
            Quality
            <select value={quality} onChange={(e) => setQuality(e.target.value)}>
              <option value="standard">Standard</option>
              <option value="high">High</option>
            </select>
          </label>
          <label className="inline">
            <input
              type="checkbox"
              checked={embedFonts}
              onChange={(e) => setEmbedFonts(e.target.checked)}
            />
            Embed fonts
          </label>
          <label>
            Image resolution (DPI)
            <select
              value={imageResolution}
              onChange={(e) => setImageResolution(e.target.value)}
            >
              <option value="150">150</option>
              <option value="300">300</option>
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
