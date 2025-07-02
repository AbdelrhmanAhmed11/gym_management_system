# Gym Client Management System

A full-featured Python desktop application for managing gym clients, subscriptions, attendance, finances, sessions, and reports.

## Features
- Client management with detailed profiles
- Subscriptions & renewals (Normal, Private, Box, Under 15)
- Attendance logging and reporting
- Financial records and categorized expenses
- Private/group session booking
- Invitation and referral tracking
- Loans management
- Role-based login (Receptionist, Admin)
- Admin dashboard with charts and alerts
- English and Arabic UI (localization)
- PDF and Excel export for reports
- Hardware integration: profile image upload, ID scanner, (optional) fingerprint scanner
- Responsive design for tablets

## Tech Stack
- Python 3.x
- PyQt5 (or Tkinter with ttkbootstrap)
- SQLite (local embedded database)
- MVC/MVVM architecture

## Folder Structure
- `models/` - Database models and logic
- `views/` - UI files and widgets
- `controllers/` - Application logic and controllers
- `i18n/` - Localization files (English/Arabic)
- `db/` - Database setup and sample data
- `assets/` - Images and resources

## Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the database setup script: `python db/setup.py`
4. Launch the app: `python main.py`

## Usage
- Login as Admin or Receptionist
- Manage clients, subscriptions, attendance, finances, and more
- Switch language from the UI
- Export reports as PDF/Excel

## Sample Data
Sample data is included for testing and demonstration.

## License
MIT 