# Computer Monitoring System with Keylogger

This is a Python-based computer monitoring system that includes a keylogger to track and log keystrokes on target machines. The system features a web-based interface for managing and viewing logged data, authentication, and real-time monitoring controls. The project is built using Flask for the backend, JavaScript for the frontend, and various libraries for encryption and parsing.

## Features
- **Keylogger:** Captures keystrokes and associates them with active application windows.
- **Web Interface:** Provides a user-friendly interface to view and manage monitored data.
- **Authentication:** Supports user login and registration with local storage.
- **Real-Time Monitoring:** Start and stop monitoring for specific machines via the UI.
- **Data Encryption:** Uses XOR encryption to secure logged data.
- **Data Export:** Export monitoring data to Excel-compatible CSV files.
- **Filtering:** Filter data by MAC address, time, data, application, and monitoring status.

## Prerequisites
Before running the project, ensure you have the following installed:
- **Python 3.x**
- **pip** (Python package manager)
- Required Python libraries (install via `requirements.txt`):
  - `flask`
  - `flask-cors`
  - `keyboard`
  - `pygetwindow`
  - `json`

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/benjamin20000/keylogger.git
   cd keylogger/logger_agent

#Install the required libraries:
    pip install -r requirements.txt

#Note: Create a requirements.txt file with the following content if not already present:
    flask
    flask-cors
    keyboard
    pygetwindow

#Ensure the data directory exists in the logger_agent folder for storing server.json.
Update config.config with appropriate write_delay and send_json_delay values if needed.

#Navigate to the logger_agent directory and run:
    python main.py


keylogger/
├── logger_agent/
│   ├── src/
│   │   ├── listener.py         # Keylogger listener logic
│   │   ├── manager.py          # Main server logic and Flask app
│   │   ├── parser/
│   │   │   ├── encryption/
│   │   │   │   ├── xor.py      # XOR encryption implementation
│   │   ├── parsers.py          # Data parsing logic
│   ├── data/                   # Directory for storing server.json
│   ├── main.py                 # Entry point to run the server
├── index.html                  # Web interface HTML
├── styles.css                  # CSS for styling the UI
├── script.js                   # JavaScript for frontend logic
├── README.md                   # This file



