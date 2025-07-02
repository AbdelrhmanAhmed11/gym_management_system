-- Gym Client Management System Database Schema

PRAGMA foreign_keys = ON;

-- Users (Receptionist, Admin)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'receptionist')),
    full_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clients
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    profile_picture TEXT,
    subscription_type TEXT NOT NULL,
    subscription_id INTEGER,
    start_date DATE,
    end_date DATE,
    amount_paid REAL DEFAULT 0,
    amount_remaining REAL DEFAULT 0,
    freeze_days INTEGER DEFAULT 0,
    trainer_name TEXT,
    rotation TEXT,
    guardian_name TEXT,
    guardian_phone TEXT,
    attendance_schedule TEXT,
    invited_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(id),
    FOREIGN KEY (invited_by) REFERENCES clients(id)
);

-- Subscriptions & Renewals
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    duration_months INTEGER,
    session_count INTEGER,
    start_date DATE,
    end_date DATE,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Attendance Logs
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checked_in_by INTEGER,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (checked_in_by) REFERENCES users(id)
);

-- Financial Records
CREATE TABLE finances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recorded_by INTEGER,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
);

-- Private Sessions
CREATE TABLE private_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    trainer_name TEXT,
    session_date DATE,
    session_type TEXT,
    is_group INTEGER DEFAULT 0,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Invitations
CREATE TABLE invitations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    friend_name TEXT NOT NULL,
    friend_phone TEXT,
    invited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tagged INTEGER DEFAULT 0,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Logs (for payment actions, auto-logging)
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Loans
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    amount REAL NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Hardware Logs (optional)
CREATE TABLE hardware_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    event_type TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
); 