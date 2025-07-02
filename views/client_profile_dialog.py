from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QDateEdit, QSpinBox, QFileDialog, 
                             QTextEdit, QMessageBox, QFrame, QScrollArea, QWidget,
                             QGridLayout, QSizePolicy)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QPixmap
import re

class ClientProfileDialog(QDialog):
    def __init__(self, translator, client=None):
        super().__init__()
        self.translator = translator
        self.client = client
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.setWindowTitle(self.tr('👤 Client Profile'))
        self.setFixedSize(800, 900)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header section
        header_section = self.create_header_section()
        main_layout.addWidget(header_section)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setObjectName("scrollArea")
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(25)
        
        # Profile picture section
        profile_section = self.create_profile_section()
        content_layout.addWidget(profile_section)
        
        # Basic information section
        basic_info_section = self.create_basic_info_section()
        content_layout.addWidget(basic_info_section)
        
        # Subscription details section
        subscription_section = self.create_subscription_section()
        content_layout.addWidget(subscription_section)
        
        # Payment information section
        payment_section = self.create_payment_section()
        content_layout.addWidget(payment_section)
        
        # Additional details section
        additional_section = self.create_additional_section()
        content_layout.addWidget(additional_section)
        
        # Guardian information section
        guardian_section = self.create_guardian_section()
        content_layout.addWidget(guardian_section)
        
        # Training details section
        training_section = self.create_training_section()
        content_layout.addWidget(training_section)
        
        # Invites section
        invites_section = self.create_invites_section()
        content_layout.addWidget(invites_section)
        
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Action buttons section
        actions_section = self.create_actions_section()
        main_layout.addWidget(actions_section)
        
        self.setLayout(main_layout)
        self.toggle_guardian_fields()

    def create_header_section(self):
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(80)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel("👤")
        icon_label.setObjectName("headerIcon")
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Title and subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        title_label = QLabel(self.tr('Client Profile'))
        title_label.setObjectName("headerTitle")
        
        subtitle_label = QLabel(self.tr('Complete client information and subscription details'))
        subtitle_label.setObjectName("headerSubtitle")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)
        text_layout.addStretch()
        
        header_layout.addWidget(icon_label)
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_profile_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('📷 Profile Picture'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Profile picture controls
        pic_layout = QHBoxLayout()
        pic_layout.setSpacing(15)
        
        self.pic_label = QLabel(self.tr('Image Path:'))
        self.pic_label.setObjectName("fieldLabel")
        
        self.pic_path = QLineEdit()
        self.pic_path.setObjectName("inputField")
        self.pic_path.setPlaceholderText(self.tr('Select profile picture...'))
        
        self.pic_btn = QPushButton(self.tr('📁 Browse'))
        self.pic_btn.setObjectName("browseButton")
        self.pic_btn.setFixedWidth(120)
        self.pic_btn.clicked.connect(self.browse_picture)
        
        pic_layout.addWidget(self.pic_label, 0)
        pic_layout.addWidget(self.pic_path, 1)
        pic_layout.addWidget(self.pic_btn, 0)
        
        layout.addLayout(pic_layout)
        section_frame.setLayout(layout)
        
        return section_frame

    def create_basic_info_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('📝 Basic Information'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Grid layout for fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Name field
        name_label = QLabel(self.tr('Full Name:'))
        name_label.setObjectName("fieldLabel")
        self.name_input = QLineEdit()
        self.name_input.setObjectName("inputField")
        self.name_input.setPlaceholderText(self.tr('Enter client full name...'))
        grid_layout.addWidget(name_label, 0, 0)
        grid_layout.addWidget(self.name_input, 0, 1)
        
        # Phone field
        phone_label = QLabel(self.tr('Phone Number:'))
        phone_label.setObjectName("fieldLabel")
        self.phone_input = QLineEdit()
        self.phone_input.setObjectName("inputField")
        self.phone_input.setPlaceholderText(self.tr('Enter phone number...'))
        grid_layout.addWidget(phone_label, 1, 0)
        grid_layout.addWidget(self.phone_input, 1, 1)
        
        # Client code field
        code_label = QLabel(self.tr('Client Code:'))
        code_label.setObjectName("fieldLabel")
        self.code_input = QLineEdit()
        self.code_input.setObjectName("inputFieldReadonly")
        self.code_input.setReadOnly(True)
        self.code_input.setPlaceholderText(self.tr('Auto-generated code...'))
        grid_layout.addWidget(code_label, 2, 0)
        grid_layout.addWidget(self.code_input, 2, 1)
        
        layout.addLayout(grid_layout)
        section_frame.setLayout(layout)
        
        return section_frame

    def create_subscription_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('🎯 Subscription Details'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Grid layout for fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Subscription type
        sub_type_label = QLabel(self.tr('Subscription Type:'))
        sub_type_label.setObjectName("fieldLabel")
        self.sub_type_combo = QComboBox()
        self.sub_type_combo.setObjectName("comboField")
        self.sub_type_combo.addItems([
            self.tr('Normal'), self.tr('Private'), self.tr('Under 15'), self.tr('Box')
        ])
        self.sub_type_combo.currentIndexChanged.connect(self.toggle_guardian_fields)
        grid_layout.addWidget(sub_type_label, 0, 0)
        grid_layout.addWidget(self.sub_type_combo, 0, 1)
        
        # Duration
        duration_label = QLabel(self.tr('Duration (months):'))
        duration_label.setObjectName("fieldLabel")
        self.duration_spin = QSpinBox()
        self.duration_spin.setObjectName("spinField")
        self.duration_spin.setRange(1, 24)
        self.duration_spin.setValue(1)
        grid_layout.addWidget(duration_label, 1, 0)
        grid_layout.addWidget(self.duration_spin, 1, 1)
        
        # Start date
        start_label = QLabel(self.tr('Start Date:'))
        start_label.setObjectName("fieldLabel")
        self.start_date = QDateEdit(QDate.currentDate())
        self.start_date.setObjectName("dateField")
        self.start_date.setCalendarPopup(True)
        grid_layout.addWidget(start_label, 2, 0)
        grid_layout.addWidget(self.start_date, 2, 1)
        
        # End date
        end_label = QLabel(self.tr('End Date:'))
        end_label.setObjectName("fieldLabel")
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setObjectName("dateField")
        self.end_date.setCalendarPopup(True)
        grid_layout.addWidget(end_label, 3, 0)
        grid_layout.addWidget(self.end_date, 3, 1)
        
        layout.addLayout(grid_layout)
        section_frame.setLayout(layout)
        
        return section_frame

    def create_payment_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('💰 Payment Information'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Grid layout for fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Amount paid
        paid_label = QLabel(self.tr('Amount Paid:'))
        paid_label.setObjectName("fieldLabel")
        self.paid_input = QLineEdit()
        self.paid_input.setObjectName("inputField")
        self.paid_input.setPlaceholderText(self.tr('Enter amount paid...'))
        grid_layout.addWidget(paid_label, 0, 0)
        grid_layout.addWidget(self.paid_input, 0, 1)
        
        # Amount remaining
        remaining_label = QLabel(self.tr('Amount Remaining:'))
        remaining_label.setObjectName("fieldLabel")
        self.remaining_input = QLineEdit()
        self.remaining_input.setObjectName("inputField")
        self.remaining_input.setPlaceholderText(self.tr('Enter remaining amount...'))
        grid_layout.addWidget(remaining_label, 1, 0)
        grid_layout.addWidget(self.remaining_input, 1, 1)
        
        layout.addLayout(grid_layout)
        section_frame.setLayout(layout)
        
        return section_frame

    def create_additional_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('⚙️ Additional Details'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Grid layout for fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Rotation
        rotation_label = QLabel(self.tr('Rotation:'))
        rotation_label.setObjectName("fieldLabel")
        self.rotation_input = QLineEdit()
        self.rotation_input.setObjectName("inputField")
        self.rotation_input.setPlaceholderText(self.tr('Enter rotation details...'))
        grid_layout.addWidget(rotation_label, 0, 0)
        grid_layout.addWidget(self.rotation_input, 0, 1)
        
        # Freeze days
        freeze_label = QLabel(self.tr('Freeze Days:'))
        freeze_label.setObjectName("fieldLabel")
        self.freeze_spin = QSpinBox()
        self.freeze_spin.setObjectName("spinField")
        self.freeze_spin.setRange(0, 60)
        self.freeze_spin.setValue(0)
        grid_layout.addWidget(freeze_label, 1, 0)
        grid_layout.addWidget(self.freeze_spin, 1, 1)
        
        layout.addLayout(grid_layout)
        section_frame.setLayout(layout)
        
        return section_frame

    def create_guardian_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('👨‍👩‍👧‍👦 Guardian Information'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Note
        note_label = QLabel(self.tr('Required for clients under 15 years old'))
        note_label.setObjectName("noteLabel")
        layout.addWidget(note_label)
        
        # Grid layout for fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Guardian name
        guardian_name_label = QLabel(self.tr('Guardian Name:'))
        guardian_name_label.setObjectName("fieldLabel")
        self.guardian_name = QLineEdit()
        self.guardian_name.setObjectName("inputField")
        self.guardian_name.setPlaceholderText(self.tr('Enter guardian full name...'))
        grid_layout.addWidget(guardian_name_label, 0, 0)
        grid_layout.addWidget(self.guardian_name, 0, 1)
        
        # Guardian phone
        guardian_phone_label = QLabel(self.tr('Guardian Phone:'))
        guardian_phone_label.setObjectName("fieldLabel")
        self.guardian_phone = QLineEdit()
        self.guardian_phone.setObjectName("inputField")
        self.guardian_phone.setPlaceholderText(self.tr('Enter guardian phone number...'))
        grid_layout.addWidget(guardian_phone_label, 1, 0)
        grid_layout.addWidget(self.guardian_phone, 1, 1)
        
        layout.addLayout(grid_layout)
        section_frame.setLayout(layout)
        
        return section_frame

    def create_training_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('🏋️ Training Details'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Trainer name
        trainer_label = QLabel(self.tr('Trainer Name:'))
        trainer_label.setObjectName("fieldLabel")
        self.trainer_input = QLineEdit()
        self.trainer_input.setObjectName("inputField")
        self.trainer_input.setPlaceholderText(self.tr('Enter assigned trainer name...'))
        layout.addWidget(trainer_label)
        layout.addWidget(self.trainer_input)
        
        # Attendance schedule
        schedule_label = QLabel(self.tr('Attendance Schedule:'))
        schedule_label.setObjectName("fieldLabel")
        self.attendance_sched = QTextEdit()
        self.attendance_sched.setObjectName("textField")
        self.attendance_sched.setPlaceholderText(self.tr('Enter training schedule and attendance notes...'))
        self.attendance_sched.setMaximumHeight(100)
        layout.addWidget(schedule_label)
        layout.addWidget(self.attendance_sched)
        
        section_frame.setLayout(layout)
        
        return section_frame

    def create_invites_section(self):
        section_frame = QFrame()
        section_frame.setObjectName("sectionFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section title
        title_label = QLabel(self.tr('📧 Client Invites'))
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Instructions
        instructions_label = QLabel(self.tr('Enter invite information (name/phone, one per line):'))
        instructions_label.setObjectName("fieldLabel")
        layout.addWidget(instructions_label)
        
        # Invites text area
        self.invites_input = QTextEdit()
        self.invites_input.setObjectName("textField")
        self.invites_input.setPlaceholderText(self.tr('Example:\nJohn Doe / 1234567890\nJane Smith / 0987654321'))
        self.invites_input.setMaximumHeight(120)
        layout.addWidget(self.invites_input)
        
        section_frame.setLayout(layout)
        
        return section_frame

    def create_actions_section(self):
        actions_frame = QFrame()
        actions_frame.setObjectName("actionsFrame")
        actions_frame.setFixedHeight(80)
        
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(30, 20, 30, 20)
        actions_layout.setSpacing(15)
        
        # Cancel button
        self.cancel_btn = QPushButton(self.tr('✖ Cancel'))
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.setFixedHeight(45)
        self.cancel_btn.setFixedWidth(120)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Save button
        self.save_btn = QPushButton(self.tr('💾 Save Client'))
        self.save_btn.setObjectName("saveButton")
        self.save_btn.setFixedHeight(45)
        self.save_btn.setFixedWidth(150)
        self.save_btn.clicked.connect(self.validate_and_accept)
        
        actions_layout.addStretch()
        actions_layout.addWidget(self.cancel_btn)
        actions_layout.addWidget(self.save_btn)
        
        actions_frame.setLayout(actions_layout)
        
        return actions_frame

    def apply_styles(self):
        style_sheet = """
            /* Main Dialog */
            QDialog {
                background-color: #2c2c2c;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Header Frame */
            QFrame#headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                border: none;
                border-bottom: 3px solid #a00e1c;
            }
            
            QLabel#headerIcon {
                font-size: 24px;
                color: white;
                background: transparent;
            }
            
            QLabel#headerTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                background: transparent;
            }
            
            QLabel#headerSubtitle {
                color: #f0f0f0;
                font-size: 14px;
                font-weight: 400;
                background: transparent;
            }
            
            /* Scroll Area */
            QScrollArea#scrollArea {
                background-color: #2c2c2c;
                border: none;
            }
            
            QScrollArea#scrollArea QWidget {
                background-color: #2c2c2c;
            }
            
            /* Section Frames */
            QFrame#sectionFrame {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 12px;
                margin: 5px 0px;
            }
            
            QFrame#sectionFrame:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            /* Section Titles */
            QLabel#sectionTitle {
                color: #e63946;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                padding: 5px 0px;
                border-bottom: 2px solid #e63946;
                margin-bottom: 10px;
            }
            
            /* Field Labels */
            QLabel#fieldLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 600;
                background: transparent;
                min-width: 140px;
            }
            
            QLabel#noteLabel {
                color: #cccccc;
                font-size: 12px;
                font-style: italic;
                background: transparent;
                margin-bottom: 10px;
            }
            
            /* Input Fields */
            QLineEdit#inputField {
                background-color: #505050;
                border: 2px solid #606060;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
                min-height: 20px;
            }
            
            QLineEdit#inputField:focus {
                border-color: #e63946;
                background-color: #5a5a5a;
            }
            
            QLineEdit#inputField::placeholder {
                color: #999999;
            }
            
            QLineEdit#inputFieldReadonly {
                background-color: #3a3a3a;
                border: 2px solid #505050;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #cccccc;
                min-height: 20px;
            }
            
            /* Combo Boxes */
            QComboBox#comboField {
                background-color: #505050;
                border: 2px solid #606060;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
                min-height: 20px;
            }
            
            QComboBox#comboField:hover {
                border-color: #e63946;
                background-color: #5a5a5a;
            }
            
            QComboBox#comboField::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox#comboField::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #ffffff;
                margin-right: 5px;
            }
            
            QComboBox#comboField QAbstractItemView {
                background-color: #505050;
                border: 2px solid #e63946;
                border-radius: 8px;
                selection-background-color: #e63946;
                color: #ffffff;
                padding: 5px;
            }
            
            /* Spin Boxes */
            QSpinBox#spinField {
                background-color: #505050;
                border: 2px solid #606060;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
                min-height: 20px;
            }
            
            QSpinBox#spinField:focus {
                border-color: #e63946;
                background-color: #5a5a5a;
            }
            
            QSpinBox#spinField::up-button, QSpinBox#spinField::down-button {
                background-color: #e63946;
                border: none;
                border-radius: 4px;
                width: 20px;
                margin: 2px;
            }
            
            QSpinBox#spinField::up-button:hover, QSpinBox#spinField::down-button:hover {
                background-color: #ff6b6b;
            }
            
            QSpinBox#spinField::up-arrow, QSpinBox#spinField::down-arrow {
                width: 8px;
                height: 8px;
            }
            
            /* Date Edit */
            QDateEdit#dateField {
                background-color: #505050;
                border: 2px solid #606060;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
                min-height: 20px;
            }
            
            QDateEdit#dateField:focus {
                border-color: #e63946;
                background-color: #5a5a5a;
            }
            
            QDateEdit#dateField::drop-down {
                background-color: #e63946;
                border: none;
                border-radius: 4px;
                width: 25px;
                margin: 2px;
            }
            
            QDateEdit#dateField::drop-down:hover {
                background-color: #ff6b6b;
            }
            
            /* Text Edit */
            QTextEdit#textField {
                background-color: #505050;
                border: 2px solid #606060;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #ffffff;
            }
            
            QTextEdit#textField:focus {
                border-color: #e63946;
                background-color: #5a5a5a;
            }
            
            /* Browse Button */
            QPushButton#browseButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #0f7b8a);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 20px;
            }
            
            QPushButton#browseButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a9c4, stop:1 #17a2b8);
            }
            
            /* Actions Frame */
            QFrame#actionsFrame {
                background-color: #2c2c2c;
                border: none;
                border-top: 3px solid #e63946;
            }
            
            /* Action Buttons */
            QPushButton#saveButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38b000, stop:1 #2d8000);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 20px;
            }
            
            QPushButton#saveButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ade80, stop:1 #38b000);
            }
            
            QPushButton#cancelButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 20px;
            }
            
            QPushButton#cancelButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #343a40);
            }
            
            /* Scrollbars */
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
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Message Boxes */
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

    def browse_picture(self):
        file, _ = QFileDialog.getOpenFileName(
            self, 
            self.tr('Select Profile Picture'), 
            '', 
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        if file:
            self.pic_path.setText(file)

    def toggle_guardian_fields(self):
        is_under_15 = self.sub_type_combo.currentText() == self.tr('Under 15')
        self.guardian_name.setEnabled(is_under_15)
        self.guardian_phone.setEnabled(is_under_15)
        
        # Visual indication
        if is_under_15:
            self.guardian_name.setStyleSheet(self.guardian_name.styleSheet() + "border-color: #ffcc00;")
            self.guardian_phone.setStyleSheet(self.guardian_phone.styleSheet() + "border-color: #ffcc00;")
        else:
            self.guardian_name.setStyleSheet("")
            self.guardian_phone.setStyleSheet("")

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        sub_type = self.sub_type_combo.currentText()
        start = self.start_date.date()
        end = self.end_date.date()
        paid = self.paid_input.text().strip()
        remaining = self.remaining_input.text().strip()
        guardian_name = self.guardian_name.text().strip()
        guardian_phone = self.guardian_phone.text().strip()
        
        # Required fields validation
        if not name or not phone or not paid or not remaining:
            QMessageBox.warning(
                self, 
                self.tr('❌ Validation Error'), 
                self.tr('Please fill all required fields:\n• Full Name\n• Phone Number\n• Amount Paid\n• Amount Remaining')
            )
            return
        
        # Phone format validation
        if not re.match(r'^\d{10,15}$', phone):
            QMessageBox.warning(
                self, 
                self.tr('❌ Invalid Phone'), 
                self.tr('Phone number must be 10-15 digits only.')
            )
            return
        
        # Date validation
        if end <= start:
            QMessageBox.warning(
                self, 
                self.tr('❌ Invalid Dates'), 
                self.tr('End date must be after start date.')
            )
            return
        
        # Payment validation
        try:
            paid_val = float(paid)
            remaining_val = float(remaining)
            if paid_val < 0 or remaining_val < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self, 
                self.tr('❌ Invalid Payment'), 
                self.tr('Paid and remaining amounts must be non-negative numbers.')
            )
            return
        
        # Guardian validation for Under 15
        if sub_type == self.tr('Under 15'):
            if not guardian_name or not guardian_phone:
                QMessageBox.warning(
                    self, 
                    self.tr('❌ Guardian Required'), 
                    self.tr('Guardian name and phone are required for clients under 15 years old.')
                )
                return
            if not re.match(r'^\d{10,15}$', guardian_phone):
                QMessageBox.warning(
                    self, 
                    self.tr('❌ Invalid Guardian Phone'), 
                    self.tr('Guardian phone number must be 10-15 digits only.')
                )
                return
        
        # Success message
        QMessageBox.information(
            self, 
            self.tr('✅ Validation Successful'), 
            self.tr('All information is valid. Client profile will be saved.')
        )
        
        self.accept()

    def tr(self, text):
        """Translation method placeholder"""
        return text