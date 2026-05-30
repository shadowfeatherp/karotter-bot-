API_KEY = "kar_live_-f7WTMjCTIFXd9gABvuPgr9ZFUaeLJ6Y2co0w3kh1oM"
import requests
import time
import json
import os

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

BOT_USERNAME = "cold_laugh"

WORDS = ["うお", "どわー", "きちー", "ええて"]

DB_FILE = "detected.json"


def load_detected():
    if not os.path.exists(DB_FILE):
        return set()
    try:
        return set(json.load(open(DB_FILE, "r", encoding="utf-8")))
    except:
        return set()


def save_detected(data):
    json.dump(list(data), open(DB_FILE, "w", encoding="utf-8"))


detected = load_detected()


def follow_user(user_id):
    requests.post(
        f"https://karotter.com/api/developer/users/{user_id}/follow",
        headers=HEADERS,
        timeout=10
    )


def quote(post_id):
    requests.post(
        "https://karotter.com/api/developer/posts",
        headers=HEADERS,
        json={
            "content": "冷笑を検知しました！",
            "quotedPostId": post_id
        },
        timeout=10
    )


def get_timeline():
    r = requests.get(
        "https://karotter.com/api/developer/timeline",
        headers=HEADERS,
        timeout=10
    )
    return r.json()


while True:
    try:
        data = get_timeline()

        for post in data.get("posts", []):

            post_id = str(post["id"])
            if post_id in detected:
                continue

            username = post["author"]["username"]
            user_id = post["author"]["id"]
            content = post.get("content", "")

            if username == BOT_USERNAME:
                continue

            # フォローは状態保存しない（その場で判断）
            try:
                follow_user(user_id)
            except:
                pass

            if any(w in content for w in WORDS):

                print("検知:", username, post_id)

                quote(post["id"])

                detected.add(post_id)
                save_detected(detected)

        time.sleep(30)

    except Exception as e:
        print("エラー:", e)
        time.sleep(30)
