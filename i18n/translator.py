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
                'An error occurred:': 'حدث خطأ:'
            }
            return translations.get(text, text)
        return text 