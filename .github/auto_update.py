from datetime import datetime
import json
from pathlib import Path
import re

# readme.md
readme_path = Path("readme.md")
text = readme_path.read_text("utf8")
text = text.split("## 功能一览")[0]
text += "## 功能一览\n\n分类|功能|更新日期\n-|-|-\n"

urls_path = Path("configs.json")
data = json.loads(urls_path.read_text("utf8"))
data = data["urls"]

for d in data:
    text += f'{d["type"]}|[{d["name"]}](https://bridgel.github.io/online_tools/{d["url"]})|{d["date"]}\n'

time_s = datetime.now().strftime("%Y/%m/%d")
text = re.sub(r"<i>更新日期：.*?</i>", f"<i>更新日期：{time_s}</i>", text)

readme_path.write_text(text, "utf8")

# index.html
index_path = Path("index.html")
text = index_path.read_text("utf8")
text = re.sub(r"<i>更新日期：.*?</i>", f"<i>更新日期：{time_s}</i>", text)
index_path.write_text(text, "utf8")
