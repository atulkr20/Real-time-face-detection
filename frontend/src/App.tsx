import { useEffect, useRef, useState } from "react";

interface ROI {
  x: number;
  y: number;
  width: number;
  height: number;
  confidence: number;
}

interface StreamMessage {
  frame_number: number;
  roi: ROI | null;
  processed_frame: string;
}

function App() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const intervalRef = useRef<NodeJS.Timer | null>(null);

  const [roi, setRoi] = useState<ROI | null>(null);
  const [frameNumber, setFrameNumber] = useState(0);
  const [connected, setConnected] = useState(false);
  const [processedFrame, setProcessedFrame] = useState<string | null>(null);

  useEffect(() => {
    // connect to webcam
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    });

    // connect to backend websocket
    const ws = new WebSocket("ws://localhost:8000/stream");
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);

    ws.onmessage = (event) => {
      const data: StreamMessage = JSON.parse(event.data);
      setFrameNumber(data.frame_number);
      setRoi(data.roi);
      setProcessedFrame(data.processed_frame);
    };

    return () => {
      ws.close();
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  useEffect(() => {
    if (!connected) return;

    // send a frame every 100ms (10 fps)
    intervalRef.current = setInterval(() => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      if (!canvas || !video || !wsRef.current) return;

      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);

      canvas.toBlob((blob) => {
        if (blob && wsRef.current?.readyState === WebSocket.OPEN) {
          blob.arrayBuffer().then((buf) => {
            wsRef.current?.send(buf);
          });
        }
      }, "image/png");
    }, 100);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [connected]);

  return (
    <div style={{ fontFamily: "monospace", padding: "24px", background: "#0f0f0f", minHeight: "100vh", color: "#fff" }}>
      <h1 style={{ color: "#00ff88" }}>Mega AI — Face Detection Stream</h1>

      <p>Status: <span style={{ color: connected ? "#00ff88" : "#ff4444" }}>{connected ? "Connected" : "Disconnected"}</span></p>
      <p>Frame: {frameNumber}</p>

      {/* hidden video + canvas for capturing frames */}
      <video ref={videoRef} autoPlay muted style={{ display: "none" }} />
      <canvas ref={canvasRef} style={{ display: "none" }} />

      {/* processed frame from backend */}
      <div style={{ display: "flex", gap: "32px", marginTop: "16px" }}>
        <div>
          <p style={{ color: "#aaa" }}>Processed Feed</p>
          {processedFrame ? (
            <img
              src={`data:image/png;base64,${processedFrame}`}
              alt="processed"
              style={{ width: "480px", border: "1px solid #333" }}
            />
          ) : (
            <div style={{ width: "480px", height: "360px", background: "#1a1a1a", display: "flex", alignItems: "center", justifyContent: "center", color: "#555" }}>
              Waiting for stream...
            </div>
          )}
        </div>

        {/* ROI data panel */}
        <div>
          <p style={{ color: "#aaa" }}>ROI Data</p>
          {roi ? (
            <div style={{ background: "#1a1a1a", padding: "16px", borderRadius: "8px", lineHeight: "2" }}>
              <div>X: {roi.x}px</div>
              <div>Y: {roi.y}px</div>
              <div>Width: {roi.width}px</div>
              <div>Height: {roi.height}px</div>
              <div>Confidence: {(roi.confidence * 100).toFixed(1)}%</div>
            </div>
          ) : (
            <div style={{ color: "#555" }}>No face detected</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;