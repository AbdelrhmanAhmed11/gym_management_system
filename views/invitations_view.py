from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy,
                             QFrame, QHeaderView, QComboBox, QInputDialog,
                             QSpacerItem, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPalette
from controllers.invitation_controller import InvitationController
from models.client_model import ClientModel
from datetime import datetime, timedelta

class InvitationsView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = InvitationController()
        self.client_model = ClientModel()
        self.init_ui()
        self.apply_styles()
        self.load_invitations()

    def init_ui(self):
        self.setWindowTitle(self.tr('Invitations Management'))
        
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
        title_label = QLabel(self.tr('🎯 Invitations Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Track client referrals, manage friend invitations, and monitor invitation status'))
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
        
        # Client search input
        self.client_input = QLineEdit()
        self.client_input.setObjectName("searchInput")
        self.client_input.setPlaceholderText(self.tr('Search by client code/name...'))
        self.client_input.setFixedHeight(45)
        self.client_input.textChanged.connect(self.on_search_text_changed)
        
        # Friend search input
        self.friend_input = QLineEdit()
        self.friend_input.setObjectName("searchInput")
        self.friend_input.setPlaceholderText(self.tr('Search by friend name/phone...'))
        self.friend_input.setFixedHeight(45)
        self.friend_input.textChanged.connect(self.on_search_text_changed)
        
        first_row.addWidget(search_icon)
        first_row.addWidget(self.client_input)
        first_row.addWidget(self.friend_input)
        
        # Second row - Filters and actions
        second_row = QHBoxLayout()
        second_row.setSpacing(20)
        
        # Status filter
        self.status_combo = QComboBox()
        self.status_combo.setObjectName("filterCombo")
        self.status_combo.setFixedHeight(45)
        self.status_combo.setFixedWidth(150)
        self.status_combo.addItems([
            self.tr('All Status'),
            self.tr('Tagged'),
            self.tr('Not Tagged')
        ])
        self.status_combo.currentTextChanged.connect(self.apply_filters)
        
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
        
        second_row.addWidget(QLabel(self.tr('Status:')))
        second_row.addWidget(self.status_combo)
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
        
        # Get invitation statistics
        stats = self.get_invitation_stats()
        
        # Create stat cards
        stat_cards = [
            ('🎯', self.tr('Total Invitations'), str(stats['total']), '#e63946'),
            ('✅', self.tr('Tagged'), str(stats['tagged']), '#38b000'),
            ('⏳', self.tr('Pending'), str(stats['pending']), '#ffcc00'),
            ('📅', self.tr('This Month'), str(stats['this_month']), '#17a2b8')
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
        table_title = QLabel(self.tr('Invitation Records'))
        table_title.setObjectName("sectionTitle")
        
        # Create table
        self.table = QTableWidget(0, 6)
        self.table.setObjectName("invitationsTable")
        self.table.setHorizontalHeaderLabels([
            self.tr('Client Code'),
            self.tr('Client Name'), 
            self.tr('Friend Name'), 
            self.tr('Friend Phone'), 
            self.tr('Invited Date'),
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
        self.add_btn = QPushButton(self.tr('➕ Add New Invitation'))
        self.add_btn.setObjectName("addButton")
        self.add_btn.setFixedHeight(45)
        self.add_btn.setFixedWidth(180)
        self.add_btn.clicked.connect(self.open_add_invitation)
        
        # Tag button
        self.tag_btn = QPushButton(self.tr('🏷️ Mark as Tagged'))
        self.tag_btn.setObjectName("editButton")
        self.tag_btn.setFixedHeight(45)
        self.tag_btn.setFixedWidth(150)
        self.tag_btn.clicked.connect(self.mark_as_tagged)
        
        # Delete button
        self.delete_btn = QPushButton(self.tr('🗑️ Delete Invitation'))
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.setFixedHeight(45)
        self.delete_btn.setFixedWidth(160)
        self.delete_btn.clicked.connect(self.handle_delete)
        
        # Export button
        self.export_btn = QPushButton(self.tr('📊 Export Data'))
        self.export_btn.setObjectName("exportButton")
        self.export_btn.setFixedHeight(45)
        self.export_btn.setFixedWidth(140)
        self.export_btn.clicked.connect(self.export_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.tag_btn)
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
            QTableWidget#invitationsTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                font-size: 13px;
                selection-background-color: #e63946;
                selection-color: white;
            }
            
            QTableWidget#invitationsTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#invitationsTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QTableWidget#invitationsTable::item:hover {
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
        """
        self.setStyleSheet(style_sheet)

    def get_invitation_stats(self):
        """Get invitation statistics"""
        try:
            invitations = self.controller.get_all()
            total = len(invitations)
            tagged = 0
            pending = 0
            this_month = 0
            
            current_month = datetime.now().strftime('%Y-%m')
            
            for invitation in invitations:
                # invitation: id, client_id, friend_name, friend_phone, invited_at, tagged
                if invitation[5]:  # tagged
                    tagged += 1
                else:
                    pending += 1
                
                # Check if invitation is from this month
                if invitation[4] and invitation[4].startswith(current_month):
                    this_month += 1
            
            return {
                'total': total,
                'tagged': tagged,
                'pending': pending,
                'this_month': this_month
            }
        except:
            return {'total': 0, 'tagged': 0, 'pending': 0, 'this_month': 0}

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
        self.load_invitations()

    def apply_filters(self):
        """Apply filters to the table"""
        self.load_invitations()

    def clear_filters(self):
        """Clear all filters"""
        self.client_input.clear()
        self.friend_input.clear()
        self.status_combo.setCurrentIndex(0)
        self.load_invitations()

    def load_invitations(self):
        """Load invitations with filters applied"""
        client_filter = self.client_input.text().strip()
        friend_filter = self.friend_input.text().strip()
        status_filter = self.status_combo.currentText()
        
        invitations = self.controller.get_all()
        filtered = []
        
        for inv in invitations:
            # inv: id, client_id, friend_name, friend_phone, invited_at, tagged
            show = True
            
            if client_filter:
                client_name = self.get_client_name_by_id(inv[1])
                client_code = self.get_client_code_by_id(inv[1])
                if (client_filter.lower() not in (client_name or '').lower() and 
                    client_filter.lower() not in (client_code or '').lower()):
                    show = False
            
            if friend_filter:
                if (friend_filter.lower() not in (inv[2] or '').lower() and 
                    friend_filter.lower() not in (inv[3] or '').lower()):
                    show = False
            
            if status_filter != self.tr('All Status'):
                if status_filter == self.tr('Tagged') and not inv[5]:
                    show = False
                elif status_filter == self.tr('Not Tagged') and inv[5]:
                    show = False
            
            if show:
                filtered.append(inv)
        
        self.populate_table(filtered)

    def populate_table(self, invitations):
        """Populate table with invitation data"""
        self.table.setRowCount(0)
        
        for inv in invitations:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Get client info
            client_code = self.get_client_code_by_id(inv[1])
            client_name = self.get_client_name_by_id(inv[1])
            
            # Format date
            invited_date = inv[4] if inv[4] else 'Unknown'
            if invited_date != 'Unknown':
                try:
                    # Try to format the date nicely
                    date_obj = datetime.strptime(invited_date, '%Y-%m-%d %H:%M:%S')
                    invited_date = date_obj.strftime('%Y-%m-%d')
                except:
                    pass
            
            # Add data to table
            items = [
                QTableWidgetItem(str(client_code or '')),
                QTableWidgetItem(str(client_name or '')),
                QTableWidgetItem(str(inv[2] or '')),  # friend_name
                QTableWidgetItem(str(inv[3] or '')),  # friend_phone
                QTableWidgetItem(str(invited_date)),  # invited_at
                QTableWidgetItem(self.tr('✅ Tagged') if inv[5] else self.tr('⏳ Pending'))  # tagged
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Set row height
            self.table.setRowHeight(row, 50)

    def open_add_invitation(self):
        """Open dialog to add new invitation"""
        code, ok = QInputDialog.getText(self, self.tr('Client Code'), 
                                       self.tr('Enter client code:'))
        if not ok or not code:
            return
        
        client_id = self.get_client_id_by_code(code)
        if not client_id:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr('❌ Client not found.'))
            return
        
        friend_name, ok = QInputDialog.getText(self, self.tr('Friend Name'), 
                                             self.tr('Enter friend name:'))
        if not ok or not friend_name:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Friend name is required.'))
            return
        
        friend_phone, ok = QInputDialog.getText(self, self.tr('Friend Phone'), 
                                              self.tr('Enter friend phone:'))
        if not ok or not friend_phone:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Friend phone is required.'))
            return
        
        import re
        if not re.match(r'^\d{10,15}$', friend_phone):
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Invalid phone number format.'))
            return
        
        try:
            self.controller.add_invitation(client_id, friend_name, friend_phone)
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ Invitation added successfully!'))
            self.load_invitations()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error adding invitation: {str(e)}'))

    def open_edit_dialog(self):
        """Open dialog to edit selected invitation"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select an invitation to edit.'))
            return
        
        QMessageBox.information(self, self.tr('Info'), 
                              self.tr('ℹ️ Invitation editing feature needs to be implemented in the controller.'))

    def mark_as_tagged(self):
        """Mark selected invitation as tagged"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select an invitation to mark as tagged.'))
            return
        
        client_name = self.table.item(row, 1).text()
        friend_name = self.table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, 
            self.tr('Confirm Tag'), 
            self.tr(f'Mark invitation as tagged?\n\n'
                   f'Client: {client_name}\n'
                   f'Friend: {friend_name}'), 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, self.tr('Info'), 
                                  self.tr('ℹ️ Tag marking feature needs to be implemented in the controller.'))

    def handle_delete(self):
        """Handle invitation deletion"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select an invitation to delete.'))
            return
        
        client_name = self.table.item(row, 1).text()
        friend_name = self.table.item(row, 2).text()
        friend_phone = self.table.item(row, 3).text()
        
        reply = QMessageBox.question(
            self, 
            self.tr('Confirm Delete'), 
            self.tr(f'Are you sure you want to delete this invitation?\n\n'
                   f'Client: {client_name}\n'
                   f'Friend: {friend_name}\n'
                   f'Phone: {friend_phone}\n\n'
                   f'This action cannot be undone.'), 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, self.tr('Info'), 
                                  self.tr('ℹ️ Invitation deletion feature needs to be implemented in the controller.'))

    def export_data(self):
        """Export invitation data"""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                self.tr('Export Invitations Data'),
                f'invitations_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                'CSV files (*.csv)'
            )
            
            if filename:
                invitations = self.controller.get_all()
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Write header
                    writer.writerow(['Client Code', 'Client Name', 'Friend Name', 'Friend Phone', 'Invited Date', 'Status'])
                    
                    # Write data
                    for invitation in invitations:
                        client_code = self.get_client_code_by_id(invitation[1])
                        client_name = self.get_client_name_by_id(invitation[1])
                        invited_date = invitation[4] if invitation[4] else 'Unknown'
                        status = 'Tagged' if invitation[5] else 'Pending'
                        
                        row = [
                            client_code,
                            client_name,
                            invitation[2],  # friend_name
                            invitation[3],  # friend_phone
                            invited_date,
                            status
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