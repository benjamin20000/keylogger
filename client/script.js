const API_URL = 'http://127.0.0.1:5000/data';
const COMMAND_URL = 'http://127.0.0.1:5000/command';
const XOR_KEY = "my_secret_key";

let computersData = {};
let isAuthenticated = false;
let currentUser = null;

document.addEventListener('DOMContentLoaded', initApp);

// Initializes the app by setting up UI and checking authentication
function initApp() {
    setupAuthUI();
    checkAuthStatus();
    if (isAuthenticated) {
        fetchData();
        setInterval(fetchData, 30000);
    }
}

// Sets up event listeners for authentication UI elements
function setupAuthUI() {
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
    document.getElementById('registerForm')?.addEventListener('submit', handleRegister);
    document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);
    document.querySelectorAll('.toggle-form').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('loginForm').style.display = document.getElementById('loginForm').style.display === 'none' ? 'block' : 'none';
            document.getElementById('registerForm').style.display = document.getElementById('registerForm').style.display === 'none' ? 'block' : 'none';
        });
    });
    document.getElementById('exportExcel')?.addEventListener('click', exportToExcel);
}

// Checks if the user is authenticated based on local storage
function checkAuthStatus() {
    const userSession = localStorage.getItem('currentUser');
    if (userSession) {
        currentUser = JSON.parse(userSession);
        isAuthenticated = true;
        showComputersPage();
    } else {
        showLoginPage();
    }
}

// Handles login form submission
function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const usersDB = JSON.parse(localStorage.getItem('usersDB')) || {};

    if (usersDB[username] && usersDB[username].password === password) {
        currentUser = { username, role: 'user' };
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        isAuthenticated = true;
        showComputersPage();
        fetchData();
        showMessage('Login successful', 'success');
    } else {
        showMessage('Invalid username or password', 'error');
    }
}

// Handles registration form submission
function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const usersDB = JSON.parse(localStorage.getItem('usersDB')) || {};

    if (password !== confirmPassword) return showMessage('Passwords do not match', 'error');
    if (usersDB[username]) return showMessage('Username already exists', 'error');

    usersDB[username] = { password, role: 'user' };
    localStorage.setItem('usersDB', JSON.stringify(usersDB));
    currentUser = { username, role: 'user' };
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    isAuthenticated = true;
    showComputersPage();
    showMessage('Registration successful', 'success');
}

// Logs out the current user
function handleLogout() {
    localStorage.removeItem('currentUser');
    isAuthenticated = false;
    currentUser = null;
    showLoginPage();
    showMessage('Logged out successfully', 'success');
}

// Displays the login page and hides the computers page
function showLoginPage() {
    document.getElementById('authContainer').style.display = 'flex';
    document.getElementById('computersContainer').style.display = 'none';
}

// Displays the computers page and hides the login page
function showComputersPage() {
    document.getElementById('authContainer').style.display = 'none';
    document.getElementById('computersContainer').style.display = 'block';
    document.getElementById('userInfo').textContent = `Logged in as: ${currentUser.username}`;
}

// Shows a temporary status message
function showMessage(message, type) {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type === 'error' ? 'status-error' : 'status-success'}`;
    statusEl.style.display = 'block';
    setTimeout(() => statusEl.style.display = 'none', 3000);
}

// Fetches data from the server or uses sample data on failure
async function fetchData() {
    if (!isAuthenticated) return;
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
        computersData = await response.json();
        console.log("Fetched data:", computersData);
        populateTable(computersData);
        showMessage('Data updated', 'success');
    } catch (error) {
        console.error('Fetch error:', error);
        computersData = {
            "00:1A:2B:3C:4D:5E": [{ "time": "2025-02-25T10:00:00", "data": "Hello World", "app": "WhatsApp", "monitoring": false }]
        };
        console.log("Using sample data:", computersData);
        populateTable(computersData);
        showMessage('Using sample data due to server error', 'error');
    }
}

// Decrypts data using XOR with a key
function decryptData(encryptedData) {
    try {
        return encryptedData.split('').map((char, i) =>
            String.fromCharCode(char.charCodeAt(0) ^ XOR_KEY.charCodeAt(i % XOR_KEY.length))
        ).join('');
    } catch (e) {
        console.error('Decryption error:', e);
        return encryptedData;
    }
}

// Populates the computers table with data
function populateTable(data) {
    const tbody = document.querySelector('#computersTable tbody');
    tbody.innerHTML = '';

    for (const mac in data) {
        const actions = data[mac];
        const latest = actions[actions.length - 1];
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${mac}</td>
            <td>${new Date(latest.time).toLocaleString()}</td>
            <td>${decryptData(latest.data)}</td>
            <td>${latest.window || 'Unknown'}</td>
            <td>${latest.monitoring ? 'Active' : 'Inactive'}</td>
            <td>
                <button class="action-btn" data-tooltip="View Details" onclick="viewDetails('${mac}')"><i class="fas fa-eye"></i></button>
                <button class="action-btn" data-tooltip="Start Monitoring" onclick="startMonitoring('${mac}')"><i class="fas fa-play"></i></button>
                <button class="action-btn" data-tooltip="Stop Monitoring" onclick="stopMonitoring('${mac}')"><i class="fas fa-stop"></i></button>
            </td>
        `;
        tbody.appendChild(row);
    }
    setupFilterListeners();
}

// Displays detailed information for a specific MAC address in a modal
function viewDetails(mac) {
    const actions = computersData[mac];
    const modal = document.getElementById('computerModal');
    const modalContent = modal.querySelector('.modal-content');
    const modalTitle = document.getElementById('modalTitle');
    const detailsTbody = document.getElementById('detailsTable').querySelector('tbody');

    modalTitle.textContent = `Details for ${mac}`;
    detailsTbody.innerHTML = actions.map(action => `
        <tr>
            <td>${new Date(action.time).toLocaleString()}</td>
            <td>${decryptData(action.data)}</td>
            <td>${action.window || 'Unknown'}</td>
            <td>${action.monitoring ? 'Active' : 'Inactive'}</td>
        </tr>
    `).join('');
    modal.style.display = 'block';
    window.currentMac = mac;
    setupModalFilterListeners();
}

// Sends a command to start monitoring a specific computer
async function startMonitoring(mac) {
    try {
        const response = await fetch(COMMAND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mac, command: 'start_monitoring', user: currentUser.username })
        });
        if (!response.ok) throw new Error(`Command failed: ${response.status} - ${response.statusText}`);
        const result = await response.json();
        console.log("Start monitoring response:", result);
        if (result.error) throw new Error(result.error);
        showMessage(result.message || `Monitoring started for ${mac}`, 'success');
        fetchData();
    } catch (error) {
        console.error('Start monitoring error:', error);
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Sends a command to stop monitoring a specific computer
async function stopMonitoring(mac) {
    try {
        const response = await fetch(COMMAND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mac, command: 'stop_monitoring', user: currentUser.username })
        });
        if (!response.ok) throw new Error(`Command failed: ${response.status} - ${response.statusText}`);
        const result = await response.json();
        console.log("Stop monitoring response:", result);
        if (result.error) throw new Error(result.error);
        showMessage(result.message || `Monitoring stopped for ${mac}`, 'success');
        fetchData();
    } catch (error) {
        console.error('Stop monitoring error:', error);
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Sets up event listeners for table filters
function setupFilterListeners() {
    document.querySelectorAll('.filter-input, .filter-date').forEach(input => {
        input.addEventListener('input', filterTableByColumn);
    });
}

// Filters the main table based on input values
function filterTableByColumn() {
    const filters = Array.from(document.querySelectorAll('.filter-input, .filter-date')).map(input => input.value.toUpperCase());
    const rows = document.querySelectorAll('#computersTable tbody tr');

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        let isVisible = true;

        filters.forEach((filter, index) => {
            if (filter && index < cells.length - 1) {
                const cellText = cells[index].textContent.toUpperCase();
                if (index === 1) { // Date column
                    const date = new Date(cells[index].textContent).toISOString().split('T')[0];
                    if (!date.includes(filter)) {
                        isVisible = false;
                    }
                } else if (cellText.indexOf(filter) === -1) {
                    isVisible = false;
                }
            }
        });

        row.style.display = isVisible ? '' : 'none';
    });
}

// Sets up event listeners for modal table filters
function setupModalFilterListeners() {
    document.querySelectorAll('.filter-input-modal, .filter-date-modal').forEach(input => {
        input.addEventListener('input', filterModalTableByColumn);
    });
}

// Filters the modal table based on input values
function filterModalTableByColumn() {
    const filters = Array.from(document.querySelectorAll('.filter-input-modal, .filter-date-modal')).map(input => input.value.toUpperCase());
    const rows = document.getElementById('detailsTable').querySelectorAll('tbody tr');

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        let isVisible = true;

        filters.forEach((filter, index) => {
            if (filter && index < cells.length) {
                const cellText = cells[index].textContent.toUpperCase();
                if (index === 0) { // Date column
                    const date = new Date(cells[index].textContent).toISOString().split('T')[0];
                    if (!date.includes(filter)) {
                        isVisible = false;
                    }
                } else if (cellText.indexOf(filter) === -1) {
                    isVisible = false;
                }
            }
        });

        row.style.display = isVisible ? '' : 'none';
    });
}

// Exports the main table to an Excel-compatible CSV file
function exportToExcel() {
    const table = document.getElementById('computersTable');
    const rows = Array.from(table.querySelectorAll('tr'));
    const csv = rows.map(row => 
        Array.from(row.querySelectorAll('th, td'))
            .slice(0, -1) // Remove Actions column
            .map(cell => `"${cell.textContent.replace(/"/g, '""')}"`)
            .join(',')
    ).join('\n');
    downloadCSV(csv, 'computer_monitoring.csv');
}

// Exports the modal table to an Excel-compatible CSV file
function exportModalToExcel() {
    const table = document.getElementById('detailsTable');
    const rows = Array.from(table.querySelectorAll('tr'));
    const csv = rows.map(row => 
        Array.from(row.querySelectorAll('th, td'))
            .map(cell => `"${cell.textContent.replace(/"/g, '""')}"`)
            .join(',')
    ).join('\n');
    downloadCSV(csv, `details_${window.currentMac}.csv`);
}

// Downloads a CSV file with the specified content and filename
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Opens a new window with detailed information for the current MAC address
function openDetailsPage() {
    const mac = window.currentMac;
    if (!mac) {
        showMessage('No MAC address selected', 'error');
        return;
    }
    const actions = computersData[mac];
    if (!actions || actions.length === 0) {
        showMessage('No data available for this MAC address', 'error');
        return;
    }
    const newWindow = window.open('', '_blank');
    newWindow.document.write(`
        <html>
        <head>
            <title>Details for ${mac}</title>
            <style>
                /* General Styles */
                * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
                body { background-color: #f0f2f5; color: #333; padding: 20px; }
                
                /* Header Styles */
                .main-title { 
                    color: #1e3c72; 
                    font-size: 32px; 
                    font-weight: bold; 
                    text-align: center; 
                    margin-bottom: 20px; 
                }
                
                /* Table Styles */
                table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1); }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background: #f8f9fa; color: #1e3c72; }
                tbody tr:hover { background: #f8f9fa; }
                
                /* Filter Input Styles */
                .filter-input, .filter-date { 
                    width: 100%; 
                    padding: 5px; 
                    margin-top: 5px; 
                    border: 1px solid #ddd; 
                    border-radius: 4px; 
                    font-size: 12px; 
                }
                
                /* Button Styles */
                .btn { 
                    padding: 8px 15px; 
                    background: #1e3c72; 
                    color: white; 
                    border: none; 
                    border-radius: 5px; 
                    cursor: pointer; 
                    margin-bottom: 15px; 
                }
                .btn:hover { background: #2a5298; }
                
                /* Header Actions */
                .header-actions { text-align: center; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="header-actions">
                <button class="btn" onclick="exportToExcel()">Export to Excel</button>
            </div>
            <h2 class="main-title">Details for ${mac}</h2>
            <table id="detailsTable">
                <thead>
                    <tr>
                        <th>Time<br><input type="date" class="filter-date" data-column="0" placeholder="Filter Date..."></th>
                        <th>Data<br><input type="text" class="filter-input" data-column="1" placeholder="Filter Data..."></th>
                        <th>Application<br><input type="text" class="filter-input" data-column="2" placeholder="Filter App..."></th>
                        <th>Monitoring<br><input type="text" class="filter-input" data-column="3" placeholder="Filter Status..."></th>
                    </tr>
                </thead>
                <tbody>
                    ${actions.map(action => `
                        <tr>
                            <td>${new Date(action.time).toLocaleString()}</td>
                            <td>${decryptData(action.data)}</td>
                            <td>${action.window || 'Unknown'}</td>
                            <td>${action.monitoring ? 'Active' : 'Inactive'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <script>
                function filterTableByColumn() {
                    const filters = Array.from(document.querySelectorAll('.filter-input, .filter-date')).map(input => input.value.toUpperCase());
                    const rows = document.querySelectorAll('#detailsTable tbody tr');
                    rows.forEach(row => {
                        const cells = row.getElementsByTagName('td');
                        let isVisible = true;
                        filters.forEach((filter, index) => {
                            if (filter && index < cells.length) {
                                const cellText = cells[index].textContent.toUpperCase();
                                if (index === 0) {
                                    const date = new Date(cells[index].textContent).toISOString().split('T')[0];
                                    if (!date.includes(filter)) isVisible = false;
                                } else if (cellText.indexOf(filter) === -1) {
                                    isVisible = false;
                                }
                            }
                        });
                        row.style.display = isVisible ? '' : 'none';
                    });
                }

                function exportToExcel() {
                    const table = document.getElementById('detailsTable');
                    const rows = Array.from(table.querySelectorAll('tr'));
                    const csv = rows.map(row => 
                        Array.from(row.querySelectorAll('th, td'))
                            .map(cell => \`"${cell.textContent.replace(/"/g, '""')}"\`)
                            .join(',')
                    ).join('\n');
                    const blob = new Blob([csv], { type: 'text/csv' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'details_${mac}.csv';
                    a.click();
                    window.URL.revokeObjectURL(url);
                }

                document.querySelectorAll('.filter-input, .filter-date').forEach(input => {
                    input.addEventListener('input', filterTableByColumn);
                });
            </script>
        </body>
        </html>
    `);
    newWindow.document.close();
}