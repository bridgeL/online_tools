from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import re

# readme.md
readme_path = Path("readme.md")
text = readme_path.read_text("utf8")
text = text.split("## 功能一览")[0]
text += "## 功能一览\n\n功能|标签|更新日期\n-|-|-\n"

urls_path = Path("config.json")
data = json.loads(urls_path.read_text("utf8"))

for d in data:
    labels = " ".join(d["labels"])
    if "http" in d["url"]:
        url = d["url"]
    else:
        url = f'https://bridgel.github.io/online_tools/{d["url"]}'
    text += f'[{d["name"]}]({url})|{labels}|{d["date"]}\n'

tz = timezone(timedelta(hours=8))
time_s = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
text = re.sub(r"<i>更新时间.*?</i>", f"<i>更新时间：{time_s}</i>", text)
readme_path.write_text(text, "utf8")

Path("timestamp.txt").write_text(time_s, "utf8")
