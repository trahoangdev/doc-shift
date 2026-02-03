import { useEffect, useMemo, useState } from "react";

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
  const [toast, setToast] = useState(null);
  const [previewKey, setPreviewKey] = useState(0);

  const downloadUrl = useMemo(() => {
    if (!jobId || status !== "completed") return "";
    return `${API_BASE}/api/jobs/${jobId}/download`;
  }, [jobId, status]);

  const previewUrl = useMemo(() => {
    if (!jobId || status !== "completed" || format !== "pdf") return "";
    return `${API_BASE}/api/jobs/${jobId}/preview?ts=${previewKey}`;
  }, [jobId, status, format, previewKey]);

  const submit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError("Please choose a file");
      return;
    }
    setError("");
    setStatus("uploading");
    setPreviewKey(0);

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
    setToast({ type: "info", message: "Job queued. Processing..." });
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
    if (data.status === "completed") {
      setToast({ type: "success", message: "Conversion completed." });
      setPreviewKey((value) => value + 1);
    } else if (data.status === "failed") {
      setToast({ type: "error", message: data.error || "Conversion failed." });
    }
  };

  useEffect(() => {
    if (!jobId) return;
    if (status !== "queued" && status !== "running") return;
    const interval = setInterval(() => {
      refreshStatus();
    }, 2000);
    return () => clearInterval(interval);
  }, [jobId, status]);

  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 4000);
    return () => clearTimeout(timer);
  }, [toast]);

  return (
    <div className="app-shell">
      {toast ? (
        <div className={`toast ${toast.type}`}>
          <span>{toast.message}</span>
          <button type="button" onClick={() => setToast(null)}>
            Dismiss
          </button>
        </div>
      ) : null}

      <header className="hero">
        <div>
          <p className="eyebrow">DocShift</p>
          <h1>Convert. Preserve. Deliver.</h1>
          <p className="lead">
            A focused pipeline for office teams who need clean conversions with
            dependable layout fidelity.
          </p>
          <div className="hero-actions">
            <span className="chip">DOCX ↔ PDF</span>
            <span className="chip">OCR-ready</span>
            <span className="chip">Batch-ready</span>
          </div>
        </div>
        <div className="hero-panel">
          <div className="metric">
            <p>Avg. processing</p>
            <h3>&lt; 30s</h3>
          </div>
          <div className="metric">
            <p>Success target</p>
            <h3>98%</h3>
          </div>
          <div className="metric">
            <p>Retention window</p>
            <h3>7 days</h3>
          </div>
        </div>
      </header>

      <main className="grid">
        <section className="panel">
          <div className="panel-head">
            <h2>Upload & Convert</h2>
            <p>Keep your structure intact with conversion presets.</p>
          </div>
          <form onSubmit={submit} className="form">
            <label className="field full">
              <span>Choose file</span>
              <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            </label>

            <div className="field-row">
              <label className="field">
                <span>Output format</span>
                <select value={format} onChange={(e) => setFormat(e.target.value)}>
                  <option value="pdf">PDF</option>
                  <option value="docx">DOCX</option>
                </select>
              </label>
              <label className="field">
                <span>Quality</span>
                <select value={quality} onChange={(e) => setQuality(e.target.value)}>
                  <option value="standard">Standard</option>
                  <option value="high">High</option>
                </select>
              </label>
            </div>

            <div className="field-row">
              <label className="field">
                <span>Layout fidelity</span>
                <select
                  value={keepLayout ? "keep" : "simple"}
                  onChange={(e) => setKeepLayout(e.target.value === "keep")}
                >
                  <option value="keep">Keep layout</option>
                  <option value="simple">Simplify</option>
                </select>
              </label>
              <label className="field">
                <span>Image resolution</span>
                <select
                  value={imageResolution}
                  onChange={(e) => setImageResolution(e.target.value)}
                >
                  <option value="150">150 DPI</option>
                  <option value="300">300 DPI</option>
                </select>
              </label>
            </div>

            <div className="field-row align">
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={embedFonts}
                  onChange={(e) => setEmbedFonts(e.target.checked)}
                />
                <span>Embed fonts</span>
              </label>
              <div className="helper">
                <p>Best for sharing externally</p>
              </div>
            </div>

            {error ? <p className="error">{error}</p> : null}
            <button type="submit" className="primary full">
              Start conversion
            </button>
          </form>
        </section>

        <section className="panel status">
          <div className="status-head">
            <h2>Job status</h2>
            <span className={`pill ${status}`}>{status}</span>
          </div>
          <div className="status-body">
            <p>Job ID</p>
            <strong>{jobId || "-"}</strong>
          </div>
          {downloadUrl ? (
            <a className="download" href={downloadUrl}>
              Download result
            </a>
          ) : null}
          <button type="button" className="ghost" onClick={refreshStatus} disabled={!jobId}>
            Refresh status
          </button>

          {previewUrl ? (
            <div className="preview">
              <h3>Preview</h3>
              <img src={previewUrl} alt="PDF preview" />
            </div>
          ) : null}
        </section>
      </main>
    </div>
  );
}
