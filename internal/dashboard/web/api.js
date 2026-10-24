// Only local, typed endpoints. The browser never sends an OS command or user ID.
const storageKey = 'autobyteus-nfs-dashboard';
let token = '';
export async function request(path, value) {
  const response = await fetch(path, {
    method: value === undefined ? 'GET' : 'POST',
    cache: 'no-store', credentials: 'omit',
    headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(value === undefined ? {} : { 'Content-Type': 'application/json' }) },
    ...(value === undefined ? {} : { body: JSON.stringify(value) }),
  });
  if (!response.ok) throw new Error((await response.text()).trim() || 'Local request refused');
  return response.json();
}
export async function connect() {
  const secret = location.hash.slice(1);
  history.replaceState(null, '', location.pathname);
  if (secret) {
    const reply = await request('/api/session', { secret });
    token = reply.token;
    sessionStorage.setItem(storageKey, token);
  } else {
    token = sessionStorage.getItem(storageKey) || '';
  }
  if (!token) throw new Error('Open the private one-time URL from your launching terminal. This tab has no session.');
  return request('/api/state');
}
export function forget() { token = ''; sessionStorage.removeItem(storageKey); }
