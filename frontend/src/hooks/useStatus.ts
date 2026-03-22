import { useEffect, useRef, useState } from 'react';
import { StatusData } from '../types/feed';

export const useStatus = () => {
  const [status, setStatus] = useState<StatusData | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new window.WebSocket('ws://localhost:8000/ws/status');
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);
    ws.onmessage = (event) => {
      try {
        setStatus(JSON.parse(event.data));
      } catch {}
    };
    return () => ws.close();
  }, []);

  return {
    status,
    connected,
    lastUpdate: status?.timestamp || null,
    counts: status?.counts || {},
    unenriched: status?.unenriched || 0,
    lastScraped: status?.last_scraped || {},
  };
};
