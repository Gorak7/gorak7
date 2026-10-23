export type BoardColumn = "todo" | "doing" | "done";
export type BoardCard = { id: string; title: string; column: BoardColumn; updatedAt?: number; version?: number };
export type QueuedMutation = { id: string; type: "card.upsert"; payload: BoardCard; baseVersion?: number; clientTimestamp: number };
const DB_NAME = "syncboard-local-v1";
const DB_VERSION = 1;
function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains("cards")) db.createObjectStore("cards", { keyPath: "id" });
      if (!db.objectStoreNames.contains("outbox")) db.createObjectStore("outbox", { keyPath: "id" });
      if (!db.objectStoreNames.contains("meta")) db.createObjectStore("meta", { keyPath: "key" });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error ?? new Error("Could not open local database"));
  });
}
async function requestResult<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => { request.onsuccess = () => resolve(request.result); request.onerror = () => reject(request.error); });
}
export async function getLocalCards(): Promise<BoardCard[]> {
  const db = await openDB(); try { return await requestResult(db.transaction("cards", "readonly").objectStore("cards").getAll()); } finally { db.close(); }
}
export async function saveLocalCards(cards: BoardCard[]): Promise<void> {
  const db = await openDB(); try { const tx = db.transaction("cards", "readwrite"); const store = tx.objectStore("cards"); for (const card of cards) store.put(card); await new Promise<void>((resolve,reject)=>{tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);}); } finally { db.close(); }
}
export async function enqueueMutation(mutation: QueuedMutation): Promise<void> {
  const db = await openDB(); try { const tx = db.transaction("outbox", "readwrite"); tx.objectStore("outbox").put(mutation); await new Promise<void>((resolve,reject)=>{tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);}); } finally { db.close(); }
}
export async function getOutbox(): Promise<QueuedMutation[]> {
  const db = await openDB(); try { return await requestResult(db.transaction("outbox", "readonly").objectStore("outbox").getAll()); } finally { db.close(); }
}
export async function removeMutation(id: string): Promise<void> {
  const db = await openDB(); try { const tx = db.transaction("outbox", "readwrite"); tx.objectStore("outbox").delete(id); await new Promise<void>((resolve,reject)=>{tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);}); } finally { db.close(); }
}