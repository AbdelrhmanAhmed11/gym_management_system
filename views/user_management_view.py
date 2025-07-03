from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, 
                             QSizePolicy, QFrame, QHeaderView, QComboBox, QSpacerItem, 
                             QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPalette
from controllers.user_controller import UserController

class UserManagementView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = UserController()
        self.init_ui()
        self.apply_styles()
        self.load_users()

    def init_ui(self):
        self.setWindowTitle(self.tr('User Management'))
        
        # Main layout with NO margins or spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header_section = self.create_header_section()
        main_layout.addWidget(header_section)

        # Search section
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
        title_label = QLabel(self.tr('👥 User Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Manage system users, roles, and access permissions'))
        subtitle_label.setObjectName("pageSubtitle")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_search_section(self):
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_frame.setFixedHeight(100)
        
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(40, 25, 40, 25)
        search_layout.setSpacing(20)
        
        # Search icon label
        search_icon = QLabel("🔍")
        search_icon.setObjectName("searchIcon")
        search_icon.setFixedSize(30, 30)
        search_icon.setAlignment(Qt.AlignCenter)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText(self.tr('Search by username or full name...'))
        self.search_input.setFixedHeight(45)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        
        # Role filter dropdown
        self.role_filter = QComboBox()
        self.role_filter.setObjectName("filterCombo")
        self.role_filter.setFixedHeight(45)
        self.role_filter.setFixedWidth(150)
        self.role_filter.addItems([
            self.tr('All Roles'),
            self.tr('Admin'),
            self.tr('Receptionist')
        ])
        self.role_filter.currentTextChanged.connect(self.apply_filter)
        
        # Search button
        self.search_btn = QPushButton(self.tr('🔍 Search'))
        self.search_btn.setObjectName("searchButton")
        self.search_btn.setFixedHeight(45)
        self.search_btn.setFixedWidth(120)
        self.search_btn.clicked.connect(self.handle_search)
        
        # Clear button
        self.clear_btn = QPushButton(self.tr('✖ Clear'))
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.setFixedHeight(45)
        self.clear_btn.setFixedWidth(100)
        self.clear_btn.clicked.connect(self.clear_search)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.role_filter)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_btn)
        
        search_frame.setLayout(search_layout)
        
        return search_frame

    def create_stats_section(self):
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_frame.setFixedHeight(120)
        
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(40, 20, 40, 20)
        stats_layout.setSpacing(15)
        
        # Get user statistics
        stats = self.get_user_stats()
        
        # Create stat cards - MATCHING REPORTS PAGE DESIGN
        stat_cards = [
            ('👥', self.tr('Total Users'), str(stats['total']), '#e63946'),
            ('🛡️', self.tr('Administrators'), str(stats['admins']), '#dc3545'),
            ('👋', self.tr('Receptionists'), str(stats['receptionists']), '#38b000'),
            ('🔐', self.tr('Active Sessions'), str(stats['active']), '#17a2b8')
        ]
        
        for icon, label, value, color in stat_cards:
            card = self.create_stat_card(icon, label, value, color)
            stats_layout.addWidget(card)
        
        stats_frame.setLayout(stats_layout)
        
        return stats_frame

    def create_stat_card(self, icon, label, value, color):
        """Create stat card with icon and colored title+count centered vertically and horizontally."""
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(80)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)

        # Icon centered
        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")
        icon_label.setAlignment(Qt.AlignCenter)

        # Colored title + count centered
        title_count_label = QLabel(f"{label} ({value})")
        title_count_label.setObjectName("statValue")
        title_count_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        title_count_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_count_label, alignment=Qt.AlignCenter)

        card.setLayout(layout)
        return card

    def create_table_section(self):
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(40, 30, 40, 30)
        table_layout.setSpacing(20)
        
        # Table title
        table_title = QLabel(self.tr('👥 User Directory'))
        table_title.setObjectName("sectionTitle")
        
        # Create table
        self.table = QTableWidget(0, 4)
        self.table.setObjectName("usersTable")
        self.table.setHorizontalHeaderLabels([
            self.tr('ID'), 
            self.tr('Username'), 
            self.tr('Role'), 
            self.tr('Full Name')
        ])
        
        # Configure table for responsiveness
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
        self.table.doubleClicked.connect(self.handle_change_password)
        
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
        actions_title = QLabel(self.tr('⚡ User Actions'))
        actions_title.setObjectName("actionsTitle")
        actions_layout.addWidget(actions_title)
        
        # Buttons layout - responsive
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Add button
        self.add_btn = QPushButton(self.tr('➕ Add User'))
        self.add_btn.setObjectName("addButton")
        self.add_btn.setFixedHeight(45)
        self.add_btn.setMinimumWidth(140)
        self.add_btn.clicked.connect(self.open_add_user)
        
        # Remove button
        self.remove_btn = QPushButton(self.tr('🗑️ Remove User'))
        self.remove_btn.setObjectName("deleteButton")
        self.remove_btn.setFixedHeight(45)
        self.remove_btn.setMinimumWidth(150)
        self.remove_btn.clicked.connect(self.handle_remove_user)
        
        # Change password button
        self.change_pass_btn = QPushButton(self.tr('🔑 Change Password'))
        self.change_pass_btn.setObjectName("editButton")
        self.change_pass_btn.setFixedHeight(45)
        self.change_pass_btn.setMinimumWidth(170)
        self.change_pass_btn.clicked.connect(self.handle_change_password)
        
        # Refresh button
        self.refresh_btn = QPushButton(self.tr('🔄 Refresh'))
        self.refresh_btn.setObjectName("refreshButton")
        self.refresh_btn.setFixedHeight(45)
        self.refresh_btn.setMinimumWidth(120)
        self.refresh_btn.clicked.connect(self.load_users)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.remove_btn)
        buttons_layout.addWidget(self.change_pass_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
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
            QTableWidget#usersTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                font-size: 13px;
                selection-background-color: #e63946;
                selection-color: white;
                border-radius: 8px;
            }
            
            QTableWidget#usersTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#usersTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QTableWidget#usersTable::item:hover {
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
            
            QPushButton#refreshButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #0f7b8a);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#refreshButton:hover {
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
                border-radius: 6px;
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
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QInputDialog QComboBox:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QInputDialog QComboBox QAbstractItemView {
                background-color: #404040;
                border: 2px solid #e63946;
                border-radius: 6px;
                selection-background-color: #e63946;
                color: #ffffff;
            }
        """
        self.setStyleSheet(style_sheet)

    def get_user_stats(self):
        """Get user statistics"""
        try:
            users = self.controller.get_all()
            total = len(users)
            admins = len([u for u in users if u[2] == 'admin'])
            receptionists = len([u for u in users if u[2] == 'receptionist'])
            active = total  # For now, assume all users are active
            
            return {
                'total': total,
                'admins': admins,
                'receptionists': receptionists,
                'active': active
            }
        except:
            return {'total': 0, 'admins': 0, 'receptionists': 0, 'active': 0}

    def load_users(self):
        """Load users into the table"""
        users = self.controller.get_all()
        self.table.setRowCount(0)
        
        for user in users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            for col, value in enumerate(user):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                item.setTextAlignment(Qt.AlignCenter)
                
                # Add role icons
                if col == 2:  # Role column
                    if value == 'admin':
                        item.setText(f"🛡️ {value.capitalize()}")
                    elif value == 'receptionist':
                        item.setText(f"👋 {value.capitalize()}")
                
                self.table.setItem(row, col, item)
            
            # Set row height
            self.table.setRowHeight(row, 50)

    def on_search_text_changed(self):
        """Handle real-time search as user types"""
        if hasattr(self, 'search_timer'):
            self.search_timer.stop()
        
        self.search_timer = QTimer()
        self.search_timer.timeout.connect(self.handle_search)
        self.search_timer.setSingleShot(True)
        self.search_timer.start(300)  # 300ms delay

    def handle_search(self):
        """Handle search functionality"""
        keyword = self.search_input.text().strip().lower()
        
        for row in range(self.table.rowCount()):
            show_row = True
            
            if keyword:
                # Check username and full name
                username = self.table.item(row, 1).text().lower()
                full_name = self.table.item(row, 3).text().lower()
                
                if keyword not in username and keyword not in full_name:
                    show_row = False
            
            self.table.setRowHidden(row, not show_row)
        
        self.apply_filter()

    def apply_filter(self):
        """Apply role filter"""
        filter_text = self.role_filter.currentText()
        
        for row in range(self.table.rowCount()):
            if self.table.isRowHidden(row):
                continue  # Skip if already hidden by search
            
            show_row = True
            
            if filter_text != self.tr('All Roles'):
                role_item = self.table.item(row, 2)
                if role_item:
                    role_text = role_item.text().lower()
                    
                    if filter_text == self.tr('Admin') and 'admin' not in role_text:
                        show_row = False
                    elif filter_text == self.tr('Receptionist') and 'receptionist' not in role_text:
                        show_row = False
            
            self.table.setRowHidden(row, not show_row)

    def clear_search(self):
        """Clear search and filters"""
        self.search_input.clear()
        self.role_filter.setCurrentIndex(0)
        self.load_users()

    def open_add_user(self):
        """Open dialog to add new user"""
        username, ok = QInputDialog.getText(self, self.tr('👤 Add User'), self.tr('Enter username:'))
        if not ok or not username.strip():
            return
        
        username = username.strip()
        
        if self.controller.get_by_username(username):
            QMessageBox.warning(self, self.tr('Error'), self.tr('❌ Username already exists.'))
            return
        
        password, ok = QInputDialog.getText(self, self.tr('🔐 Set Password'), self.tr('Enter password:'), QLineEdit.Password)
        if not ok or not password:
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, self.tr('Error'), self.tr('❌ Password must be at least 6 characters.'))
            return
        
        role, ok = QInputDialog.getItem(self, self.tr('👥 Select Role'), self.tr('Select user role:'), 
                                       ['admin', 'receptionist'], 0, False)
        if not ok:
            return
        
        full_name, ok = QInputDialog.getText(self, self.tr('📝 Full Name'), self.tr('Enter full name:'))
        if not ok or not full_name.strip():
            return
        
        full_name = full_name.strip()
        
        try:
            self.controller.add_user(username, password, role, full_name)
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ User added successfully!'))
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error adding user: {str(e)}'))

    def handle_remove_user(self):
        """Handle user removal"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a user to remove.'))
            return
        
        user_id = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        if username == 'admin':
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('❌ Cannot remove the main admin user.'))
            return
        
        reply = QMessageBox.question(
            self, 
            self.tr('Confirm Delete'), 
            self.tr(f'Are you sure you want to remove user "{username}"?\n\nThis action cannot be undone.'), 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.controller.remove_user(user_id)
                QMessageBox.information(self, self.tr('Success'), 
                                      self.tr('✅ User removed successfully!'))
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, self.tr('Error'), 
                                   self.tr(f'❌ Error removing user: {str(e)}'))

    def handle_change_password(self):
        """Handle password change"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a user to change password.'))
            return
        
        user_id = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        new_password, ok = QInputDialog.getText(
            self, 
            self.tr(f'🔑 Change Password for {username}'), 
            self.tr('Enter new password:'), 
            QLineEdit.Password
        )
        
        if not ok or not new_password:
            return
        
        if len(new_password) < 6:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('❌ Password must be at least 6 characters.'))
            return
        
        try:
            self.controller.change_password(user_id, new_password)
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ Password changed successfully!'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error changing password: {str(e)}'))

    def tr(self, text):
        """Translation method placeholder"""
        return self.translator.translate(text)

    def retranslate_ui(self):
        if self.translator.get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        
        # Header
        for widget in self.findChildren(QLabel, 'pageTitle'):
            widget.setText(self.tr('👥 User Management'))
        for widget in self.findChildren(QLabel, 'pageSubtitle'):
            widget.setText(self.tr('Manage system users, roles, and access permissions'))
        
        # Search section
        self.search_input.setPlaceholderText(self.tr('Search by username or full name...'))
        self.role_filter.setItemText(0, self.tr('All Roles'))
        self.role_filter.setItemText(1, self.tr('Admin'))
        self.role_filter.setItemText(2, self.tr('Receptionist'))
        self.search_btn.setText(self.tr('🔍 Search'))
        self.clear_btn.setText(self.tr('✖ Clear'))
        
        # Table section
        for widget in self.findChildren(QLabel, 'sectionTitle'):
            widget.setText(self.tr('👥 User Directory'))
        self.table.setHorizontalHeaderLabels([
            self.tr('ID'),
            self.tr('Username'),
            self.tr('Role'),
            self.tr('Full Name')
        ])
        
        # Actions section
        for widget in self.findChildren(QLabel, 'actionsTitle'):
            widget.setText(self.tr('⚡ User Actions'))
        self.add_btn.setText(self.tr('➕ Add User'))
        self.remove_btn.setText(self.tr('🗑️ Remove User'))
        self.change_pass_btn.setText(self.tr('🔑 Change Password'))
        self.refresh_btn.setText(self.tr('🔄 Refresh'))
        
        # Reload users to refresh display
        self.load_users()