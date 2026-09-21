const sampleSales = [];
let salesData = [];
const storedProfile = JSON.parse(localStorage.getItem('northstar-profile') || 'null');
const profileState = storedProfile || { name: 'Jordan Davis', role: 'Admin' };
const profileInitials = name => name.split(' ').map(part => part[0]).join('').slice(0, 2).toUpperCase();
const money = value => !value ? '0 FCFA' : value >= 1000000 ? `${(value / 1000000).toFixed(1)} M FCFA` : `${(value / 1000).toFixed(1)} k FCFA`;
const iconMap = ['wallet-cards', 'shopping-bag', 'user-round-check', 'percent'];
const metricData = () => {
  const revenue = salesData.reduce((sum, row) => sum + row.revenue, 0) * 1.44;
  const orders = salesData.reduce((sum, row) => sum + row.orders, 0) * 3;
  const customers = salesData.length;
  return [
    { label: 'Total revenue', value: money(revenue), change: '0.0%', detail: 'vs last period', tone: 'teal' },
    { label: 'Total orders', value: orders.toLocaleString(), change: '0.0%', detail: 'vs last period', tone: 'yellow' },
    { label: 'Active customers', value: customers.toLocaleString(), change: '0.0%', detail: 'vs last period', tone: 'blue' },
    { label: 'Avg. order value', value: money(revenue / orders), change: '0.0%', detail: 'vs last period', tone: 'coral' }
  ];
};
function renderMetrics() {
  document.querySelector('#metricGrid').innerHTML = metricData().map((metric, index) => `<article class="metric-card"><div class="metric-top"><span>${metric.label}</span><span class="metric-icon ${metric.tone}"><i data-lucide="${iconMap[index]}"></i></span></div><div class="metric-value">${metric.value}</div><div class="metric-bottom"><strong class="${metric.negative ? 'negative' : 'positive'}">${metric.change}</strong><span>${metric.detail}</span></div></article>`).join('');
  const customerBadge = document.querySelector('.nav-item[data-view="customers"] .nav-count');
  if (customerBadge) customerBadge.textContent = salesData.length;
  lucide.createIcons();
}
function renderCustomers() {
  document.querySelector('#customerTable').innerHTML = salesData.length ? salesData.slice(0, 5).map((row, index) => `<tr><td><div class="customer-cell"><span class="customer-logo ${['', 'alt', 'blue', 'yellow', 'alt'][index]}">${row.customer.slice(0, 2).toUpperCase()}</span><strong>${row.customer}</strong></div></td><td>${row.orders}</td><td><strong>${money(row.revenue)}</strong></td><td><span class="${row.growth < 0 ? 'negative' : 'growth'}">${row.growth > 0 ? '+' : ''}${row.growth}%</span></td><td><button class="row-more" aria-label="More options"><i data-lucide="more-horizontal"></i></button></td></tr>`).join('') : '<tr><td colspan="5"><div class="empty-state compact"><i data-lucide="database"></i><strong>No customer data yet</strong><span>Import a CSV to populate this table.</span></div></td></tr>';
  lucide.createIcons();
}
function renderChannels() {
  const totals = salesData.reduce((result, row) => { result[row.channel] = (result[row.channel] || 0) + row.revenue; return result; }, {});
  const colors = ['#0b8f81', '#81a8e9', '#f6c84c', '#f08f74'];
  const total = Object.values(totals).reduce((sum, value) => sum + value, 0);
  document.querySelector('.donut').classList.toggle('empty', !total);
  document.querySelector('.donut-center strong').textContent = money(total);
  document.querySelector('#channelList').innerHTML = total ? Object.entries(totals).slice(0, 4).map(([name, value], index) => `<div class="channel-item"><i style="background:${colors[index]}"></i><span>${name}</span><strong>${Math.round(value / total * 100)}%</strong></div>`).join('') : '<div class="empty-state compact"><strong>No channel data yet</strong><span>Import sales to see mix.</span></div>';
}
function resetZeroOverview() {
  const chart = document.querySelector('.revenue-chart');
  if (chart) {
    chart.querySelector('.target-path').setAttribute('d', 'M0 220 L700 220');
    chart.querySelector('.area-path').setAttribute('d', 'M0 220 L700 220 L700 240 L0 240 Z');
    chart.querySelector('.line-path').setAttribute('d', 'M0 220 L700 220');
    chart.querySelector('.last-point').setAttribute('cy', '220');
  }
  document.querySelectorAll('.y-axis span').forEach(label => { label.textContent = '0 FCFA'; });
  const insight = document.querySelector('.insight-strip');
  if (insight) { insight.querySelector('strong').textContent = 'Your workspace is ready'; insight.querySelector('span').textContent = 'Import sales data to unlock revenue insights and management reporting.'; insight.querySelector('.strip-action').textContent = 'Import data'; }
  const footer = document.querySelector('.channel-footer span');
  if (footer) footer.innerHTML = '<i data-lucide="minus"></i> 0.0% <small>vs last period</small>';
  if (footer) lucide.createIcons();
  const activity = document.querySelector('.activity-list');
  if (activity) activity.innerHTML = '<div class="empty-state compact"><i data-lucide="clock-3"></i><strong>No activity yet</strong><span>Your workspace activity will appear here.</span></div>';
  const syncHint = document.querySelector('.upload-hint');
  if (syncHint) syncHint.textContent = 'Awaiting first import';
  lucide.createIcons();
}
function showToast(message) {
  const toast = document.querySelector('#toast');
  toast.querySelector('span').textContent = message;
  toast.classList.add('visible');
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => toast.classList.remove('visible'), 3200);
}
function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) throw new Error('The CSV needs a header and at least one row.');
  const headers = lines.shift().split(',').map(header => header.trim().toLowerCase());
  return lines.map(line => {
    const values = line.split(',').map(value => value.trim().replace(/^"|"$/g, ''));
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index] || '']));
    const revenue = Number(String(row.revenue || row.sales || row.amount).replace(/[$,]/g, ''));
    const orders = Number(row.orders || row.order_count || 1);
    if (!row.customer || Number.isNaN(revenue)) return null;
    return { customer: row.customer, orders: Number.isNaN(orders) ? 1 : orders, revenue, growth: Number(row.growth || 0), channel: row.channel || 'Direct' };
  }).filter(Boolean);
}
function exportReport() {
  const rows = [['Customer', 'Orders', 'Revenue (FCFA)', 'Growth', 'Channel'], ...salesData.map(row => [row.customer, row.orders, row.revenue, `${row.growth}%`, row.channel])];
  const blob = new Blob([rows.map(row => row.join(',')).join('\n')], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a'); link.href = url; link.download = 'northstar-management-report.csv'; link.click(); URL.revokeObjectURL(url);
  showToast('Management report exported');
}
document.querySelector('#fileInput').addEventListener('change', event => {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => { try { const imported = parseCsv(reader.result); if (!imported.length) throw new Error('No usable rows found.'); salesData = imported; renderMetrics(); renderCustomers(); renderChannels(); showToast(`${imported.length} sales rows imported`); } catch (error) { showToast(error.message); } };
  reader.readAsText(file);
});
document.querySelector('#exportBtn').addEventListener('click', exportReport);
document.querySelector('#periodSelect').addEventListener('change', event => showToast(`Showing performance for the last ${event.target.value === '365' ? 'year' : event.target.value + ' days'}`));
document.querySelector('#insightBtn').addEventListener('click', () => showToast('EMEA softened 4.2% over the last two weeks'));
document.querySelector('.strip-close').addEventListener('click', event => event.currentTarget.closest('.insight-strip').remove());
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => { document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active')); const navItem = button.closest('.nav-item'); if (navItem) navItem.classList.add('active'); showToast(`${button.dataset.view[0].toUpperCase() + button.dataset.view.slice(1)} view selected`); }));
renderMetrics(); renderCustomers(); renderChannels(); lucide.createIcons();

const overviewMarkup = document.querySelector('#pageContent').innerHTML;
const pageTemplates = {
  customers: `<section class="page-heading"><div><p class="eyebrow">Relationship management</p><h1>Customers</h1><p class="subtitle">Track account health, value, and retention in one place.</p></div><button class="button button-dark" data-action="add-customer"><i data-lucide="user-plus"></i>Add customer</button></section><section class="enterprise-grid"><article class="panel stat-panel"><span>Managed accounts</span><strong>${salesData.length}</strong><small>Awaiting import</small></article><article class="panel stat-panel"><span>Customer revenue</span><strong>${money(salesData.reduce((sum, row) => sum + row.revenue, 0))}</strong><small>Current workspace</small></article><article class="panel stat-panel"><span>At-risk accounts</span><strong>0</strong><small>No data loaded</small></article></section><article class="panel data-panel"><div class="panel-heading"><div><h2>Customer directory</h2><p>Searchable account register and performance summary</p></div><label class="search-field"><i data-lucide="search"></i><input placeholder="Search customers" data-table-search="customers"></label></div><div class="table-wrap"><table><thead><tr><th>Customer</th><th>Orders</th><th>Revenue</th><th>Growth</th><th>Status</th></tr></thead><tbody>${salesData.length ? salesData.map(row => `<tr><td><strong>${row.customer}</strong></td><td>${row.orders}</td><td>${money(row.revenue)}</td><td>${row.growth}%</td><td><span class="status-pill">Active</span></td></tr>`).join('') : '<tr><td colspan="5"><div class="empty-state"><i data-lucide="users"></i><strong>No customers to display</strong><span>Import your sales data or add a customer to begin.</span><button class="button button-light" data-action="import">Import data</button></div></td></tr>'}</tbody></table></div></article>`,
  products: `<section class="page-heading"><div><p class="eyebrow">Catalog intelligence</p><h1>Products</h1><p class="subtitle">Monitor product performance, margin, and inventory signals.</p></div><button class="button button-dark" data-action="add-product"><i data-lucide="plus"></i>New product</button></section><section class="enterprise-grid"><article class="panel stat-panel"><span>Active products</span><strong>0</strong><small>Catalog is empty</small></article><article class="panel stat-panel"><span>Units sold</span><strong>0</strong><small>Current period</small></article><article class="panel stat-panel"><span>Gross margin</span><strong>0%</strong><small>Awaiting product data</small></article></section><article class="panel data-panel"><div class="panel-heading"><div><h2>Product catalog</h2><p>Products become visible when sales data includes a product column.</p></div><button class="text-button" data-action="import">Import product data <i data-lucide="arrow-up-right"></i></button></div><div class="empty-state page-empty"><i data-lucide="package-open"></i><strong>No products yet</strong><span>Connect a source or import a CSV with product, units, and revenue columns.</span></div></article>`,
  reports: `<section class="page-heading"><div><p class="eyebrow">Decision support</p><h1>Reports</h1><p class="subtitle">Create polished, shareable reporting packs for your leadership team.</p></div><button class="button button-dark" data-action="create-report"><i data-lucide="file-plus-2"></i>Create report</button></section><article class="panel report-builder"><div><span class="section-kicker">Report builder</span><h2>Build a management report</h2><p>Select the sections your stakeholders need and export a clean CSV summary.</p></div><div class="report-options"><label><input type="checkbox" checked> Executive summary</label><label><input type="checkbox" checked> Revenue performance</label><label><input type="checkbox" checked> Customer analysis</label><label><input type="checkbox"> Product margin</label></div><button class="button button-light" data-action="export"><i data-lucide="download"></i>Export current report</button></article><div class="section-title"><div><h2>Saved reports</h2><p>Reusable reporting views for your team</p></div></div><section class="report-grid"><article class="panel report-card"><div class="report-icon teal-bg"><i data-lucide="presentation"></i></div><div><strong>Weekly executive brief</strong><span>Not generated yet</span></div><button data-action="create-report"><i data-lucide="play"></i></button></article><article class="panel report-card"><div class="report-icon blue-bg"><i data-lucide="users"></i></div><div><strong>Customer health report</strong><span>Not generated yet</span></div><button data-action="create-report"><i data-lucide="play"></i></button></article></section>`,
  data: `<section class="page-heading"><div><p class="eyebrow">Connections & ingestion</p><h1>Data sources</h1><p class="subtitle">Control how sales data enters your reporting workspace.</p></div><label class="button button-dark"><i data-lucide="upload"></i>Import CSV<input type="file" id="pageFileInput" accept=".csv,text/csv" hidden></label></section><section class="source-grid"><article class="panel source-card connected"><div class="source-icon"><i data-lucide="file-spreadsheet"></i></div><div><strong>CSV upload</strong><span>Manual file ingestion</span></div><span class="source-status">Ready</span><div class="source-progress"><i></i></div><small>Upload a CSV with customer, revenue, orders, growth, and channel columns.</small></article><article class="panel source-card"><div class="source-icon"><i data-lucide="cloud"></i></div><div><strong>Cloud warehouse</strong><span>Snowflake, BigQuery, Redshift</span></div><button class="text-button" data-action="connect">Connect</button><small>Sync enterprise data on a schedule.</small></article><article class="panel source-card"><div class="source-icon"><i data-lucide="plug"></i></div><div><strong>CRM connector</strong><span>Salesforce, HubSpot</span></div><button class="text-button" data-action="connect">Connect</button><small>Bring account ownership and lifecycle data together.</small></article></section><article class="panel data-panel"><div class="panel-heading"><div><h2>Data quality</h2><p>Validation checks for the current workspace</p></div><span class="status-pill neutral">No records</span></div><div class="quality-list"><span><i data-lucide="circle-check"></i> Required columns</span><strong>Waiting for import</strong><span><i data-lucide="circle-check"></i> Duplicate check</span><strong>Waiting for import</strong><span><i data-lucide="circle-check"></i> Last refresh</span><strong>Never</strong></div></article>`,
  settings: `<section class="page-heading"><div><p class="eyebrow">Workspace administration</p><h1>Settings</h1><p class="subtitle">Configure workspace preferences, targets, and team access.</p></div><button class="button button-dark" data-action="save-settings"><i data-lucide="save"></i>Save changes</button></section><section class="settings-layout"><aside class="panel settings-tabs"><button class="active">Workspace</button><button>Targets</button><button>Team access</button><button>Notifications</button></aside><article class="panel settings-form"><div><h2>Workspace preferences</h2><p>Make Northstar fit the way your team operates.</p></div><label>Workspace name<input value="Acme Corp" data-setting="workspace"></label><label>Currency<select data-setting="currency"><option>XAF — Franc CFA (Cameroon)</option><option>EUR — Euro</option><option>USD — United States Dollar</option></select></label><label>Monthly revenue target<input type="number" value="0" min="0" data-setting="target"></label><label class="toggle-row"><span><strong>Weekly email digest</strong><small>Send a summary every Monday morning.</small></span><input type="checkbox" checked data-setting="digest"></label></article></section>`
};

function renderPage(view) {
  closeHeaderPanels();
  const page = document.querySelector('#pageContent');
  page.innerHTML = view === 'overview' ? overviewMarkup : pageTemplates[view] || pageTemplates.overview;
  document.querySelector('.breadcrumbs strong').textContent = view[0].toUpperCase() + view.slice(1);
  document.querySelectorAll('.nav-item').forEach(item => item.classList.toggle('active', item.dataset.view === view));
  lucide.createIcons();
  if (view === 'overview') { renderMetrics(); renderCustomers(); renderChannels(); resetZeroOverview(); }
}

document.addEventListener('click', event => {
  const nav = event.target.closest('[data-view]');
  if (nav) { event.preventDefault(); renderPage(nav.dataset.view); return; }
  const action = event.target.closest('[data-action]');
  if (!action) return;
  if (action.dataset.action === 'export') exportReport();
  else if (action.dataset.action === 'import') renderPage('data');
  else if (action.dataset.action === 'profile') openProfileModal();
  else if (action.dataset.action === 'sign-out') showSignedOut();
  else if (action.dataset.action === 'sign-in') signIn();
  else if (action.dataset.action === 'mark-read') showToast('Notifications marked as read');
  else showToast(`${action.dataset.action.replace('-', ' ')} is ready for configuration`);
});
document.addEventListener('change', event => {
  if (event.target.id !== 'pageFileInput') return;
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => { try { const imported = parseCsv(reader.result); if (!imported.length) throw new Error('No usable rows found.'); salesData = imported; showToast(`${imported.length} sales rows imported`); renderPage('overview'); } catch (error) { showToast(error.message); } };
  reader.readAsText(file);
});
document.querySelector('.icon-button[aria-label="Search"]').addEventListener('click', () => showToast('Global search is ready for your workspace'));
renderPage('overview');
syncProfileUI();

function closeHeaderPanels() {
  document.querySelectorAll('.header-popover').forEach(panel => panel.remove());
  document.querySelector('.search-overlay')?.remove();
}

function toggleHeaderPanel(panel) {
  const existing = document.querySelector('.header-popover');
  if (existing && existing.dataset.panel === panel) { existing.remove(); return; }
  closeHeaderPanels();
  if (panel === 'notifications') document.querySelector('.notification span')?.classList.add('hidden');
  const element = document.createElement('div');
  element.className = `header-popover ${panel}-popover`;
  element.dataset.panel = panel;
  element.innerHTML = panel === 'profile' ? `<div class="popover-heading"><div class="popover-avatar">${profileInitials(profileState.name)}</div><div><strong>${profileState.name}</strong><span>${profileState.role}</span></div></div><div class="popover-rule"></div><button data-view="settings"><i data-lucide="settings-2"></i>Workspace settings</button><button data-action="profile"><i data-lucide="user-round"></i>Change profile</button><div class="popover-rule"></div><button class="danger-action" data-action="sign-out"><i data-lucide="log-out"></i>Sign out</button>` : `<div class="popover-title"><strong>Notifications</strong><button data-action="mark-read">Mark all read</button></div><div class="notification-empty"><i data-lucide="bell-off"></i><strong>You're all caught up</strong><span>New workspace activity will appear here.</span></div>`;
  document.body.appendChild(element);
  lucide.createIcons();
}

function syncProfileUI() {
  const initials = profileInitials(profileState.name);
  document.querySelectorAll('.profile-avatar, .avatar-button').forEach(element => { element.textContent = initials; });
  const name = document.querySelector('.profile strong');
  const role = document.querySelector('.profile small');
  if (name) name.textContent = profileState.name;
  if (role) role.textContent = profileState.role;
}

function openProfileModal() {
  closeHeaderPanels();
  const modal = document.createElement('div');
  modal.className = 'profile-modal';
  modal.innerHTML = `<form class="profile-card" id="profileForm"><button type="button" class="modal-close" aria-label="Close profile"><i data-lucide="x"></i></button><div class="profile-card-heading"><div class="large-avatar">${profileInitials(profileState.name)}</div><div><span class="section-kicker">Account profile</span><h2>Change profile</h2><p>Update the identity shown across your workspace.</p></div></div><label>Full name<input id="profileName" value="${profileState.name}" required></label><label>Role<select id="profileRole"><option ${profileState.role === 'Admin' ? 'selected' : ''}>Admin</option><option ${profileState.role === 'Analyst' ? 'selected' : ''}>Analyst</option><option ${profileState.role === 'Manager' ? 'selected' : ''}>Manager</option></select></label><div class="profile-card-actions"><button type="button" class="button button-light modal-close">Cancel</button><button type="submit" class="button button-dark">Save profile</button></div></form>`;
  document.body.appendChild(modal);
  lucide.createIcons();
  modal.querySelectorAll('.modal-close').forEach(button => button.addEventListener('click', () => modal.remove()));
  modal.querySelector('form').addEventListener('submit', event => { event.preventDefault(); profileState.name = modal.querySelector('#profileName').value.trim(); profileState.role = modal.querySelector('#profileRole').value; localStorage.setItem('northstar-profile', JSON.stringify(profileState)); syncProfileUI(); modal.remove(); showToast('Profile updated'); });
}

function showSignedOut() {
  closeHeaderPanels();
  if (document.querySelector('.session-screen')) return;
  const screen = document.createElement('div');
  screen.className = 'session-screen';
  screen.innerHTML = `<div class="session-card"><span class="brand-mark"><i data-lucide="sparkles"></i></span><h1>Signed out</h1><p>Your Northstar workspace is closed. Return when you are ready to continue.</p><button class="button button-dark" data-action="sign-in"><i data-lucide="log-in"></i>Return to workspace</button></div>`;
  document.body.appendChild(screen);
  lucide.createIcons();
}

function signIn() {
  document.querySelector('.session-screen')?.remove();
  syncProfileUI();
  showToast(`Welcome back, ${profileState.name}`);
}

function openSearchOverlay() {
  closeHeaderPanels();
  const overlay = document.createElement('div');
  overlay.className = 'search-overlay';
  overlay.innerHTML = `<div class="search-box"><i data-lucide="search"></i><input id="globalSearchInput" placeholder="Search workspace sections..." autofocus><kbd>ESC</kbd></div><div class="search-results" id="searchResults"></div>`;
  document.body.appendChild(overlay);
  lucide.createIcons();
  const input = overlay.querySelector('input');
  const results = overlay.querySelector('#searchResults');
  const sections = [{ id: 'overview', label: 'Overview', description: 'Revenue and performance snapshot', icon: 'layout-dashboard' }, { id: 'customers', label: 'Customers', description: 'Accounts, value, and retention', icon: 'users' }, { id: 'products', label: 'Products', description: 'Catalog intelligence and margin', icon: 'package-2' }, { id: 'reports', label: 'Reports', description: 'Management reporting workspace', icon: 'file-bar-chart-2' }, { id: 'data', label: 'Data sources', description: 'Imports and connections', icon: 'database' }, { id: 'settings', label: 'Settings', description: 'Workspace administration', icon: 'settings-2' }];
  const renderResults = query => { const matches = sections.filter(section => `${section.label} ${section.description}`.toLowerCase().includes(query.toLowerCase())); results.innerHTML = matches.length ? matches.map(section => `<button data-view="${section.id}"><i data-lucide="${section.icon}"></i><span><strong>${section.label}</strong><small>${section.description}</small></span><i data-lucide="arrow-up-right"></i></button>`).join('') : '<div class="notification-empty"><i data-lucide="search-x"></i><strong>No matching sections</strong><span>Try a different workspace search.</span></div>'; lucide.createIcons(); };
  renderResults('');
  input.addEventListener('input', event => renderResults(event.target.value));
  input.addEventListener('keydown', event => { if (event.key === 'Escape') closeHeaderPanels(); });
}

document.querySelector('.avatar-button').addEventListener('click', event => { event.stopPropagation(); toggleHeaderPanel('profile'); });
document.querySelector('.notification').addEventListener('click', event => { event.stopPropagation(); toggleHeaderPanel('notifications'); });
document.querySelector('.icon-button[aria-label="Search"]').addEventListener('click', event => { event.stopPropagation(); openSearchOverlay(); });
document.addEventListener('click', event => { if (!event.target.closest('.header-popover, .search-overlay, .avatar-button, .notification, .icon-button[aria-label="Search"]')) closeHeaderPanels(); });
