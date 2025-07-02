from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, 
                             QSizePolicy, QFrame, QGraphicsDropShadowEffect, QHeaderView, QSpacerItem)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QColor
from controllers.attendance_controller import AttendanceController
from models.client_model import ClientModel

class AttendanceView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = AttendanceController()
        self.client_model = ClientModel()
        self.init_ui()
        self.apply_styles()
        self.load_attendance()

    def init_ui(self):
        self.setWindowTitle(self.tr('Attendance Management'))
        
        # Main layout with NO margins or spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header section
        header_section = self.create_header_section()
        main_layout.addWidget(header_section)
        
        # Controls section (date picker and search)
        controls_section = self.create_controls_section()
        main_layout.addWidget(controls_section)
        
        # Table section
        table_section = self.create_table_section()
        main_layout.addWidget(table_section)
        
        # Check-in section
        checkin_section = self.create_checkin_section()
        main_layout.addWidget(checkin_section)
        
        self.setLayout(main_layout)

    def create_header_section(self):
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(120)
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(40, 30, 40, 30)
        
        # Title
        title_label = QLabel(self.tr('📋 Attendance Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Track member check-ins and monitor gym attendance'))
        subtitle_label.setObjectName("pageSubtitle")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_controls_section(self):
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_frame.setFixedHeight(100)
        
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(40, 25, 40, 25)
        controls_layout.setSpacing(20)
        
        # Date section
        date_label = QLabel(self.tr('📅 Select Date:'))
        date_label.setObjectName("controlLabel")
        
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setObjectName("datePicker")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setFixedHeight(45)
        self.date_picker.setFixedWidth(180)
        
        self.search_btn = QPushButton(self.tr('🔍 View Attendance'))
        self.search_btn.setObjectName("searchButton")
        self.search_btn.setFixedHeight(45)
        self.search_btn.setFixedWidth(160)
        self.search_btn.clicked.connect(self.load_attendance)
        
        # Statistics label
        self.stats_label = QLabel(self.tr('Total Check-ins: 0'))
        self.stats_label.setObjectName("statsLabel")
        
        controls_layout.addWidget(date_label)
        controls_layout.addWidget(self.date_picker)
        controls_layout.addWidget(self.search_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.stats_label)
        
        controls_frame.setLayout(controls_layout)
        
        return controls_frame

    def create_table_section(self):
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(40, 30, 40, 30)
        table_layout.setSpacing(20)
        
        # Table title
        table_title = QLabel(self.tr('Attendance Records'))
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Create and style table
        self.table = QTableWidget(0, 3)
        self.table.setObjectName("attendanceTable")
        self.table.setHorizontalHeaderLabels([
            self.tr('Client Code'), 
            self.tr('Member Name'), 
            self.tr('Check-in Time')
        ])
        
        # Configure table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setMinimumHeight(400)
        
        table_layout.addWidget(self.table)
        table_frame.setLayout(table_layout)
        
        return table_frame

    def create_checkin_section(self):
        checkin_frame = QFrame()
        checkin_frame.setObjectName("checkinFrame")
        checkin_frame.setFixedHeight(120)
        
        checkin_layout = QVBoxLayout()
        checkin_layout.setContentsMargins(40, 25, 40, 25)
        checkin_layout.setSpacing(15)
        
        # Section title
        checkin_title = QLabel(self.tr('✅ Quick Check-in'))
        checkin_title.setObjectName("checkinTitle")
        checkin_layout.addWidget(checkin_title)
        
        # Input controls
        input_layout = QHBoxLayout()
        input_layout.setSpacing(15)
        
        input_label = QLabel(self.tr('👤 Client:'))
        input_label.setObjectName("inputLabel")
        
        self.client_input = QLineEdit()
        self.client_input.setObjectName("clientInput")
        self.client_input.setPlaceholderText(self.tr('Enter client code or name...'))
        self.client_input.setFixedHeight(45)
        self.client_input.setMinimumWidth(300)
        
        self.checkin_btn = QPushButton(self.tr('🔥 Log Check-in'))
        self.checkin_btn.setObjectName("checkinButton")
        self.checkin_btn.setFixedHeight(45)
        self.checkin_btn.setFixedWidth(160)
        self.checkin_btn.clicked.connect(self.handle_checkin)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.client_input)
        input_layout.addWidget(self.checkin_btn)
        input_layout.addStretch()
        
        checkin_layout.addLayout(input_layout)
        checkin_frame.setLayout(checkin_layout)
        
        return checkin_frame

    def apply_styles(self):
        style_sheet = """
            /* Main Widget Background - DARK like Dashboard */
            QWidget {
                background-color: #2c2c2c;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Header Frame - DARK seamless */
            QFrame#headerFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QLabel#pageTitle {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
            
            QLabel#pageSubtitle {
                color: #cccccc;
                font-size: 16px;
                font-weight: 400;
                background: transparent;
            }
            
            /* Controls Frame - DARK seamless */
            QFrame#controlsFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QLabel#controlLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            QLabel#statsLabel {
                color: #e63946;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
            
            /* Date Picker - DARK style */
            QDateEdit#datePicker {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 12px;
            }
            
            QDateEdit#datePicker:focus {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QDateEdit#datePicker::drop-down {
                border: none;
                background-color: #e63946;
                border-radius: 4px;
                width: 30px;
            }
            
            QDateEdit#datePicker::down-arrow {
                image: none;
                border: none;
                width: 0px;
                height: 0px;
            }
            
            /* Search Button */
            QPushButton#searchButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#searchButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #e63946);
            }
            
            QPushButton#searchButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c1121f, stop:1 #a00e1c);
            }
            
            /* Table Frame - DARK seamless */
            QFrame#tableFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            /* Section Titles */
            QLabel#sectionTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                padding: 0px 0px 10px 0px;
                border-bottom: 3px solid #e63946;
            }
            
            /* Attendance Table - DARK style */
            QTableWidget#attendanceTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                selection-background-color: #e63946;
                selection-color: white;
                font-size: 14px;
            }
            
            QTableWidget#attendanceTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#attendanceTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                padding: 15px 8px;
                border: none;
                border-right: 1px solid #a00e1c;
                font-size: 14px;
                font-weight: bold;
            }
            
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #e63946);
            }
            
            /* Scrollbars - DARK */
            QScrollBar:vertical {
                background-color: #404040;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #e63946;
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #ff6b6b;
            }
            
            /* Check-in Frame - DARK seamless */
            QFrame#checkinFrame {
                background-color: #2c2c2c;
                border: none;
                border-top: 2px solid #e63946;
            }
            
            QLabel#checkinTitle {
                color: #e63946;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }
            
            QLabel#inputLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            /* Client Input - DARK style */
            QLineEdit#clientInput {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 12px 15px;
            }
            
            QLineEdit#clientInput:focus {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QLineEdit#clientInput::placeholder {
                color: #999999;
            }
            
            /* Check-in Button */
            QPushButton#checkinButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38b000, stop:1 #2d8f00);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#checkinButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ade80, stop:1 #38b000);
            }
            
            QPushButton#checkinButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d8f00, stop:1 #1f6b00);
            }
            
            /* Message Boxes - DARK */
            QMessageBox {
                background-color: #2c2c2c;
                color: #ffffff;
            }
            
            QMessageBox QPushButton {
                background-color: #e63946;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #ff6b6b;
            }
        """
        self.setStyleSheet(style_sheet)

    def load_attendance(self):
        date = self.date_picker.date().toString('yyyy-MM-dd')
        records = self.controller.get_by_date(date)
        
        self.table.setRowCount(0)
        
        for rec in records:
            _, code, name, checkin_time = rec
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Create items with proper formatting
            code_item = QTableWidgetItem(str(code))
            name_item = QTableWidgetItem(str(name))
            time_item = QTableWidgetItem(str(checkin_time))
            
            # Center align the code and time
            code_item.setTextAlignment(Qt.AlignCenter)
            time_item.setTextAlignment(Qt.AlignCenter)
            
            self.table.setItem(row, 0, code_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, time_item)
        
        # Update statistics
        total_checkins = len(records)
        self.stats_label.setText(self.tr(f'📊 Total Check-ins: {total_checkins}'))

    def handle_checkin(self):
        text = self.client_input.text().strip()
        if not text:
            self.show_error_message(self.tr('Please enter client code or name.'))
            return
            
        # Find client by code or name
        clients = self.client_model.search(text)
        if not clients:
            self.show_error_message(self.tr('Client not found. Please verify the code or name.'))
            return
            
        client_code = clients[0][0]
        
        # Get client_id
        client_id = self.get_client_id_by_code(client_code)
        if not client_id:
            self.show_error_message(self.tr('Client not found in database.'))
            return
            
        try:
            self.controller.log_checkin(client_id, 1)  # Assume user_id=1 (admin) for now
            self.show_success_message(self.tr('✅ Check-in logged successfully!'))
            self.client_input.clear()
            self.load_attendance()  # Refresh the table
        except Exception as e:
            self.show_error_message(str(e))

    def show_success_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(self.tr('Success'))
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(self.tr('Error'))
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def get_client_id_by_code(self, code):
        # Helper to get client id from code
        from models.db_manager import DBManager
        db = DBManager()
        row = db.fetchone('SELECT id FROM clients WHERE client_code=?', (code,))
        return row[0] if row else None

    def tr(self, text):
        # Placeholder for translation - implement with your translator
        if hasattr(self.translator, 'tr'):
            return self.translator.tr(text)
        return text