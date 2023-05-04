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
    url = "https://api-takumi-static.mihoyo.com/content_v2_user/app/1963de8dc19e461c/getContentList"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referrer": "https://sr.mihoyo.com/",
        "user-agent": random.choice(user_agents)
    }
    params = {
        "iPage":str(page),
        "iPageSize":"5",
        "sLangKey":"zh-cn",
        "isPreview":"0",
        "iChanId":"256",
    }

    res = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=5,
    )
    data = res.json()["data"]["list"]
    return data

def get_post(data):
    # 时间戳
    time_s = data["dtCreateTime"]
    dt = datetime.datetime.strptime(time_s, "%Y-%m-%d %H:%M:%S")
    time_i = int(dt.timestamp())

    # pid、标题
    pid = data["iInfoId"]
    title = data["sTitle"]

    # 视频 + 封面
    content = data["sContent"]
    r = re.search(r"<video.*?src=\"(.*?)\".*?</video>", content)
    video = r.group(1)
    image = json.loads(data["sExt"])["news-poster"][0]["url"]

    post = {
        "pid": pid,
        "title": title,
        "time_s": time_s,
        "time_i": time_i,
        "video": video,
        "image": image
    }
    print(post)
    return post


def update():
    pids = get_pids(1)
    print("pids", pids)

    old_pids = []
    path = Path("games", "starrail_video", "pids.json")
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
    path = Path("games", "starrail_video", "posts.json")
    if path.exists():
        with path.open("r", encoding="utf8") as f:
            old_posts = json.load(f)

    old_posts.extend(posts)
    old_posts.sort(key=lambda x: x["time_i"], reverse=True)
    with path.open("w+", encoding="utf8") as f:
        json.dump(old_posts, f, ensure_ascii=False, indent=4)


# timestamp.txt
tz = datetime.timezone(datetime.timedelta(hours=8))
time_s = datetime.datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
Path("games", "starrail_video", "timestamp.txt").write_text(time_s, "utf8")

try:
    update()
except:
    print(traceback.format_exc())
    print("更新starrail video失败")
