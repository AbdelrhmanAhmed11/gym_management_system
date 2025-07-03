from PyQt5.QtCore import QTranslator, QLocale
import os

class Translator:
    def __init__(self, app):
        self.app = app
        self.translator = QTranslator()
        self.current_lang = 'en'
        self.translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
        self.set_language('en')

    def set_language(self, lang_code):
        self.current_lang = lang_code
        qm_file = os.path.join(self.translations_dir, f'{lang_code}.qm')
        self.app.removeTranslator(self.translator)
        if os.path.exists(qm_file):
            self.translator.load(qm_file)
            self.app.installTranslator(self.translator)

    def get_language(self):
        return self.current_lang
    
    def translate(self, text):
        """Translate text using the current language"""
        if self.current_lang == 'ar':
            # Simple Arabic translations - in a real app, you'd use the .qm file
            translations = {
                # Login
                'Gym Management System - Login': 'نظام إدارة الجيم - تسجيل الدخول',
                'GYM MANAGEMENT': 'إدارة الجيم',
                'Welcome Back': 'مرحباً بعودتك',
                'Username': 'اسم المستخدم',
                'Enter your username': 'أدخل اسم المستخدم',
                'Password': 'كلمة المرور',
                'Enter your password': 'أدخل كلمة المرور',
                'Role': 'الدور',
                'LOGIN': 'تسجيل الدخول',
                'Language:': 'اللغة:',
                'Admin': 'مدير',
                'Receptionist': 'استقبال',
                'Input Error': 'خطأ في الإدخال',
                'Please enter both username and password.': 'يرجى إدخال اسم المستخدم وكلمة المرور.',
                'LOGGING IN...': 'جاري تسجيل الدخول...',
                'Login Successful': 'تم تسجيل الدخول بنجاح',
                'Welcome! Login successful.': 'مرحباً! تم تسجيل الدخول بنجاح.',
                'Login Failed': 'فشل تسجيل الدخول',
                'Invalid credentials or role. Please try again.': 'بيانات غير صحيحة أو دور غير صحيح. يرجى المحاولة مرة أخرى.',
                'System Error': 'خطأ في النظام',
                'An error occurred:': 'حدث خطأ:',
                # Dashboard
                'Gym Management Dashboard': 'لوحة تحكم إدارة الجيم',
                'Dashboard Overview': 'نظرة عامة على لوحة التحكم',
                'Monitor your gym operations and performance': 'راقب عمليات وأداء الجيم الخاص بك',
                'Key Metrics': 'المؤشرات الرئيسية',
                'Frozen': 'مجمد',
                'Daily Cashier': 'الصندوق اليومي',
                'Missing Payments': 'مدفوعات مفقودة',
                'Invite Conversion': 'تحويل الدعوات',
                'Total Revenue': 'إجمالي الإيرادات',
                'Total Clients': 'إجمالي العملاء',
                'QUICK ACTIONS': 'إجراءات سريعة',
                'Clients': 'العملاء',
                'Attendance': 'الحضور',
                'Finance': 'المالية',
                'Sessions': 'الجلسات',
                'Invitations': 'الدعوات',
                'Loans': 'القروض',
                'Reports': 'التقارير',
                'User Management': 'إدارة المستخدمين',
                '← Back to Dashboard': '← العودة إلى لوحة التحكم',
                # Clients
                '👥 Clients Management': '👥 إدارة العملاء',
                'Clients Management': 'إدارة العملاء',
                'Manage gym members, subscriptions, and client information': 'إدارة أعضاء الجيم والاشتراكات ومعلومات العملاء',
                'Search by name, code, or phone number...': 'ابحث بالاسم أو الكود أو رقم الهاتف...',
                'All Clients': 'كل العملاء',
                'Active': 'نشط',
                'Expired': 'منتهي',
                'Ending Soon': 'ينتهي قريباً',
                '🔍 Search': '🔍 بحث',
                '✖ Clear': '✖ مسح',
                'Total': 'الإجمالي',
                '📊 Total Check-ins:': '📊 إجمالي الحضور:',
                # Attendance
                'Enter client code or name...': 'أدخل كود أو اسم العميل...',
                # Finance
                '💰 Total Payments:': '💰 إجمالي المدفوعات:',
                '💸 Total Expenses:': '💸 إجمالي المصروفات:',
                # Sessions
                'Search by trainer name...': 'ابحث باسم المدرب...',
                'Search by client code/name...': 'ابحث بكود/اسم العميل...',
                # Invitations
                'Search by friend name/phone...': 'ابحث باسم/هاتف الصديق...',
                # Loans
                'Running Balance: $0.00': 'الرصيد الجاري: 0.00$',
                'Running Balance: $': 'الرصيد الجاري: $',
                'Search by amount...': 'ابحث بالمبلغ...',
                # Reports
                'Export Complete': 'تم التصدير بنجاح',
                'Export Error': 'خطأ في التصدير',
                # User Management
                'Search by username or full name...': 'ابحث باسم المستخدم أو الاسم الكامل...',
                # Common/Other
                'Yes': 'نعم',
                'No': 'لا',
                'OK': 'موافق',
                'Cancel': 'إلغاء',
                'Save': 'حفظ',
                'Edit': 'تعديل',
                'Delete': 'حذف',
                'Add': 'إضافة',
                'Close': 'إغلاق',
                'Details': 'تفاصيل',
                'Name': 'الاسم',
                'Phone': 'الهاتف',
                'Code': 'الكود',
                'Amount': 'المبلغ',
                'Date': 'التاريخ',
                'Status': 'الحالة',
                'Type': 'النوع',
                'Description': 'الوصف',
                'Search': 'بحث',
                'Filter': 'تصفية',
                'Back': 'رجوع',
                'Next': 'التالي',
                'Previous': 'السابق',
                'Submit': 'إرسال',
                'Reset': 'إعادة تعيين',
                'Dashboard': 'لوحة التحكم',
                'Overview': 'نظرة عامة',
                'Metrics': 'المؤشرات',
                'Revenue': 'الإيرادات',
                'Clients List': 'قائمة العملاء',
                'Payments': 'المدفوعات',
                'Expenses': 'المصروفات',
                'Loans List': 'قائمة القروض',
                'Sessions List': 'قائمة الجلسات',
                'Invitations List': 'قائمة الدعوات',
                'Reports List': 'قائمة التقارير',
                'User List': 'قائمة المستخدمين',
                'Profile': 'الملف الشخصي',
                'Settings': 'الإعدادات',
                'Logout': 'تسجيل الخروج',
                # Clients Page Table and Actions
                'Client Directory': 'دليل العملاء',
                'End Date': 'تاريخ الانتهاء',
                'Start Date': 'تاريخ البدء',
                'Subscription': 'الاشتراك',
                'Quick Actions': 'إجراءات سريعة',
                'Export Data': 'تصدير البيانات',
                'Delete Client': 'حذف العميل',
                'Edit Client': 'تعديل العميل',
                'Add New Client': 'إضافة عميل جديد',
                'Normal': 'عادي',
                'Monthly': 'شهري',
                'Quarterly': 'ربع سنوي',
                'Yearly': 'سنوي',
                'Unknown': 'غير معروف',
                '❌ Expired': '❌ منتهي',
                '⏰ Ending Soon': '⏰ ينتهي قريباً',
                '✅ Active': '✅ نشط',
                # Attendance Page
                'Attendance Management': 'إدارة الحضور',
                '📋 Attendance Management': '📋 إدارة الحضور',
                'Track member check-ins and monitor gym attendance': 'تتبع حضور الأعضاء ومراقبة حضور الجيم',
                '📅 Select Date:': '📅 اختر التاريخ:',
                '🔍 View Attendance': '🔍 عرض الحضور',
                'Total Check-ins: 0': 'إجمالي الحضور: 0',
                'Total Check-ins:': 'إجمالي الحضور:',
                'Attendance Records': 'سجلات الحضور',
                'Client Code': 'كود العميل',
                'Member Name': 'اسم العضو',
                'Check-in Time': 'وقت الحضور',
                '✅ Quick Check-in': '✅ تسجيل حضور سريع',
                '👤 Client:': '👤 العميل:',
                '🔥 Log Check-in': '🔥 تسجيل الحضور',
                'Success': 'نجاح',
                'Error': 'خطأ',
                'No Selection': 'لا يوجد تحديد',
                'Please select a record to edit.': 'يرجى تحديد سجل للتعديل.',
                'Please select a record to delete.': 'يرجى تحديد سجل للحذف.',
                'Check-in logged successfully!': 'تم تسجيل الحضور بنجاح!',
                'Error logging check-in.': 'حدث خطأ أثناء تسجيل الحضور.',
                # Finance Page
                'Finance Management': 'إدارة المالية',
                '💰 Finance Management': '💰 إدارة المالية',
                'Track payments, expenses, and financial performance': 'تتبع المدفوعات والمصروفات والأداء المالي',
                'Alert:': 'تنبيه:',
                'unmatched or invalid payments detected!': 'مدفوعات غير متطابقة أو غير صالحة تم اكتشافها!',
                'Today\'s Revenue': 'إيرادات اليوم',
                'Monthly Revenue': 'إيرادات الشهر',
                'Today\'s Expenses': 'مصروفات اليوم',
                'Net Profit': 'صافي الربح',
                '💳 Payments': '💳 المدفوعات',
                '💸 Expenses': '💸 المصروفات',
                'Payments': 'المدفوعات',
                'Expenses': 'المصروفات',
                'Total Payments:': 'إجمالي المدفوعات:',
                'Total Expenses:': 'إجمالي المصروفات:',
                'Client Code': 'كود العميل',
                'Member Name': 'اسم العضو',
                'Amount': 'المبلغ',
                'Date': 'التاريخ',
                'Category': 'الفئة',
                'Description': 'الوصف',
                'Add Payment': 'إضافة دفعة',
                'Add Expense': 'إضافة مصروف',
                'Edit Payment': 'تعديل دفعة',
                'Edit Expense': 'تعديل مصروف',
                'Delete Payment': 'حذف دفعة',
                'Delete Expense': 'حذف مصروف',
                'Export Payments': 'تصدير المدفوعات',
                'Export Expenses': 'تصدير المصروفات',
                'Success': 'نجاح',
                'Error': 'خطأ',
                'Payment added successfully!': 'تمت إضافة الدفعة بنجاح!',
                'Expense added successfully!': 'تمت إضافة المصروف بنجاح!',
                'Payment updated successfully!': 'تم تعديل الدفعة بنجاح!',
                'Expense updated successfully!': 'تم تعديل المصروف بنجاح!',
                'Payment deleted successfully!': 'تم حذف الدفعة بنجاح!',
                'Expense deleted successfully!': 'تم حذف المصروف بنجاح!',
                'Error adding payment.': 'خطأ أثناء إضافة الدفعة.',
                'Error adding expense.': 'خطأ أثناء إضافة المصروف.',
                'Error updating payment.': 'خطأ أثناء تعديل الدفعة.',
                'Error updating expense.': 'خطأ أثناء تعديل المصروف.',
                'Error deleting payment.': 'خطأ أثناء حذف الدفعة.',
                'Error deleting expense.': 'خطأ أثناء حذف المصروف.',
                'Error loading payments.': 'خطأ أثناء تحميل المدفوعات.',
                'Error loading expenses.': 'خطأ أثناء تحميل المصروفات.',
                'View Payments': 'عرض المدفوعات',
                'Payment Actions': 'إجراءات المدفوعات',
                'Payment Records': 'سجلات المدفوعات',
                '➕ Add Payment': '➕ إضافة دفعة',
                '💳 Payment Actions': '💳 إجراءات المدفوعات',
                '🔍 View Payments': '🔍 عرض المدفوعات',
                # Sessions Page
                'Sessions Management': 'إدارة الجلسات',
                '🏋️ Sessions Management': '🏋️ إدارة الجلسات',
                'Track training sessions, manage schedules, and monitor workout activities': 'تتبع الجلسات التدريبية، إدارة الجداول، ومراقبة الأنشطة الرياضية',
                'Search by trainer name...': 'ابحث باسم المدرب...',
                'Search by client code/name...': 'ابحث بكود/اسم العميل...',
                'All Types': 'كل الأنواع',
                'Private': 'خاصة',
                'Group': 'جماعية',
                '🔍 Filter': '🔍 تصفية',
                '✖ Clear': '✖ مسح',
                'Type:': 'النوع:',
                'Date:': 'التاريخ:',
                'Total Sessions': 'إجمالي الجلسات',
                'Private Sessions': 'جلسات خاصة',
                'Group Sessions': 'جلسات جماعية',
                'Today': 'اليوم',
                'Session Records': 'سجلات الجلسات',
                'Trainer': 'المدرب',
                'Client': 'العميل',
                'Session Type': 'نوع الجلسة',
                'Session Date': 'تاريخ الجلسة',
                'Add Session': 'إضافة جلسة',
                'Edit Session': 'تعديل جلسة',
                'Delete Session': 'حذف جلسة',
                'Export Sessions': 'تصدير الجلسات',
                'Success': 'نجاح',
                'Error': 'خطأ',
                'Session added successfully!': 'تمت إضافة الجلسة بنجاح!',
                'Session updated successfully!': 'تم تعديل الجلسة بنجاح!',
                'Session deleted successfully!': 'تم حذف الجلسة بنجاح!',
                'Error adding session.': 'خطأ أثناء إضافة الجلسة.',
                'Error updating session.': 'خطأ أثناء تعديل الجلسة.',
                'Error deleting session.': 'خطأ أثناء حذف الجلسة.',
                'Error loading sessions.': 'خطأ أثناء تحميل الجلسات.',
                'Group Session': 'جلسة جماعية',
                'Client Name': 'اسم العميل',
                'Quick Actions': 'إجراءات سريعة',
                'Export Data': 'تصدير البيانات',
                'Delete Session': 'حذف الجلسة',
                'Edit Session': 'تعديل الجلسة',
                '➕ Add New Session': '➕ إضافة جلسة جديدة',
                '✏️ Edit Session': '✏️ تعديل الجلسة',
                '🗑️ Delete Session': '🗑️ حذف الجلسة',
                # Invitations Page
                'Invitations Management': 'إدارة الدعوات',
                '🎯 Invitations Management': '🎯 إدارة الدعوات',
                'Track client referrals, manage friend invitations, and monitor invitation status': 'تتبع إحالات العملاء، إدارة دعوات الأصدقاء، ومراقبة حالة الدعوة',
                'Invitation Records': 'سجلات الدعوات',
                'Client Code': 'كود العميل',
                'Client Name': 'اسم العميل',
                'Friend Name': 'اسم الصديق',
                'Friend Phone': 'هاتف الصديق',
                'Invited Date': 'تاريخ الدعوة',
                'Status': 'الحالة',
                'All Status': 'كل الحالات',
                'Tagged': 'تم الوسم',
                'Not Tagged': 'لم يتم الوسم',
                'Pending': 'قيد الانتظار',
                'This Month': 'هذا الشهر',
                'Total Invitations': 'إجمالي الدعوات',
                'Mark as Tagged': 'وضع كوسم',
                '🏷️ Mark as Tagged': '🏷️ وضع كوسم',
                'Add New Invitation': 'إضافة دعوة جديدة',
                '➕ Add New Invitation': '➕ إضافة دعوة جديدة',
                'Delete Invitation': 'حذف الدعوة',
                '🗑️ Delete Invitation': '🗑️ حذف الدعوة',
                'Export Invitations Data': 'تصدير بيانات الدعوات',
                'Export Data': 'تصدير البيانات',
                '📊 Export Data': '📊 تصدير البيانات',
                'Quick Actions': 'إجراءات سريعة',
                '⚡ Quick Actions': '⚡ إجراءات سريعة',
                'Status:': 'الحالة:',
                'Filter': 'تصفية',
                '🔍 Filter': '🔍 تصفية',
                'Clear': 'مسح',
                '✖ Clear': '✖ مسح',
                'Search by client code/name...': 'ابحث بكود/اسم العميل...',
                'Search by friend name/phone...': 'ابحث باسم/هاتف الصديق...',
                'Confirm Tag': 'تأكيد الوسم',
                'Mark invitation as tagged?': 'هل تريد وضع الدعوة كوسم؟',
                'Confirm Delete': 'تأكيد الحذف',
                'Are you sure you want to delete this invitation?': 'هل أنت متأكد أنك تريد حذف هذه الدعوة؟',
                'This action cannot be undone.': 'لا يمكن التراجع عن هذا الإجراء.',
                'No Selection': 'لا يوجد تحديد',
                'Please select an invitation to edit.': 'يرجى تحديد دعوة للتعديل.',
                'Please select an invitation to delete.': 'يرجى تحديد دعوة للحذف.',
                'Please select an invitation to mark as tagged.': 'يرجى تحديد دعوة لوضعها كوسم.',
                '✅ Invitation added successfully!': '✅ تم إضافة الدعوة بنجاح!',
                '❌ Error adding invitation:': '❌ خطأ أثناء إضافة الدعوة:',
                '❌ Client not found.': '❌ العميل غير موجود.',
                '⚠️ Friend name is required.': '⚠️ اسم الصديق مطلوب.',
                '⚠️ Friend phone is required.': '⚠️ هاتف الصديق مطلوب.',
                '⚠️ Invalid phone number format.': '⚠️ تنسيق رقم الهاتف غير صالح.',
                'Enter client code:': 'أدخل كود العميل:',
                'Enter friend name:': 'أدخل اسم الصديق:',
                'Enter friend phone:': 'أدخل هاتف الصديق:',
                'Export Complete': 'تم التصدير بنجاح',
                'Export Error': 'خطأ في التصدير',
                'Export Invitations Data': 'تصدير بيانات الدعوات',
                '✅ Data exported successfully to:': '✅ تم تصدير البيانات بنجاح إلى:',
                '❌ Error exporting data:': '❌ خطأ أثناء تصدير البيانات:',
                'Info': 'معلومات',
                'ℹ️ Invitation editing feature needs to be implemented in the controller.': 'ℹ️ ميزة تعديل الدعوة تحتاج إلى تنفيذ في وحدة التحكم.',
                'ℹ️ Tag marking feature needs to be implemented in the controller.': 'ℹ️ ميزة وضع الوسم تحتاج إلى تنفيذ في وحدة التحكم.',
                'ℹ️ Invitation deletion feature needs to be implemented in the controller.': 'ℹ️ ميزة حذف الدعوة تحتاج إلى تنفيذ في وحدة التحكم.',
                'Friend:': 'الصديق:',
                'Phone:': 'الهاتف:',
                'Client:': 'العميل:',
                'Tagged': 'تم الوسم',
                '✅ Tagged': '✅ تم الوسم',
                '⏳ Pending': '⏳ قيد الانتظار',
                'Unknown': 'غير معروف',
                # Loans Page
                'Loans Management': 'إدارة القروض',
                '💰 Loans Management': '💰 إدارة القروض',
                'Track client loans, manage balances, and monitor financial transactions': 'تتبع قروض العملاء، إدارة الأرصدة، ومراقبة المعاملات المالية',
                'Loan Records': 'سجلات القروض',
                'Client Code': 'كود العميل',
                'Client Name': 'اسم العميل',
                'Amount': 'المبلغ',
                'Description': 'الوصف',
                'Date': 'التاريخ',
                'Status': 'الحالة',
                'All Amounts': 'كل المبالغ',
                '< 100': '< 100',
                '100 - 500': '100 - 500',
                '> 500': '> 500',
                'Amount:': 'المبلغ:',
                'Total Loans': 'إجمالي القروض',
                'Total Amount': 'إجمالي المبلغ',
                'Average Loan': 'متوسط القرض',
                'This Month': 'هذا الشهر',
                'Running Balance: $0.00': 'الرصيد الجاري: 0.00$',
                'Running Balance: $': 'الرصيد الجاري: $',
                'Search by amount...': 'ابحث بالمبلغ...',
                'Loan Amount': 'مبلغ القرض',
                'Enter amount:': 'أدخل المبلغ:',
                '⚠️ Amount must be positive.': '⚠️ يجب أن يكون المبلغ موجباً.',
                '⚠️ Description is required.': '⚠️ الوصف مطلوب.',
                '✅ Loan added successfully!': '✅ تم إضافة القرض بنجاح!',
                '❌ Error adding loan:': '❌ خطأ أثناء إضافة القرض:',
                '💳 Record Payment': '💳 تسجيل دفعة',
                'Enter payment amount for': 'أدخل مبلغ الدفعة لـ',
                '⚠️ Payment amount must be positive.': '⚠️ يجب أن يكون مبلغ الدفعة موجباً.',
                'ℹ️ Payment recording feature needs to be implemented in the controller.': 'ℹ️ ميزة تسجيل الدفعة تحتاج إلى تنفيذ في وحدة التحكم.',
                '➕ Add New Loan': '➕ إضافة قرض جديد',
                '🗑️ Delete Loan': '🗑️ حذف القرض',
                '📊 Export Data': '📊 تصدير البيانات',
                '⚡ Quick Actions': '⚡ إجراءات سريعة',
                'Confirm Delete': 'تأكيد الحذف',
                'Are you sure you want to delete this loan?': 'هل أنت متأكد أنك تريد حذف هذا القرض؟',
                'Client:': 'العميل:',
                'Amount:': 'المبلغ:',
                'Description:': 'الوصف:',
                'This action cannot be undone.': 'لا يمكن التراجع عن هذا الإجراء.',
                'ℹ️ Loan editing feature needs to be implemented in the controller.': 'ℹ️ ميزة تعديل القرض تحتاج إلى تنفيذ في وحدة التحكم.',
                'ℹ️ Loan deletion feature needs to be implemented in the controller.': 'ℹ️ ميزة حذف القرض تحتاج إلى تنفيذ في وحدة التحكم.',
                'Export Loans Data': 'تصدير بيانات القروض',
                'Export Complete': 'تم التصدير بنجاح',
                'Export Error': 'خطأ في التصدير',
                '✅ Data exported successfully to:': '✅ تم تصدير البيانات بنجاح إلى:',
                '❌ Error exporting data:': '❌ خطأ أثناء تصدير البيانات:',
                'Active': 'نشط',
                'Paid': 'مدفوع',
                # Reports Page
                'Reports Management': 'إدارة التقارير',
                '📊 Reports Management': '📊 إدارة التقارير',
                'Generate comprehensive reports, track analytics, and export business insights': 'إنشاء تقارير شاملة، تتبع التحليلات، وتصدير رؤى الأعمال',
                'Report Categories': 'فئات التقارير',
                '📋 Report Categories': '📋 فئات التقارير',
                '📝 Registered Today': '📝 المسجلون اليوم',
                '💳 Paid Today': '💳 المدفوع اليوم',
                '🏃 Attended Today': '🏃 الحضور اليوم',
                '💰 Monthly Financials': '💰 المالية الشهرية',
                '⚠️ Missing Payments': '⚠️ المدفوعات المفقودة',
                'Registered Today': 'المسجلون اليوم',
                'Payments Today': 'المدفوعات اليوم',
                'Attendance Today': 'الحضور اليوم',
                'Total Reports': 'إجمالي التقارير',
                'Report': 'تقرير',
                'Code': 'الكود',
                'Name': 'الاسم',
                'Phone': 'الهاتف',
                'Subscription': 'الاشتراك',
                'Start Date': 'تاريخ البدء',
                'Amount': 'المبلغ',
                'Description': 'الوصف',
                'Check-in Time': 'وقت الحضور',
                'Category': 'الفئة',
                'User': 'المستخدم',
                'Amount Remaining': 'المبلغ المتبقي',
                'End Date': 'تاريخ الانتهاء',
                'Export PDF': 'تصدير PDF',
                '📄 Export PDF': '📄 تصدير PDF',
                'Export Excel': 'تصدير Excel',
                '📊 Export Excel': '📊 تصدير Excel',
                'Export Complete': 'تم التصدير بنجاح',
                'Export Error': 'خطأ في التصدير',
                '✅ PDF exported successfully!': '✅ تم تصدير PDF بنجاح!',
                '❌ Error exporting PDF:': '❌ خطأ أثناء تصدير PDF:',
                '✅ Excel exported successfully!': '✅ تم تصدير Excel بنجاح!',
                '❌ Error exporting Excel:': '❌ خطأ أثناء تصدير Excel:',
                # User Management Page
                'User Management': 'إدارة المستخدمين',
                '👥 User Management': '👥 إدارة المستخدمين',
                'Manage system users, roles, and access permissions': 'إدارة مستخدمي النظام، الأدوار، وصلاحيات الوصول',
                'User Directory': 'دليل المستخدمين',
                'ID': 'المعرف',
                'Username': 'اسم المستخدم',
                'Role': 'الدور',
                'Full Name': 'الاسم الكامل',
                'All Roles': 'كل الأدوار',
                'Admin': 'مدير',
                'Receptionist': 'موظف استقبال',
                'Total Users': 'إجمالي المستخدمين',
                'Administrators': 'المدراء',
                'Receptionists': 'موظفو الاستقبال',
                'Active Sessions': 'الجلسات النشطة',
                '⚡ User Actions': '⚡ إجراءات المستخدمين',
                '➕ Add User': '➕ إضافة مستخدم',
                '🗑️ Remove User': '🗑️ حذف مستخدم',
                '🔑 Change Password': '🔑 تغيير كلمة المرور',
                '🔄 Refresh': '🔄 تحديث',
                '👤 Add User': '👤 إضافة مستخدم',
                'Enter username:': 'أدخل اسم المستخدم:',
                '🔐 Set Password': '🔐 تعيين كلمة المرور',
                'Enter password:': 'أدخل كلمة المرور:',
                '👥 Select Role': '👥 اختر الدور',
                'Select user role:': 'اختر دور المستخدم:',
                '📝 Full Name': '📝 الاسم الكامل',
                'Enter full name:': 'أدخل الاسم الكامل:',
                '❌ Username already exists.': '❌ اسم المستخدم موجود بالفعل.',
                '❌ Password must be at least 6 characters.': '❌ يجب أن تتكون كلمة المرور من 6 أحرف على الأقل.',
                '✅ User added successfully!': '✅ تم إضافة المستخدم بنجاح!',
                '❌ Error adding user:': '❌ خطأ أثناء إضافة المستخدم:',
                'No Selection': 'لا يوجد تحديد',
                'Please select a user to remove.': 'يرجى تحديد مستخدم للحذف.',
                '❌ Cannot remove the main admin user.': '❌ لا يمكن حذف المستخدم الرئيسي (المدير).',
                'Confirm Delete': 'تأكيد الحذف',
                'Are you sure you want to remove user': 'هل أنت متأكد أنك تريد حذف المستخدم',
                'This action cannot be undone.': 'لا يمكن التراجع عن هذا الإجراء.',
                '✅ User removed successfully!': '✅ تم حذف المستخدم بنجاح!',
                '❌ Error removing user:': '❌ خطأ أثناء حذف المستخدم:',
                'Please select a user to change password.': 'يرجى تحديد مستخدم لتغيير كلمة المرور.',
                '🔑 Change Password for': '🔑 تغيير كلمة المرور لـ',
                'Enter new password:': 'أدخل كلمة المرور الجديدة:',
                '✅ Password changed successfully!': '✅ تم تغيير كلمة المرور بنجاح!',
                '❌ Error changing password:': '❌ خطأ أثناء تغيير كلمة المرور:',
                'Search by username or full name...': 'ابحث باسم المستخدم أو الاسم الكامل...'
            }
            return translations.get(text, text)
        return text 