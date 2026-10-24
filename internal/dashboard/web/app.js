import { connect, request, forget } from './api.js';
import { byID, show, text, prepareForm, setupInput, chooser } from './forms.js';
let snapshot, configuration = null, review = null, observation = null;
let sequence = 0, seen = '', submitting = false, stopped = false, timer, closeChooser = () => {};
const names = { authorize: 'Awaiting administrator approval in your terminal', inspect: 'Inspecting saved configuration', beginServer: 'Preparing server plan', beginClient: 'Preparing client plan', beginReconnect: 'Preparing reconnect review', beginDetach: 'Preparing disconnect review', checkReadiness: 'Checking actual host readiness', cancelReview: 'Cancelling uncommitted review', commit: 'Applying reviewed host operation' };
function error(e) { text('error', e.message || String(e)); show('error', true); byID('error').focus(); }
function notice(running, authorized, expired) {
  if (stopped) return 'Dashboard stopped. Storage is NOT disconnected. Any admitted host work will drain in the launching terminal.';
  const op = snapshot.operation;
  if (running) return `${names[op?.kind] || 'Submitting operation'}… This can wait for storage; do not start another operation.`;
  if (!authorized) return 'Not authorized. Use the terminal approval step below. Idle authorization expires; no storage is disconnected.';
  if (review) return expired ? 'Review expired. Cancel or inspect configuration and prepare a fresh plan.' : 'Plan prepared — waiting for your explicit approval.';
  if (op?.state === 'incomplete') return 'Operation incomplete. Read the error and inspect saved configuration before deciding how to recover. No rollback is implied.';
  if (configuration?.state === 'pending') return 'Setup is incomplete. Review the saved plan to resume; no automatic repair has run.';
  if (observation?.status?.hostReady) return `Ready at ${new Date(observation.checkedAt).toLocaleString()} — a past observation, not continuous monitoring.`;
  if (configuration?.state === 'empty') return 'Not configured. Prepare a server or client plan below.';
  if (configuration) return 'Configured — readiness is unchecked or incomplete. Check explicitly when ready.';
  return 'Authorized. Inspect configuration to read its current state.';
}
function render() {
  if (!snapshot) return;
  const op = snapshot.operation;
  const running = submitting || op?.state === 'running';
  const authorized = snapshot.authorized;
  const wrongRole = configuration?.role && configuration.role !== snapshot.role;
  const configured = configuration && configuration.state !== 'empty';
  const expired = review && Date.now() >= Date.parse(review.expiresAt);
  text('notice', notice(running, authorized, expired));
  if (!authorized) review = null;
  show('authorization', !authorized && !stopped);
  show('configuration', authorized && !stopped);
  show('setup', authorized && !stopped && !configured && configuration?.state === 'empty' && !review);
  show('review', authorized && !!review && !stopped);
  text('configuration-title', !configuration ? 'Configuration not observed' : configuration.state === 'empty' ? 'No storage configured' : configuration.state === 'pending' ? 'Saved setup is incomplete' : `${configuration.role === 'server' ? 'Server' : 'Client'} configuration`);
  text('configuration-detail', configuration?.connection ? `${configuration.connection.endpoint}:${configuration.connection.export} → ${configuration.connection.mountRoot}${configuration.source ? ` · Source: ${configuration.source}` : ''}` : 'Inspect reads private metadata only. It does not check mounted storage or reconnect it.');
  show('wrong-role', !!wrongRole);
  if (wrongRole) text('wrong-role', `This computer is configured as a ${configuration.role}. Stop this dashboard and run: autobyteus-nfs ${configuration.role}`);
  show('check', !!configured && !wrongRole); show('reconnect', !!configured && !wrongRole); show('detach', !!configured && !wrongRole);
  text('reconnect', configuration?.state === 'pending' ? 'Review saved setup' : 'Review reconnect');
  show('connection-panel', !!configuration?.connection);
  if (configuration?.connection) byID('connection-output').value = JSON.stringify(configuration.connection, null, 2);
  show('observed', !!observation);
  if (observation) { text('checked-at', `${observation.status?.hostReady ? 'Ready' : 'Incomplete'} at ${new Date(observation.checkedAt).toLocaleString()}. Checks are not repeated automatically.`); text('status-json', JSON.stringify(observation.status, null, 2)); }
  for (const id of ['authorize', 'inspect', 'check', 'reconnect', 'detach']) byID(id).disabled = running || !!review || stopped;
  for (const el of byID('setup-form').elements) el.disabled = running || stopped;
  byID('stop').disabled = stopped; byID('copy').disabled = running || stopped;
  if (review) {
    text('review-title', review.kind === 'detach' ? 'Review safe disconnect' : review.kind === 'resume' ? 'Review saved setup' : 'Review this exact plan');
    text('review-deadline', `Review expires ${new Date(review.expiresAt).toLocaleTimeString()}. ${expired ? 'Expired — this plan cannot be applied.' : 'The administrative lock is held until apply, cancel, or expiry.'}`);
    text('review-summary', review.summary.join('\n\n'));
    text('review-connection', JSON.stringify(review.configuration.connection, null, 2));
    show('drain-label', review.kind === 'detach');
    byID('commit').disabled = running || expired || !byID('consent').checked || (review.kind === 'detach' && !byID('drained').checked);
    byID('cancel').disabled = running;
    byID('consent').disabled = running || expired; byID('drained').disabled = running || expired;
    text('commit', review.kind === 'detach' ? 'Disconnect reviewed storage' : 'Apply reviewed plan');
  }
}
function accept(next) {
  snapshot = next; sequence = Math.max(sequence, next.operation?.requestId || 0);
  const op = next.operation;
  if (op && op.state !== 'running' && op.id !== seen) {
    seen = op.id;
    const data = op.data;
    if ((op.kind === 'authorize' || op.kind === 'inspect') && op.state === 'succeeded') { configuration = data; observation = null; }
    if (data?.configuration && ['commit', 'checkReadiness'].includes(op.kind)) configuration = data.configuration;
    if (data?.configuration?.state === 'empty') observation = null;
    if (data?.checkedAt) observation = { checkedAt: data.checkedAt, status: data.status };
    if (op.kind.startsWith('begin') && op.state === 'succeeded') {
      review = data; byID('consent').checked = false; byID('drained').checked = false;
      // A new setup plan is not an installed configuration.
      if (data.kind !== 'setup') configuration = data.configuration;
      render(); byID('review').focus();
    }
    if (op.kind === 'commit' || op.kind === 'cancelReview') review = null;
    if (op.error) error(new Error(`${op.error.detail}${op.error.truncated ? '\n(Error detail truncated.)' : ''}${op.error.effectsMayHaveStarted ? '\nEffects may have started. Inspect saved configuration before deciding how to recover; this is not a rollback.' : ''}`));
    if (data?.retained) text('copy-result', data.retained);
  }
  render();
}
async function poll() {
  if (stopped) return;
  try { accept(await request('/api/state')); }
  catch (e) { error(new Error(`Local dashboard unavailable: ${e.message}. A host operation may still be running. Check the launching terminal; do not force a retry.`)); return; }
  if (!stopped) timer = setTimeout(poll, 800);
}
async function submit(kind, payload = {}) {
  if (submitting || snapshot?.operation?.state === 'running' || stopped) return;
  show('error', false); submitting = true; render();
  try {
    const op = await request('/api/operations', { id: ++sequence, kind, payload });
    snapshot = { ...snapshot, operation: op }; accept(snapshot);
  } catch (e) { error(e); }
  finally { submitting = false; render(); }
}
byID('authorize').onclick = () => submit('authorize');
byID('inspect').onclick = () => submit('inspect');
byID('check').onclick = () => submit('checkReadiness');
byID('reconnect').onclick = () => submit('beginReconnect');
byID('detach').onclick = () => submit('beginDetach');
byID('setup-form').onsubmit = e => { e.preventDefault(); submit(snapshot.role === 'server' ? 'beginServer' : 'beginClient', setupInput(snapshot.role)); };
byID('consent').onchange = render; byID('drained').onchange = render;
byID('commit').onclick = () => { if (review) submit('commit', { leaseId: review.leaseId, consent: byID('consent').checked, drained: byID('drained').checked }); };
byID('cancel').onclick = () => { if (review) submit('cancelReview', { leaseId: review.leaseId }); };
byID('copy').onclick = async () => {
  try { await navigator.clipboard.writeText(byID('connection-output').value); text('copy-result', 'Connection details copied.'); }
  catch { byID('connection-output').focus(); byID('connection-output').select(); text('copy-result', 'Clipboard unavailable. The JSON is selected; copy it manually.'); }
};
byID('stop').onclick = async () => {
  try { await request('/api/stop', {}); stopped = true; clearTimeout(timer); closeChooser(); forget(); render(); }
  catch (e) { error(e); }
};
try {
  const initial = await connect();
  text('role-label', initial.role === 'server' ? 'SERVER · SHARE FROM THIS COMPUTER' : 'CLIENT · USE SHARED STORAGE');
  text('title', initial.role === 'server' ? 'Set up shared storage' : 'Connect this computer');
  text('subtitle', initial.role === 'server' ? 'Choose a folder, review the plan, then share it on your private network.' : 'Use the server’s connection details to mount shared storage locally.');
  document.title = `AutoByteus NFS · ${initial.role === 'server' ? 'Server' : 'Client'} setup`;
  prepareForm(initial.role, initial.platform); closeChooser = chooser(initial.home, error);
  accept(initial); timer = setTimeout(poll, 800);
} catch (e) { text('notice', 'This page is not connected to an authorized local browser session.'); error(e); }
