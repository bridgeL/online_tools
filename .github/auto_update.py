import json
from pathlib import Path


path = Path("readme.md")
text = path.read_text("utf8")
text = text.split("## 功能一览")[0]
text += "## 功能一览\n\n分类|功能|更新日期\n-|-|-\n"

urls_path = Path("urls.json")
data = json.loads(urls_path.read_text("utf8"))

for d in data:
    text += f'{d["type"]}|[{d["name"]}](https://bridgel.github.io/online_tools/{d["url"]})|{d["date"]}\n'

path.write_text(text, "utf8")
