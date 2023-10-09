import time
import json
from pathlib import Path


def update_time():
    path = Path("config.json")
    with path.open("r", encoding="utf8") as f:
        data = json.load(f)
        data["update_time"] = int(time.time()*1000)

    with path.open("w+", encoding="utf8") as f:
        json.dump(data, f)


update_time()
