from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy,
                             QFrame, QHeaderView, QComboBox, QDateEdit, QInputDialog,
                             QSpacerItem, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QColor, QFont, QPalette
from controllers.session_controller import SessionController
from models.client_model import ClientModel
from datetime import datetime, timedelta

class SessionsView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = SessionController()
        self.client_model = ClientModel()
        self.init_ui()
        self.apply_styles()
        self.load_sessions()

    def init_ui(self):
        self.setWindowTitle(self.tr('Sessions Management'))
        
        # Main layout with NO margins or spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header_section = self.create_header_section()
        main_layout.addWidget(header_section)

        # Search and filter section
        search_section = self.create_search_section()
        main_layout.addWidget(search_section)

        # Stats section
        stats_section = self.create_stats_section()
        main_layout.addWidget(stats_section)

        # Table section
        table_section = self.create_table_section()
        main_layout.addWidget(table_section)

        # Action buttons section
        actions_section = self.create_actions_section()
        main_layout.addWidget(actions_section)

        self.setLayout(main_layout)

    def create_header_section(self):
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(120)
        
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(40, 30, 40, 30)
        header_layout.setSpacing(10)
        
        # Title
        title_label = QLabel(self.tr('🏋️ Sessions Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Track training sessions, manage schedules, and monitor workout activities'))
        subtitle_label.setObjectName("pageSubtitle")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_search_section(self):
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_frame.setFixedHeight(120)
        
        search_layout = QVBoxLayout()
        search_layout.setContentsMargins(40, 20, 40, 20)
        search_layout.setSpacing(15)
        
        # First row - Search and basic filters
        first_row = QHBoxLayout()
        first_row.setSpacing(20)
        
        # Search icon label
        search_icon = QLabel("🔍")
        search_icon.setObjectName("searchIcon")
        search_icon.setFixedSize(30, 30)
        search_icon.setAlignment(Qt.AlignCenter)
        
        # Trainer search input
        self.trainer_input = QLineEdit()
        self.trainer_input.setObjectName("searchInput")
        self.trainer_input.setPlaceholderText(self.tr('Search by trainer name...'))
        self.trainer_input.setFixedHeight(45)
        self.trainer_input.textChanged.connect(self.on_search_text_changed)
        
        # Client search input
        self.client_input = QLineEdit()
        self.client_input.setObjectName("searchInput")
        self.client_input.setPlaceholderText(self.tr('Search by client code/name...'))
        self.client_input.setFixedHeight(45)
        self.client_input.textChanged.connect(self.on_search_text_changed)
        
        first_row.addWidget(search_icon)
        first_row.addWidget(self.trainer_input)
        first_row.addWidget(self.client_input)
        
        # Second row - Filters and actions
        second_row = QHBoxLayout()
        second_row.setSpacing(20)
        
        # Type filter
        self.type_combo = QComboBox()
        self.type_combo.setObjectName("filterCombo")
        self.type_combo.setFixedHeight(45)
        self.type_combo.setFixedWidth(150)
        self.type_combo.addItems([
            self.tr('All Types'),
            self.tr('Private'),
            self.tr('Group')
        ])
        self.type_combo.currentTextChanged.connect(self.apply_filters)
        
        # Date picker
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setObjectName("dateInput")
        self.date_picker.setFixedHeight(45)
        self.date_picker.setFixedWidth(150)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.dateChanged.connect(self.apply_filters)
        
        # Filter button
        self.filter_btn = QPushButton(self.tr('🔍 Filter'))
        self.filter_btn.setObjectName("searchButton")
        self.filter_btn.setFixedHeight(45)
        self.filter_btn.setFixedWidth(120)
        self.filter_btn.clicked.connect(self.handle_filter)
        
        # Clear button
        self.clear_btn = QPushButton(self.tr('✖ Clear'))
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.setFixedHeight(45)
        self.clear_btn.setFixedWidth(100)
        self.clear_btn.clicked.connect(self.clear_filters)
        
        second_row.addWidget(QLabel(self.tr('Type:')))
        second_row.addWidget(self.type_combo)
        second_row.addWidget(QLabel(self.tr('Date:')))
        second_row.addWidget(self.date_picker)
        second_row.addWidget(self.filter_btn)
        second_row.addWidget(self.clear_btn)
        second_row.addStretch()
        
        search_layout.addLayout(first_row)
        search_layout.addLayout(second_row)
        
        search_frame.setLayout(search_layout)
        
        return search_frame

    def create_stats_section(self):
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_frame.setFixedHeight(120)
        
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(40, 20, 40, 20)
        stats_layout.setSpacing(15)
        
        # Get session statistics
        stats = self.get_session_stats()
        
        # Create stat cards
        stat_cards = [
            ('🏋️', self.tr('Total Sessions'), str(stats['total']), '#e63946'),
            ('👤', self.tr('Private Sessions'), str(stats['private']), '#38b000'),
            ('👥', self.tr('Group Sessions'), str(stats['group']), '#17a2b8'),
            ('📅', self.tr('Today'), str(stats['today']), '#ffcc00')
        ]
        
        for icon, label, value, color in stat_cards:
            card = self.create_stat_card(icon, label, value, color)
            stats_layout.addWidget(card)
        
        stats_frame.setLayout(stats_layout)
        
        return stats_frame

    def create_stat_card(self, icon, label, value, color):
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(80)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        
        # Top row with icon and value
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(value_label)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setObjectName("statLabel")
        label_widget.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(top_layout)
        layout.addWidget(label_widget)
        
        card.setLayout(layout)
        
        return card

    def create_table_section(self):
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(40, 30, 40, 30)
        table_layout.setSpacing(20)
        
        # Table title
        table_title = QLabel(self.tr('Session Records'))
        table_title.setObjectName("sectionTitle")
        
        # Create table
        self.table = QTableWidget(0, 6)
        self.table.setObjectName("sessionsTable")
        self.table.setHorizontalHeaderLabels([
            self.tr('Client Code'),
            self.tr('Client Name'), 
            self.tr('Trainer'), 
            self.tr('Date'), 
            self.tr('Type'), 
            self.tr('Group Session')
        ])
        
        # Configure table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumHeight(45)
        
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(400)
        
        # Connect double-click to edit
        self.table.doubleClicked.connect(self.open_edit_dialog)
        
        table_layout.addWidget(table_title)
        table_layout.addWidget(self.table)
        
        table_frame.setLayout(table_layout)
        
        return table_frame

    def create_actions_section(self):
        actions_frame = QFrame()
        actions_frame.setObjectName("actionsFrame")
        actions_frame.setFixedHeight(120)
        
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(40, 25, 40, 25)
        actions_layout.setSpacing(15)
        
        # Section title
        actions_title = QLabel(self.tr('⚡ Quick Actions'))
        actions_title.setObjectName("actionsTitle")
        actions_layout.addWidget(actions_title)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Add button
        self.add_btn = QPushButton(self.tr('➕ Add New Session'))
        self.add_btn.setObjectName("addButton")
        self.add_btn.setFixedHeight(45)
        self.add_btn.setFixedWidth(170)
        self.add_btn.clicked.connect(self.open_add_session)
        
        # Edit button
        self.edit_btn = QPushButton(self.tr('✏️ Edit Session'))
        self.edit_btn.setObjectName("editButton")
        self.edit_btn.setFixedHeight(45)
        self.edit_btn.setFixedWidth(140)
        self.edit_btn.clicked.connect(self.open_edit_dialog)
        
        # Delete button
        self.delete_btn = QPushButton(self.tr('🗑️ Delete Session'))
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.setFixedHeight(45)
        self.delete_btn.setFixedWidth(150)
        self.delete_btn.clicked.connect(self.handle_delete)
        
        # Export button
        self.export_btn = QPushButton(self.tr('📊 Export Data'))
        self.export_btn.setObjectName("exportButton")
        self.export_btn.setFixedHeight(45)
        self.export_btn.setFixedWidth(140)
        self.export_btn.clicked.connect(self.export_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.export_btn)
        
        actions_layout.addLayout(buttons_layout)
        actions_frame.setLayout(actions_layout)
        
        return actions_frame

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
            
            /* Search Frame - DARK seamless */
            QFrame#searchFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QLabel#searchIcon {
                font-size: 18px;
                background: transparent;
                color: #e63946;
            }
            
            QLineEdit#searchInput {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QLineEdit#searchInput:focus {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QLineEdit#searchInput::placeholder {
                color: #999999;
            }
            
            QComboBox#filterCombo {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QComboBox#filterCombo:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QComboBox#filterCombo::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox#filterCombo::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #ffffff;
                margin-right: 5px;
            }
            
            QComboBox#filterCombo QAbstractItemView {
                background-color: #404040;
                border: 2px solid #e63946;
                border-radius: 8px;
                selection-background-color: #e63946;
                color: #ffffff;
            }
            
            QDateEdit#dateInput {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QDateEdit#dateInput:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QDateEdit#dateInput::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QDateEdit#dateInput::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #ffffff;
                margin-right: 5px;
            }
            
            /* Search and Clear Buttons */
            QPushButton#searchButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 20px;
            }
            
            QPushButton#searchButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #e63946);
            }
            
            QPushButton#clearButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 20px;
            }
            
            QPushButton#clearButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #343a40);
            }
            
            /* Stats Frame - DARK seamless */
            QFrame#statsFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QFrame#statCard {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 10px;
            }
            
            QFrame#statCard:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QLabel#statIcon {
                font-size: 20px;
                background: transparent;
            }
            
            QLabel#statValue {
                background: transparent;
            }
            
            QLabel#statLabel {
                color: #cccccc;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
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
            
            /* Table Styling - DARK */
            QTableWidget#sessionsTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                font-size: 13px;
                selection-background-color: #e63946;
                selection-color: white;
            }
            
            QTableWidget#sessionsTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#sessionsTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QTableWidget#sessionsTable::item:hover {
                background-color: #4a4a4a;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #a00e1c;
                font-weight: bold;
                font-size: 14px;
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
            
            /* Actions Frame - DARK seamless */
            QFrame#actionsFrame {
                background-color: #2c2c2c;
                border: none;
                border-top: 2px solid #e63946;
            }
            
            QLabel#actionsTitle {
                color: #e63946;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }
            
            /* Action Buttons */
            QPushButton#addButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38b000, stop:1 #2d8000);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#addButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ade80, stop:1 #38b000);
            }
            
            QPushButton#editButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#editButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #e63946);
            }
            
            QPushButton#deleteButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #a71e2a);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#deleteButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #dc3545);
            }
            
            QPushButton#exportButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #0f7b8a);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#exportButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a9c4, stop:1 #17a2b8);
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
            
            /* Input Dialogs - DARK */
            QInputDialog {
                background-color: #2c2c2c;
                color: #ffffff;
            }
            
            QInputDialog QLineEdit {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QInputDialog QLineEdit:focus {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QInputDialog QComboBox {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QInputDialog QComboBox:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
        """
        self.setStyleSheet(style_sheet)

    def get_session_stats(self):
        """Get session statistics"""
        try:
            sessions = self.controller.get_all()
            total = len(sessions)
            private = 0
            group = 0
            today = 0
            
            today_date = datetime.now().date().strftime('%Y-%m-%d')
            
            for session in sessions:
                # session: id, client_id, trainer_name, session_date, session_type, is_group
                if session[5]:  # is_group
                    group += 1
                else:
                    private += 1
                
                if session[3] == today_date:  # session_date
                    today += 1
            
            return {
                'total': total,
                'private': private,
                'group': group,
                'today': today
            }
        except:
            return {'total': 0, 'private': 0, 'group': 0, 'today': 0}

    def on_search_text_changed(self):
        """Handle real-time search as user types"""
        if hasattr(self, 'search_timer'):
            self.search_timer.stop()
        
        self.search_timer = QTimer()
        self.search_timer.timeout.connect(self.handle_filter)
        self.search_timer.setSingleShot(True)
        self.search_timer.start(300)  # 300ms delay

    def handle_filter(self):
        """Handle filtering functionality"""
        self.load_sessions()

    def apply_filters(self):
        """Apply filters to the table"""
        self.load_sessions()

    def clear_filters(self):
        """Clear all filters"""
        self.trainer_input.clear()
        self.client_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.date_picker.setDate(QDate.currentDate())
        self.load_sessions()

    def load_sessions(self):
        """Load sessions with filters applied"""
        trainer = self.trainer_input.text().strip()
        client = self.client_input.text().strip()
        session_type = self.type_combo.currentText()
        date = self.date_picker.date().toString('yyyy-MM-dd')
        
        sessions = self.controller.get_all()
        filtered = []
        
        for s in sessions:
            # s: id, client_id, trainer_name, session_date, session_type, is_group
            show = True
            
            if trainer and trainer.lower() not in (s[2] or '').lower():
                show = False
            
            if client:
                client_name = self.get_client_name_by_id(s[1])
                client_code = self.get_client_code_by_id(s[1])
                if (client.lower() not in (client_name or '').lower() and 
                    client.lower() not in (client_code or '').lower()):
                    show = False
            
            if session_type != self.tr('All Types'):
                if session_type.lower() not in (s[4] or '').lower():
                    show = False
            
            # Only filter by date if it's not today's date
            current_date = QDate.currentDate().toString('yyyy-MM-dd')
            if date != current_date and date != (s[3] or ''):
                show = False
            
            if show:
                filtered.append(s)
        
        self.populate_table(filtered)

    def populate_table(self, sessions):
        """Populate table with session data"""
        self.table.setRowCount(0)
        
        for s in sessions:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Get client info
            client_code = self.get_client_code_by_id(s[1])
            client_name = self.get_client_name_by_id(s[1])
            
            # Add data to table
            items = [
                QTableWidgetItem(str(client_code or '')),
                QTableWidgetItem(str(client_name or '')),
                QTableWidgetItem(str(s[2] or '')),  # trainer_name
                QTableWidgetItem(str(s[3] or '')),  # session_date
                QTableWidgetItem(str(s[4] or '')),  # session_type
                QTableWidgetItem(self.tr('Yes') if s[5] else self.tr('No'))  # is_group
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Set row height
            self.table.setRowHeight(row, 50)

    def open_add_session(self):
        """Open dialog to add new session"""
        code, ok = QInputDialog.getText(self, self.tr('Client Code'), 
                                       self.tr('Enter client code:'))
        if not ok or not code:
            return
        
        client_id = self.get_client_id_by_code(code)
        if not client_id:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr('❌ Client not found.'))
            return
        
        trainer, ok = QInputDialog.getText(self, self.tr('Trainer Name'), 
                                         self.tr('Enter trainer name:'))
        if not ok or not trainer:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Trainer name is required.'))
            return
        
        session_date, ok = QInputDialog.getText(self, self.tr('Session Date'), 
                                              self.tr('Enter date (yyyy-MM-dd):'))
        if not ok or not session_date:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Session date is required.'))
            return
        
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', session_date):
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Date must be in yyyy-MM-dd format.'))
            return
        
        session_type, ok = QInputDialog.getItem(
            self, self.tr('Session Type'), 
            self.tr('Select type:'), 
            [self.tr('Private'), self.tr('Group')], 
            0, False
        )
        if not ok:
            return
        
        is_group = 1 if session_type == self.tr('Group') else 0
        
        try:
            self.controller.add_session(client_id, trainer, session_date, session_type, is_group)
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ Session added successfully!'))
            self.load_sessions()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error adding session: {str(e)}'))

    def open_edit_dialog(self):
        """Open dialog to edit selected session"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a session to edit.'))
            return
        
        # Get current session data
        client_code = self.table.item(row, 0).text()
        trainer = self.table.item(row, 2).text()
        session_date = self.table.item(row, 3).text()
        session_type = self.table.item(row, 4).text()
        
        # Edit trainer
        new_trainer, ok = QInputDialog.getText(
            self, self.tr('Edit Trainer'), 
            self.tr('Trainer name:'), 
            text=trainer
        )
        if not ok:
            return
        
        # Edit date
        new_date, ok = QInputDialog.getText(
            self, self.tr('Edit Date'), 
            self.tr('Session date (yyyy-MM-dd):'), 
            text=session_date
        )
        if not ok:
            return
        
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', new_date):
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Date must be in yyyy-MM-dd format.'))
            return
        
        # Edit type
        new_type, ok = QInputDialog.getItem(
            self, self.tr('Edit Type'), 
            self.tr('Session type:'), 
            [self.tr('Private'), self.tr('Group')], 
            0 if session_type == self.tr('Private') else 1, 
            False
        )
        if not ok:
            return
        
        QMessageBox.information(self, self.tr('Info'), 
                              self.tr('ℹ️ Session editing feature needs to be implemented in the controller.'))

    def handle_delete(self):
        """Handle session deletion"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a session to delete.'))
            return
        
        client_name = self.table.item(row, 1).text()
        trainer = self.table.item(row, 2).text()
        session_date = self.table.item(row, 3).text()
        
        reply = QMessageBox.question(
            self, 
            self.tr('Confirm Delete'), 
            self.tr(f'Are you sure you want to delete this session?\n\n'
                   f'Client: {client_name}\n'
                   f'Trainer: {trainer}\n'
                   f'Date: {session_date}\n\n'
                   f'This action cannot be undone.'), 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, self.tr('Info'), 
                                  self.tr('ℹ️ Session deletion feature needs to be implemented in the controller.'))

    def export_data(self):
        """Export session data"""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                self.tr('Export Sessions Data'),
                f'sessions_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                'CSV files (*.csv)'
            )
            
            if filename:
                sessions = self.controller.get_all()
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Write header
                    writer.writerow(['Client Code', 'Client Name', 'Trainer', 'Date', 'Type', 'Group Session'])
                    
                    # Write data
                    for session in sessions:
                        client_code = self.get_client_code_by_id(session[1])
                        client_name = self.get_client_name_by_id(session[1])
                        is_group = 'Yes' if session[5] else 'No'
                        
                        row = [
                            client_code,
                            client_name,
                            session[2],  # trainer_name
                            session[3],  # session_date
                            session[4],  # session_type
                            is_group
                        ]
                        writer.writerow(row)
                
                QMessageBox.information(self, self.tr('Export Complete'), 
                                      self.tr(f'✅ Data exported successfully to:\n{filename}'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Export Error'), 
                               self.tr(f'❌ Error exporting data: {str(e)}'))

    def get_client_name_by_id(self, client_id):
        """Get client name by ID"""
        try:
            from models.db_manager import DBManager
            db = DBManager()
            row = db.fetchone('SELECT name FROM clients WHERE id=?', (client_id,))
            return row[0] if row else 'Unknown'
        except:
            return 'Unknown'

    def get_client_code_by_id(self, client_id):
        """Get client code by ID"""
        try:
            from models.db_manager import DBManager
            db = DBManager()
            row = db.fetchone('SELECT client_code FROM clients WHERE id=?', (client_id,))
            return row[0] if row else 'Unknown'
        except:
            return 'Unknown'

    def get_client_id_by_code(self, code):
        """Get client ID by code"""
        try:
            from models.db_manager import DBManager
            db = DBManager()
            row = db.fetchone('SELECT id FROM clients WHERE client_code=?', (code,))
            return row[0] if row else None
        except:
            return None

    def tr(self, text):
        """Translation method placeholder"""
        return text