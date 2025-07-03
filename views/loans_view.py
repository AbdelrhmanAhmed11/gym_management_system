from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy,
                             QFrame, QHeaderView, QComboBox, QInputDialog,
                             QSpacerItem, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPalette
from controllers.loans_controller import LoansController
from models.client_model import ClientModel
from datetime import datetime, timedelta

class LoansView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = LoansController()
        self.client_model = ClientModel()
        self.init_ui()
        self.apply_styles()
        self.load_loans()

    def init_ui(self):
        self.setWindowTitle(self.tr('Loans Management'))
        
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
        title_label = QLabel(self.tr('💰 Loans Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Track client loans, manage balances, and monitor financial transactions'))
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
        
        # Amount search input
        self.amount_input = QLineEdit()
        self.amount_input.setObjectName("searchInput")
        self.amount_input.setPlaceholderText(self.tr('Search by amount...'))
        self.amount_input.setFixedHeight(45)
        self.amount_input.textChanged.connect(self.on_search_text_changed)
        
        first_row.addWidget(search_icon)
        first_row.addWidget(self.client_input)
        first_row.addWidget(self.amount_input)
        
        # Second row - Filters and actions
        second_row = QHBoxLayout()
        second_row.setSpacing(20)
        
        # Amount filter
        self.amount_combo = QComboBox()
        self.amount_combo.setObjectName("filterCombo")
        self.amount_combo.setFixedHeight(45)
        self.amount_combo.setFixedWidth(150)
        self.amount_combo.addItems([
            self.tr('All Amounts'),
            self.tr('< 100'),
            self.tr('100 - 500'),
            self.tr('> 500')
        ])
        self.amount_combo.currentTextChanged.connect(self.apply_filters)
        
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
        
        second_row.addWidget(QLabel(self.tr('Amount:')))
        second_row.addWidget(self.amount_combo)
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
        
        # Get loan statistics
        stats = self.get_loan_stats()
        
        # Create stat cards
        stat_cards = [
            ('💰', self.tr('Total Loans'), str(stats['total']), '#e63946'),
            ('💵', self.tr('Total Amount'), f"${stats['total_amount']:.2f}", '#38b000'),
            ('📊', self.tr('Average Loan'), f"${stats['average']:.2f}", '#17a2b8'),
            ('📅', self.tr('This Month'), str(stats['this_month']), '#ffcc00')
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
        
        # Table title and balance
        title_layout = QHBoxLayout()
        
        table_title = QLabel(self.tr('Loan Records'))
        table_title.setObjectName("sectionTitle")
        
        self.balance_label = QLabel(self.tr('Running Balance: $0.00'))
        self.balance_label.setObjectName("balanceLabel")
        
        title_layout.addWidget(table_title)
        title_layout.addStretch()
        title_layout.addWidget(self.balance_label)
        
        # Create table
        self.table = QTableWidget(0, 6)
        self.table.setObjectName("loansTable")
        self.table.setHorizontalHeaderLabels([
            self.tr('Client Code'),
            self.tr('Client Name'), 
            self.tr('Amount'), 
            self.tr('Description'), 
            self.tr('Date'),
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
        
        table_layout.addLayout(title_layout)
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
        self.add_btn = QPushButton(self.tr('➕ Add New Loan'))
        self.add_btn.setObjectName("addButton")
        self.add_btn.setFixedHeight(45)
        self.add_btn.setFixedWidth(160)
        self.add_btn.clicked.connect(self.open_add_loan)
        
        # Payment button
        self.payment_btn = QPushButton(self.tr('💳 Record Payment'))
        self.payment_btn.setObjectName("editButton")
        self.payment_btn.setFixedHeight(45)
        self.payment_btn.setFixedWidth(160)
        self.payment_btn.clicked.connect(self.record_payment)
        
        # Delete button
        self.delete_btn = QPushButton(self.tr('🗑️ Delete Loan'))
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
        buttons_layout.addWidget(self.payment_btn)
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
            
            QLabel#balanceLabel {
                color: #38b000;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                padding: 10px 20px;
                border: 2px solid #38b000;
                border-radius: 8px;
            }
            
            /* Table Styling - DARK */
            QTableWidget#loansTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                font-size: 13px;
                selection-background-color: #e63946;
                selection-color: white;
            }
            
            QTableWidget#loansTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#loansTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QTableWidget#loansTable::item:hover {
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

    def get_loan_stats(self):
        """Get loan statistics"""
        try:
            loans = self.controller.get_all()
            total = len(loans)
            total_amount = 0
            this_month = 0
            
            current_month = datetime.now().strftime('%Y-%m')
            
            for loan in loans:
                # loan: id, client_id, amount, description, created_at
                total_amount += float(loan[2])
                
                # Check if loan is from this month
                if loan[4] and loan[4].startswith(current_month):
                    this_month += 1
            
            average = total_amount / total if total > 0 else 0
            
            return {
                'total': total,
                'total_amount': total_amount,
                'average': average,
                'this_month': this_month
            }
        except:
            return {'total': 0, 'total_amount': 0, 'average': 0, 'this_month': 0}

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
        self.load_loans()

    def apply_filters(self):
        """Apply filters to the table"""
        self.load_loans()

    def clear_filters(self):
        """Clear all filters"""
        self.client_input.clear()
        self.amount_input.clear()
        self.amount_combo.setCurrentIndex(0)
        self.load_loans()

    def load_loans(self):
        """Load loans with filters applied"""
        client_filter = self.client_input.text().strip()
        amount_filter = self.amount_input.text().strip()
        amount_range = self.amount_combo.currentText()
        
        loans = self.controller.get_all()
        filtered = []
        client_id = None
        
        for loan in loans:
            # loan: id, client_id, amount, description, created_at
            show = True
            
            if client_filter:
                client_name = self.get_client_name_by_id(loan[1])
                client_code = self.get_client_code_by_id(loan[1])
                if (client_filter.lower() not in (client_name or '').lower() and 
                    client_filter.lower() not in (client_code or '').lower()):
                    show = False
                else:
                    client_id = loan[1]
            
            if amount_filter:
                if amount_filter not in str(loan[2]):
                    show = False
            
            if amount_range != self.tr('All Amounts'):
                amount = float(loan[2])
                if amount_range == self.tr('< 100') and amount >= 100:
                    show = False
                elif amount_range == self.tr('100 - 500') and (amount < 100 or amount > 500):
                    show = False
                elif amount_range == self.tr('> 500') and amount <= 500:
                    show = False
            
            if show:
                filtered.append(loan)
        
        self.populate_table(filtered)
        
        # Show running balance if filtered by client
        if client_id:
            balance = self.controller.get_running_balance(client_id)
            self.balance_label.setText(self.tr(f'Running Balance: ${balance:.2f}'))
        else:
            self.balance_label.setText(self.tr('Running Balance: $0.00'))

    def populate_table(self, loans):
        """Populate table with loan data"""
        self.table.setRowCount(0)
        
        for loan in loans:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Get client info
            client_code = self.get_client_code_by_id(loan[1])
            client_name = self.get_client_name_by_id(loan[1])
            
            # Format date
            loan_date = loan[4] if loan[4] else 'Unknown'
            if loan_date != 'Unknown':
                try:
                    # Try to format the date nicely
                    date_obj = datetime.strptime(loan_date, '%Y-%m-%d %H:%M:%S')
                    loan_date = date_obj.strftime('%Y-%m-%d')
                except:
                    pass
            
            # Determine status based on amount
            amount = float(loan[2])
            if amount > 0:
                status = '💰 Active'
            else:
                status = '💳 Paid'
            
            # Add data to table
            items = [
                QTableWidgetItem(str(client_code or '')),
                QTableWidgetItem(str(client_name or '')),
                QTableWidgetItem(f"${loan[2]:.2f}"),  # amount
                QTableWidgetItem(str(loan[3] or '')),  # description
                QTableWidgetItem(str(loan_date)),  # created_at
                QTableWidgetItem(status)  # status
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Set row height
            self.table.setRowHeight(row, 50)

    def open_add_loan(self):
        """Open dialog to add new loan"""
        code, ok = QInputDialog.getText(self, self.tr('Client Code'), 
                                       self.tr('Enter client code:'))
        if not ok or not code:
            return
        
        client_id = self.get_client_id_by_code(code)
        if not client_id:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr('❌ Client not found.'))
            return
        
        amount, ok = QInputDialog.getDouble(self, self.tr('Loan Amount'), 
                                          self.tr('Enter amount:'), 0, 0)
        if not ok:
            return
        
        if amount <= 0:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Amount must be positive.'))
            return
        
        desc, ok = QInputDialog.getText(self, self.tr('Description'), 
                                      self.tr('Enter description:'))
        if not ok or not desc:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Description is required.'))
            return
        
        try:
            self.controller.add_loan(client_id, amount, desc)
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ Loan added successfully!'))
            self.load_loans()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error adding loan: {str(e)}'))

    def record_payment(self):
        """Record a payment for a loan"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a loan to record payment for.'))
            return
        
        client_name = self.table.item(row, 1).text()
        current_amount = self.table.item(row, 2).text().replace('$', '')
        
        payment, ok = QInputDialog.getDouble(
            self, self.tr('Record Payment'), 
            self.tr(f'Enter payment amount for {client_name}:'), 
            0, 0, float(current_amount)
        )
        if not ok:
            return
        
        if payment <= 0:
            QMessageBox.warning(self, self.tr('Error'), 
                              self.tr('⚠️ Payment amount must be positive.'))
            return
        
        QMessageBox.information(self, self.tr('Info'), 
                              self.tr('ℹ️ Payment recording feature needs to be implemented in the controller.'))

    def open_edit_dialog(self):
        """Open dialog to edit selected loan"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a loan to edit.'))
            return
        
        QMessageBox.information(self, self.tr('Info'), 
                              self.tr('ℹ️ Loan editing feature needs to be implemented in the controller.'))

    def handle_delete(self):
        """Handle loan deletion"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr('No Selection'), 
                                  self.tr('Please select a loan to delete.'))
            return
        
        client_name = self.table.item(row, 1).text()
        amount = self.table.item(row, 2).text()
        description = self.table.item(row, 3).text()
        
        reply = QMessageBox.question(
            self, 
            self.tr('Confirm Delete'), 
            self.tr(f'Are you sure you want to delete this loan?\n\n'
                   f'Client: {client_name}\n'
                   f'Amount: {amount}\n'
                   f'Description: {description}\n\n'
                   f'This action cannot be undone.'), 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, self.tr('Info'), 
                                  self.tr('ℹ️ Loan deletion feature needs to be implemented in the controller.'))

    def export_data(self):
        """Export loan data"""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                self.tr('Export Loans Data'),
                f'loans_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                'CSV files (*.csv)'
            )
            
            if filename:
                loans = self.controller.get_all()
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Write header
                    writer.writerow(['Client Code', 'Client Name', 'Amount', 'Description', 'Date', 'Status'])
                    
                    # Write data
                    for loan in loans:
                        client_code = self.get_client_code_by_id(loan[1])
                        client_name = self.get_client_name_by_id(loan[1])
                        loan_date = loan[4] if loan[4] else 'Unknown'
                        amount = float(loan[2])
                        status = 'Active' if amount > 0 else 'Paid'
                        
                        row = [
                            client_code,
                            client_name,
                            f"${loan[2]:.2f}",
                            loan[3],  # description
                            loan_date,
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
        return self.translator.translate(text)

    def retranslate_ui(self):
        if self.translator.get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        # Header
        for widget in self.findChildren(QLabel, 'pageTitle'):
            widget.setText(self.tr('💰 Loans Management'))
        for widget in self.findChildren(QLabel, 'pageSubtitle'):
            widget.setText(self.tr('Track client loans, manage balances, and monitor financial transactions'))
        # Search section
        self.client_input.setPlaceholderText(self.tr('Search by client code/name...'))
        self.amount_input.setPlaceholderText(self.tr('Search by amount...'))
        self.amount_combo.clear()
        self.amount_combo.addItems([
            self.tr('All Amounts'),
            self.tr('< 100'),
            self.tr('100 - 500'),
            self.tr('> 500')
        ])
        self.filter_btn.setText(self.tr('🔍 Filter'))
        self.clear_btn.setText(self.tr('✖ Clear'))
        for widget in self.findChildren(QLabel):
            if widget.text().replace(':','').strip() in ['Amount', 'المبلغ']:
                widget.setText(self.tr('Amount:'))
        # Stats section
        stats = self.get_loan_stats()
        stat_labels = [self.tr('Total Loans'), self.tr('Total Amount'), self.tr('Average Loan'), self.tr('This Month')]
        for i, card in enumerate(self.findChildren(QFrame, 'statCard')):
            for label in card.findChildren(QLabel):
                if label.objectName() == 'statIcon':
                    continue
                if i < len(stat_labels):
                    label.setText(f"{stat_labels[i]} ({stats[list(stats.keys())[i]] if i < 3 else stats['this_month']})")
        # Table section
        for widget in self.findChildren(QLabel, 'sectionTitle'):
            widget.setText(self.tr('Loan Records'))
        self.table.setHorizontalHeaderLabels([
            self.tr('Client Code'),
            self.tr('Client Name'),
            self.tr('Amount'),
            self.tr('Description'),
            self.tr('Date'),
            self.tr('Status')
        ])
        # Balance label
        balance_text = self.balance_label.text()
        import re
        match = re.search(r'([\d\.,]+)', balance_text)
        if match:
            value = match.group(1)
            if value == '0.00':
                self.balance_label.setText(self.tr('Running Balance: $0.00'))
            else:
                self.balance_label.setText(self.tr(f'Running Balance: ${value}'))
        else:
            self.balance_label.setText(self.tr('Running Balance: $0.00'))
        # Actions section
        for widget in self.findChildren(QLabel, 'actionsTitle'):
            widget.setText(self.tr('⚡ Quick Actions'))
        self.add_btn.setText(self.tr('➕ Add New Loan'))
        self.payment_btn.setText(self.tr('💳 Record Payment'))
        self.delete_btn.setText(self.tr('🗑️ Delete Loan'))
        self.export_btn.setText(self.tr('📊 Export Data'))
        # Reload loans to refresh display
        self.reload_data()

    def reload_data(self):
        self.load_loans()
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)