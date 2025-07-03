from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                                QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy,
                                QFrame, QHeaderView, QComboBox, QGraphicsDropShadowEffect,
                                QSpacerItem, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPalette
from controllers.clients_controller import ClientsController
from views.client_profile_dialog import ClientProfileDialog
import uuid
from datetime import datetime, timedelta

class ClientsView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = ClientsController()
        self.init_ui()
        self.apply_styles()
        self.load_clients()
        # Set layout direction based on language
        if self.translator.get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)

    def init_ui(self):
        self.setWindowTitle(self.tr('Clients Management'))
        
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
        title_label = QLabel(self.tr('👥 Clients Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Manage gym members, subscriptions, and client information'))
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
        self.search_input.setPlaceholderText(self.tr('Search by name, code, or phone number...'))
        self.search_input.setFixedHeight(45)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        
        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.setObjectName("filterCombo")
        self.filter_combo.setFixedHeight(45)
        self.filter_combo.setFixedWidth(150)
        self.filter_combo.addItems([
            self.tr('All Clients'),
            self.tr('Active'),
            self.tr('Expired'),
            self.tr('Ending Soon')
        ])
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        
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
        search_layout.addWidget(self.filter_combo)
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
        
        # Get client statistics
        stats = self.get_client_stats()
        
        # Create stat cards
        stat_cards = [
            ('👥', self.tr('Total'), str(stats['total']), '#e63946'),
            ('✅', self.tr('Active'), str(stats['active']), '#38b000'),
            ('⏰', self.tr('Ending Soon'), str(stats['ending_soon']), '#ffcc00'),
            ('❌', self.tr('Expired'), str(stats['expired']), '#dc3545')
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
        table_title = QLabel(self.tr('Client Directory'))
        table_title.setObjectName("sectionTitle")
        
        # Create table
        self.table = QTableWidget(0, 7)
        self.table.setObjectName("clientsTable")
        self.table.setHorizontalHeaderLabels([
            self.tr('Code'), 
            self.tr('Name'), 
            self.tr('Phone'), 
            self.tr('Subscription'), 
            self.tr('Start Date'), 
            self.tr('End Date'),
            self.tr('Status')
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
        self.add_btn = QPushButton(self.tr('➕ Add New Client'))
        self.add_btn.setObjectName("addButton")
        self.add_btn.setFixedHeight(45)
        self.add_btn.setFixedWidth(160)
        self.add_btn.clicked.connect(self.open_add_dialog)
        
        # Edit button
        self.edit_btn = QPushButton(self.tr('✏️ Edit Client'))
        self.edit_btn.setObjectName("editButton")
        self.edit_btn.setFixedHeight(45)
        self.edit_btn.setFixedWidth(140)
        self.edit_btn.clicked.connect(self.open_edit_dialog)
        
        # Delete button
        self.delete_btn = QPushButton(self.tr('🗑️ Delete Client'))
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.setFixedHeight(45)
        self.delete_btn.setFixedWidth(140)
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
            QTableWidget#clientsTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                font-size: 13px;
                selection-background-color: #e63946;
                selection-color: white;
            }
            
            QTableWidget#clientsTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#clientsTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QTableWidget#clientsTable::item:hover {
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
        """
        self.setStyleSheet(style_sheet)

    def get_client_stats(self):
        """Get client statistics"""
        try:
            clients = self.controller.load_all()
            total = len(clients)
            active = 0
            expired = 0
            ending_soon = 0
            
            today = datetime.now().date()
            week_from_now = today + timedelta(days=7)
            
            for client in clients:
                try:
                    end_date = datetime.strptime(client[5], '%Y-%m-%d').date()
                    if end_date >= today:
                        active += 1
                        if end_date <= week_from_now:
                            ending_soon += 1
                    else:
                        expired += 1
                except:
                    pass
            
            return {
                'total': total,
                'active': active,
                'expired': expired,
                'ending_soon': ending_soon
            }
        except:
            return {'total': 0, 'active': 0, 'expired': 0, 'ending_soon': 0}

    def load_clients(self):
        """Load clients into the table"""
        clients = self.controller.load_all()
        self.table.setRowCount(0)
        
        today = datetime.now().date()
        week_from_now = today + timedelta(days=7)
        
        for row_data in clients:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add regular data
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Add status column
            try:
                end_date = datetime.strptime(row_data[5], '%Y-%m-%d').date()
                if end_date < today:
                    status = "❌ Expired"
                    status_color = "#dc3545"
                elif end_date <= week_from_now:
                    status = "⏰ Ending Soon"
                    status_color = "#ffcc00"
                else:
                    status = "✅ Active"
                    status_color = "#38b000"
                
                status_item = QTableWidgetItem(status)
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 6, status_item)
                
                # Set row height
                self.table.setRowHeight(row, 50)
                
            except:
                status_item = QTableWidgetItem("❓ Unknown")
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 6, status_item)

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
        keyword = self.search_input.text().strip()
        if keyword:
            clients = self.controller.search(keyword)
        else:
            clients = self.controller.load_all()
        
        self.populate_table(clients)
        self.apply_filter()

    def apply_filter(self):
        """Apply filter based on status"""
        filter_text = self.filter_combo.currentText()
        
        for row in range(self.table.rowCount()):
            show_row = True
            
            if filter_text != self.tr('All Clients'):
                status_item = self.table.item(row, 6)
                if status_item:
                    status = status_item.text()
                    
                    if filter_text == self.tr('Active') and '✅' not in status:
                        show_row = False
                    elif filter_text == self.tr('Expired') and '❌' not in status:
                        show_row = False
                    elif filter_text == self.tr('Ending Soon') and '⏰' not in status:
                        show_row = False
            
            self.table.setRowHidden(row, not show_row)

    def populate_table(self, clients):
        """Populate table with client data"""
        self.table.setRowCount(0)
        
        today = datetime.now().date()
        week_from_now = today + timedelta(days=7)
        
        for row_data in clients:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add regular data
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Add status column
            try:
                end_date = datetime.strptime(row_data[5], '%Y-%m-%d').date()
                if end_date < today:
                    status = '❌ Expired'
                elif end_date <= week_from_now:
                    status = '⏰ Ending Soon'
                else:
                    status = '✅ Active'
                status_item = QTableWidgetItem(self.tr(status))
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 6, status_item)
                
                self.table.setRowHeight(row, 50)
                
            except:
                status_item = QTableWidgetItem(self.tr("Unknown"))
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 6, status_item)

    def clear_search(self):
        """Clear search and filters"""
        self.search_input.clear()
        self.filter_combo.setCurrentIndex(0)
        self.load_clients()

    def open_add_dialog(self):
        """Open dialog to add new client"""
        dlg = ClientProfileDialog(self.translator)
        # Auto-generate client code
        code = str(uuid.uuid4())[:8].upper()
        dlg.code_input.setText(code)
        
        if dlg.exec_() == dlg.Accepted:
            data = (
                dlg.code_input.text(),
                dlg.name_input.text(),
                dlg.phone_input.text(),
                dlg.sub_type_combo.currentText(),
                dlg.start_date.date().toString('yyyy-MM-dd'),
                dlg.end_date.date().toString('yyyy-MM-dd')
            )
            try:
                self.controller.add(data)
                QMessageBox.information(self, self.tr('Success'), 
                                    self.tr('✅ Client added successfully!'))
                self.load_clients()
            except Exception as e:
                QMessageBox.critical(self, self.tr('Error'), 
                                self.tr(f'❌ Error adding client: {str(e)}'))

    def open_edit_dialog(self):
        """Open dialog to edit selected client"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                self.tr('Please select a client to edit.'))
            return
        
        code = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        phone = self.table.item(row, 2).text()
        sub_type = self.table.item(row, 3).text()
        start = self.table.item(row, 4).text()
        end = self.table.item(row, 5).text()
        
        dlg = ClientProfileDialog(self.translator)
        dlg.code_input.setText(code)
        dlg.code_input.setEnabled(False)  # Don't allow code editing
        dlg.name_input.setText(name)
        dlg.phone_input.setText(phone)
        dlg.sub_type_combo.setCurrentText(sub_type)
        dlg.start_date.setDate(dlg.start_date.date().fromString(start, 'yyyy-MM-dd'))
        dlg.end_date.setDate(dlg.end_date.date().fromString(end, 'yyyy-MM-dd'))
        
        if dlg.exec_() == dlg.Accepted:
            data = (
                dlg.name_input.text(),
                dlg.phone_input.text(),
                dlg.sub_type_combo.currentText(),
                dlg.start_date.date().toString('yyyy-MM-dd'),
                dlg.end_date.date().toString('yyyy-MM-dd')
            )
            try:
                self.controller.update(code, data)
                QMessageBox.information(self, self.tr('Success'), 
                                    self.tr('✅ Client updated successfully!'))
                self.load_clients()
            except Exception as e:
                QMessageBox.critical(self, self.tr('Error'), 
                                self.tr(f'❌ Error updating client: {str(e)}'))

    def handle_delete(self):
        """Handle client deletion"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                self.tr('Please select a client to delete.'))
            return
        
        code = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 
            self.tr('Confirm Delete'), 
            self.tr(f'Are you sure you want to delete client "{name}" ({code})?\n\nThis action cannot be undone.'), 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.controller.delete(code)
                QMessageBox.information(self, self.tr('Success'), 
                                    self.tr('✅ Client deleted successfully!'))
                self.load_clients()
            except Exception as e:
                QMessageBox.critical(self, self.tr('Error'), 
                                self.tr(f'❌ Error deleting client: {str(e)}'))

    def export_data(self):
        """Export client data"""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                self.tr('Export Clients Data'),
                f'clients_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                'CSV files (*.csv)'
            )
            
            if filename:
                clients = self.controller.load_all()
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Write header
                    writer.writerow(['Code', 'Name', 'Phone', 'Subscription', 'Start Date', 'End Date', 'Status'])
                    
                    # Write data
                    today = datetime.now().date()
                    week_from_now = today + timedelta(days=7)
                    
                    for client in clients:
                        try:
                            end_date = datetime.strptime(client[5], '%Y-%m-%d').date()
                            if end_date < today:
                                status = "Expired"
                            elif end_date <= week_from_now:
                                status = "Ending Soon"
                            else:
                                status = "Active"
                        except:
                            status = "Unknown"
                        
                        row = list(client) + [status]
                        writer.writerow(row)
                
                QMessageBox.information(self, self.tr('Export Complete'), 
                                    self.tr(f'✅ Data exported successfully to:\n{filename}'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Export Error'), 
                            self.tr(f'❌ Error exporting data: {str(e)}'))

    def tr(self, text):
        """Translation method placeholder"""
        return self.translator.translate(text)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr('Clients Management'))
        # Update header
        if hasattr(self, 'header_frame'):
            title_label = self.header_frame.findChild(QLabel, 'pageTitle')
            if title_label:
                title_label.setText(self.tr('👥 Clients Management'))
            subtitle_label = self.header_frame.findChild(QLabel, 'pageSubtitle')
            if subtitle_label:
                subtitle_label.setText(self.tr('Manage gym members, subscriptions, and client information'))
        # Update search section
        if hasattr(self, 'search_input'):
            self.search_input.setPlaceholderText(self.tr('Search by name, code, or phone number...'))
        if hasattr(self, 'filter_combo'):
            self.filter_combo.clear()
            self.filter_combo.addItems([
                self.tr('All Clients'),
                self.tr('Active'),
                self.tr('Expired'),
                self.tr('Ending Soon')
            ])
        if hasattr(self, 'search_btn'):
            self.search_btn.setText(self.tr('🔍 Search'))
        if hasattr(self, 'clear_btn'):
            self.clear_btn.setText(self.tr('✖ Clear'))
        # Update stats section
        if hasattr(self, 'stats_frame'):
            for card in self.stats_frame.findChildren(QFrame, 'statCard'):
                label_widget = card.findChild(QLabel, 'statLabel')
                if label_widget:
                    label_widget.setText(self.tr(label_widget.text()))
        # Update table headers
        if hasattr(self, 'table'):
            self.table.setHorizontalHeaderLabels([
                self.tr('Code'),
                self.tr('Name'),
                self.tr('Phone'),
                self.tr('Subscription'),
                self.tr('Start Date'),
                self.tr('End Date'),
                self.tr('Status')
            ])
        # Update action buttons
        if hasattr(self, 'add_btn'):
            self.add_btn.setText(self.tr('Add New Client'))
        if hasattr(self, 'edit_btn'):
            self.edit_btn.setText(self.tr('Edit Client'))
        if hasattr(self, 'delete_btn'):
            self.delete_btn.setText(self.tr('Delete Client'))
        if hasattr(self, 'export_btn'):
            self.export_btn.setText(self.tr('Export Data'))