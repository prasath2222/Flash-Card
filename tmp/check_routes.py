import re

with open("server.ts", "r", encoding="utf-8") as f:
    text = f.read()

for m in re.finditer(r'app\.(get|post|all)\([\'"]([^\'"]+)', text):
    print(m.group(0))
