import traceback
import json
import datetime
import random
import re
import time
import requests
from pathlib import Path


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD1.170811.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; J8110 Build/55.0.A.0.552; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"
]


def get_pids(page=1):
    url = "https://content-static.mihoyo.com/content/ysCn/getContentList"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referrer": "https://ys.mihoyo.com/",
        "user-agent": random.choice(user_agents)
    }
    params = {
        "pageSize": "10",
        "pageNum": str(page),
        "channelId": "11",
    }

    res = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=5,
    )
    data = res.json()["data"]["list"]
    return [d["id"] for d in data]


def get_post(pid):
    url = "https://content-static.mihoyo.com/content/ysCn/getContent"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referrer": "https://ys.mihoyo.com/",
        "user-agent": random.choice(user_agents)
    }
    params = {
        "contentId": str(pid),
        "around": "1",
    }
    res = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=5,
    )
    data = res.json()["data"]

    # 时间戳
    time_s = data["start_time"]
    dt = datetime.datetime.strptime(time_s, "%Y-%m-%d %H:%M:%S")
    time_i = int(dt.timestamp())

    # 视频 + 封面
    content = data["content"]
    r = re.search(r"<video(.*?)>.*?</video>", content)
    if not r:
        return
    content = r.group(1)
    params = {}
    for r in re.finditer(r"(.*?)=\"(.*?)\"", content):
        k = r.group(1).strip()
        v = r.group(2).strip()
        params[k] = v

    post = {
        "pid": pid,
        "title": data["title"],
        "time_s": time_s,
        "time_i": time_i,
        "video": params["src"],
        "image": params["poster"]
    }
    print(post)
    return post


def update():
    pids = get_pids(1)
    print("pids", pids)

    old_pids = []
    path = Path("games", "yuanshen_video", "pids.json")
    if path.exists():
        with path.open("r", encoding="utf8") as f:
            old_pids = json.load(f)

    pids = [pid for pid in pids if pid not in old_pids]
    print("new_pids", pids)

    posts = []
    for pid in pids:
        time.sleep(5)
        post = get_post(pid)
        if post:
            posts.append(post)

    old_pids.extend(pids)
    old_pids.sort(reverse=True)
    old_pids = old_pids[:20]
    with path.open("w+", encoding="utf8") as f:
        json.dump(old_pids, f, ensure_ascii=False, indent=4)

    old_posts = []
    path = Path("games", "yuanshen_video", "posts.json")
    if path.exists():
        with path.open("r", encoding="utf8") as f:
            old_posts = json.load(f)

    old_posts.extend(posts)
    old_posts.sort(key=lambda x: x["time_i"], reverse=True)
    with path.open("w+", encoding="utf8") as f:
        json.dump(old_posts, f, ensure_ascii=False, indent=4)


# index.html
tz = datetime.timezone(datetime.timedelta(hours=8))
time_s = datetime.datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
index_path = Path("games", "yuanshen_video", "index.html")
text = index_path.read_text("utf8")
text = re.sub(r"<i>更新时间.*?</i>", f"<i>更新时间：{time_s}</i>", text)
index_path.write_text(text, "utf8")

try:
    update()
except:
    print(traceback.format_exc())
    print("更新genshin video失败")
