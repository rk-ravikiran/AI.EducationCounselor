with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove lines 70-117 (orphaned legacy code)
lines = lines[:69] + lines[117:]

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
