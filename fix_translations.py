import os
import re

def fix_tr_methods():
    views_dir = 'views'
    
    for filename in os.listdir(views_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(views_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the tr method implementation
            old_pattern = r'def tr\(self, text\):\s*\n\s*# Placeholder for translation - implement with your translator\s*\n\s*return text'
            new_implementation = '''def tr(self, text):
        # Use the translator if available
        if hasattr(self, 'translator') and self.translator:
            return self.translator.translate(text)
        return text'''
            
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_implementation, content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Fixed {filename}")

if __name__ == "__main__":
    fix_tr_methods()
    print("Translation methods fixed!") 