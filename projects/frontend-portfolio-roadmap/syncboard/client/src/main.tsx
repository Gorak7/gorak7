import React from "react";
import { createRoot } from "react-dom/client";
import { BoardCard, BoardColumn, QueuedMutation, enqueueMutation, getLocalCards, getOutbox, removeMutation, saveLocalCards } from "./offline-store";
import "./style.css";

const wsUrl = import.meta.env.VITE_WS_URL ?? "ws://localhost:3001/ws";
function App() {
  const [cards, setCards] = React.useState<BoardCard[]>([]);
  const [title, setTitle] = React.useState("");
  const [status, setStatus] = React.useState("Loading local board…");
  const [pending, setPending] = React.useState(0);
  const [conflicts, setConflicts] = React.useState<Record<string, { mutation: QueuedMutation; current: BoardCard }>>({});
  const socket = React.useRef<WebSocket | null>(null);
  const cardsRef = React.useRef<BoardCard[]>([]);
  const snapshotReady = React.useRef(false);
  const sending = React.useRef(false);

  const applyCards = React.useCallback((next: BoardCard[]) => {
    cardsRef.current = next;
    setCards(next);
    void saveLocalCards(next).catch(() => setStatus("Local storage unavailable"));
  }, []);

  const transmitOutbox = React.useCallback(async () => {
    const ws = socket.current;
    if (!snapshotReady.current || !ws || ws.readyState !== WebSocket.OPEN || sending.current) return;
    sending.current = true;
    try {
      const queue = await getOutbox();
      setPending(queue.length);
      for (const mutation of queue) {
        if (ws.readyState !== WebSocket.OPEN) break;
        if (conflicts[mutation.payload.id]) continue;
        ws.send(JSON.stringify(mutation));
      }
    } catch {
      setStatus("Could not read offline queue");
    } finally {
      sending.current = false;
    }
  }, [conflicts]);

  React.useEffect(() => {
    let alive = true;
    let retryTimer: number | undefined;
    let reconnectDelay = 1000;
    const loadLocal = async () => {
      try {
        const local = await getLocalCards();
        if (alive && local.length) applyCards(local);
        const queue = await getOutbox();
        if (alive) setPending(queue.length);
      } catch { if (alive) setStatus("Browser storage unavailable"); }
    };
    void loadLocal();

    const connect = () => {
      if (!alive) return;
      setStatus(navigator.onLine ? "Connecting…" : "Offline · changes will be queued");
      const ws = new WebSocket(wsUrl);
      socket.current = ws;
      ws.onopen = () => {
        if (!alive) return;
        reconnectDelay = 1000;
        setStatus("Connected · syncing");
      };
      ws.onmessage = async event => {
        if (!alive) return;
        let message: any;
        try { message = JSON.parse(event.data); } catch { return; }
        if (message.type === "snapshot") {
          snapshotReady.current = true;
          const queue = await getOutbox();
          const merged = new Map<string, BoardCard>((message.cards as BoardCard[]).map(card => [card.id, card]));
          for (const mutation of queue) merged.set(mutation.payload.id, { ...merged.get(mutation.payload.id), ...mutation.payload });
          applyCards([...merged.values()]);
          setStatus("Connected · changes sync across clients");
          await transmitOutbox();
        } else if (message.type === "card.upsert" && message.payload) {
          const card = message.payload as BoardCard;
          applyCards([...cardsRef.current.filter(item => item.id !== card.id), card]);
        } else if (message.type === "ack" && message.id) {
          await removeMutation(message.id);
          const queue = await getOutbox();
          setPending(queue.length);
          setStatus("Connected · all acknowledged changes saved");
        } else if (message.type === "reject" && message.code === "VERSION_CONFLICT" && message.id) {
          const queue = await getOutbox();
          const mutation = queue.find(item => item.id === message.id);
          if (mutation && message.current) {
            setConflicts(prev => ({ ...prev, [mutation.payload.id]: { mutation, current: message.current } }));
            setStatus("Conflict detected · your local edit is preserved for review");
          }
        } else if (message.type === "reject") {
          setStatus(`Server rejected a change: ${message.message ?? message.code}`);
        }
      };
      ws.onclose = () => {
        snapshotReady.current = false;
        if (!alive) return;
        setStatus(navigator.onLine ? "Disconnected · reconnecting" : "Offline · changes are queued");
        retryTimer = window.setTimeout(connect, reconnectDelay);
        reconnectDelay = Math.min(reconnectDelay * 2, 15000);
      };
      ws.onerror = () => ws.close();
    };
    const onOnline = () => { setStatus("Network restored · reconnecting"); if (socket.current?.readyState === WebSocket.OPEN) void transmitOutbox(); };
    const onOffline = () => setStatus("Offline · changes will be queued");
    window.addEventListener("online", onOnline);
    window.addEventListener("offline", onOffline);
    connect();
    return () => {
      alive = false;
      if (retryTimer) window.clearTimeout(retryTimer);
      window.removeEventListener("online", onOnline);
      window.removeEventListener("offline", onOffline);
      socket.current?.close();
    };
  }, [applyCards, transmitOutbox]);

  async function saveMutation(card: BoardCard) {
    const mutation: QueuedMutation = {
      id: crypto.randomUUID(), type: "card.upsert", payload: card,
      baseVersion: card.version ?? 0, clientTimestamp: Date.now()
    };
    await enqueueMutation(mutation);
    const queue = await getOutbox();
    setPending(queue.length);
    if (socket.current?.readyState === WebSocket.OPEN && snapshotReady.current) {
      socket.current.send(JSON.stringify(mutation));
    } else {
      setStatus("Offline · edit saved locally and queued");
    }
  }

  async function addCard(event: React.FormEvent) {
    event.preventDefault();
    const clean = title.trim();
    if (!clean) return;
    const card: BoardCard = { id: crypto.randomUUID(), title: clean, column: "todo", version: 0, updatedAt: Date.now() };
    applyCards([...cardsRef.current, card]);
    setTitle("");
    await saveMutation(card);
  }

  async function move(card: BoardCard, column: BoardColumn) {
    const updated = { ...card, column, updatedAt: Date.now() };
    applyCards(cardsRef.current.map(item => item.id === card.id ? updated : item));
    await saveMutation(updated);
  }

  async function resolveConflict(cardId: string) {
    const conflict = conflicts[cardId];
    if (!conflict) return;
    const rebased = { ...conflict.mutation, baseVersion: conflict.current.version, payload: { ...conflict.mutation.payload, version: conflict.current.version } };
    await enqueueMutation(rebased);
    applyCards([...cardsRef.current.filter(card => card.id !== cardId), { ...rebased.payload, version: conflict.current.version }]);
    setConflicts(prev => { const next = { ...prev }; delete next[cardId]; return next; });
    if (socket.current?.readyState === WebSocket.OPEN) socket.current.send(JSON.stringify(rebased));
    else setStatus("Conflict resolution queued until reconnect");
  }

  const columns: { id: BoardColumn; label: string }[] = [
    { id: "todo", label: "To do" }, { id: "doing", label: "In progress" }, { id: "done", label: "Done" }
  ];
  return <main className="app">
    <header className="top"><div><span className="eyebrow">TEAM WORKSPACE</span><h1>SyncBoard</h1><p>Small steps, shared progress.</p></div><div className="sync-meta"><span className={`status ${status.startsWith("Connected") ? "online" : ""}`}><i/> {status}</span><span className="pending-count">{pending} pending</span></div></header>
    <form className="new-card" onSubmit={addCard}><label htmlFor="new-title">Add a task</label><div><input id="new-title" value={title} onChange={e => setTitle(e.target.value)} placeholder="What needs to get done?" maxLength={160}/><button type="submit">+ Add task</button></div></form>
    {Object.entries(conflicts).map(([id, conflict]) => <aside className="conflict" key={id} role="alert"><div><strong>Another user changed “{conflict.current.title}”.</strong><p>Your edit is saved locally. Choose to keep your edit and submit it on top of the latest version.</p></div><button type="button" onClick={() => void resolveConflict(id)}>Keep my edit</button></aside>)}
    <section className="board" aria-label="Task board">{columns.map(col => <section className="column" key={col.id} aria-labelledby={`heading-${col.id}`}><div className="column-title"><h2 id={`heading-${col.id}`}>{col.label}</h2><span>{cards.filter(card => card.column === col.id).length}</span></div>{cards.filter(card => card.column === col.id).map(card => <article className="task" key={card.id}><p>{card.title}</p><label htmlFor={`move-${card.id}`}>Move task</label><select id={`move-${card.id}`} value={card.column} onChange={e => void move(card, e.target.value as BoardColumn)}><option value="todo">To do</option><option value="doing">In progress</option><option value="done">Done</option></select>{conflicts[card.id] && <span className="conflict-label">Needs conflict resolution</span>}</article>)}{cards.every(card => card.column !== col.id) && <p className="empty">No tasks yet</p>}</section>)}</section>
    <footer>Local edits persist in IndexedDB. Server mutations use IDs and version checks; conflicts require an explicit choice.</footer>
  </main>;
}
if ("serviceWorker" in navigator) window.addEventListener("load", () => { void navigator.serviceWorker.register("/sw.js").catch(() => undefined); });
createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);