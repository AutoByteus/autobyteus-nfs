import { request } from './api.js';
export const byID = (id) => document.getElementById(id);
export const show = (id, visible) => { byID(id).hidden = !visible; };
export const text = (id, value) => { byID(id).textContent = value; };
export function prepareForm(role, platform) {
  show('server-fields', role === 'server'); show('client-fields', role === 'client');
  text('setup-title', role === 'server' ? 'Share a folder from this computer' : 'Connect to shared storage');
  for (const id of ['source', 'endpoint', 'allowlist']) byID(id).required = role === 'server';
  byID('connection-input').required = role === 'client';
  byID('mount-root').value = role === 'server' ? '/Volumes/autobyteus-shared' : '';
  if (role === 'client') {
    byID('mount-root').placeholder = 'Use the mount root in the connection JSON';
    text('mount-hint', 'Optional local override. An occupied directory will not be hidden or replaced.');
  }
  const backends = platform === 'darwin' ? [['apple', 'Native macOS NFS']] : [['ganesha-native', 'Native Linux NFS'], ['ganesha-docker', 'Linux Docker storage engine (advanced)']];
  byID('backend').replaceChildren(...backends.map(([value, label]) => new Option(label, value)));
  byID('backend').onchange = () => show('docker-fields', byID('backend').value === 'ganesha-docker');
}
export function setupInput(role) {
  if (role === 'client') return { connection: byID('connection-input').value, mountRoot: byID('mount-root').value };
  return { source: byID('source').value, endpoint: byID('endpoint').value, allowlist: byID('allowlist').value.split(',').map(s => s.trim()), backend: byID('backend').value, mountRoot: byID('mount-root').value, dockerSocket: byID('backend').value === 'ganesha-docker' ? byID('docker-socket').value : '' };
}
export function chooser(home, reportError) {
  const dialog = byID('chooser'); let listing = null, timer;
  const selection = () => { byID('choose-directory').disabled = !listing || listing.state !== 'complete' || !!listing.error || byID('directory-path').value !== listing.path; };
  byID('directory-path').oninput = selection;
  const render = value => {
    listing = value;
    const running = value.state === 'running';
    text('directory-message', running ? 'Listing directories; a filesystem read may wait. Manual path entry remains available.' : value.error || (value.tooMany ? 'First 200 entries only. Enter a more specific path to continue.' : 'Choose this directory, or open a child directory.'));
    selection();
    byID('directory-parent').disabled = running || !value.parent || value.parent === value.path;
    const buttons = (value.names || []).map(name => {
      const button = document.createElement('button'); button.className = 'secondary'; button.textContent = name;
      button.onclick = () => list(`${value.path === '/' ? '' : value.path}/${name}`); return button;
    });
    byID('directory-list').replaceChildren(...buttons);
    clearTimeout(timer);
    if (running && dialog.open) timer = setTimeout(async () => { try { render(await request('/api/directories')); } catch (e) { reportError(e); } }, 500);
  };
  const list = async path => {
    // Only explicit navigation/submission seeds the field; background results
    // own the listing, never the user's editable path draft.
    byID('directory-path').value = path;
    listing = null; selection();
    byID('directory-parent').disabled = true; byID('directory-list').replaceChildren();
    try { render(await request('/api/directories', { path })); } catch (e) { text('directory-message', e.message); }
  };
  byID('browse').onclick = () => { dialog.showModal(); list(byID('source').value || home); };
  byID('close-chooser').onclick = () => dialog.close(); dialog.onclose = () => clearTimeout(timer);
  byID('directory-form').onsubmit = e => { e.preventDefault(); list(byID('directory-path').value); };
  byID('directory-parent').onclick = () => list(listing.parent);
  byID('choose-directory').onclick = () => { byID('source').value = listing.path; dialog.close(); byID('source').focus(); };
  return () => { clearTimeout(timer); if (dialog.open) dialog.close(); };
}
