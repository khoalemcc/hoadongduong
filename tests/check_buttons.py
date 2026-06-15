import os
import re

views_dir = r'd:\github\hoadongduong\frontend\src\views'
for file in os.listdir(views_dir):
    if file.startswith('Admin') and file.endswith('.vue'):
        filepath = os.path.join(views_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        buttons = re.findall(r'<button[^>]*>.*?</button>', content, re.IGNORECASE | re.DOTALL)
        missing = []
        for btn in buttons:
            has_click = re.search(r'@click', btn)
            has_submit = re.search(r'type=[\'\"]submit[\'\"]', btn)
            has_disabled = re.search(r'\bdisabled\b', btn) and not has_click # if disabled, maybe it's mock
            if not has_click and not has_submit:
                # remove newlines
                btn_clean = ' '.join(btn.split())
                snippet = re.search(r'>([^<]+)</button>', btn_clean)
                if snippet and snippet.group(1).strip():
                    text = snippet.group(1).strip()
                else:
                    text_match = re.search(r'<span[^>]*>([^<]*)</span>', btn_clean)
                    text = '[Icon: ' + text_match.group(1).strip() + ']' if text_match else '[Empty/Icon]'
                missing.append(text)
        if missing:
            print(f'{file} missing clicks for:')
            for m in missing:
                print(f'  - {m}')
