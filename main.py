import requests
import time

API_KEY = "kar_live_-f7WTMjCTIFXd9gABvuPgr9ZFUaeLJ6Y2co0w3kh1oM"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

WORDS = [
    "うお",
    "どわー",
    "きちー",
    "ええて"
]

BOT_USERNAME = "cold_laugh"

seen = set()


def get_timeline():
    r = requests.get(
        "https://karotter.com/api/developer/timeline",
        headers=HEADERS,
        timeout=15
    )

    r.raise_for_status()
    return r.json()


def create_post(text):
    r = requests.post(
        "https://karotter.com/api/developer/posts",
        headers=HEADERS,
        json={
            "content": text
        },
        timeout=15
    )

    print("投稿:", r.status_code)


while True:
    try:
        data = get_timeline()

        posts = data.get("posts", [])

        for post in posts:

            post_id = post["id"]

            if post_id in seen:
                continue

            seen.add(post_id)

            username = post["author"]["username"]
            content = post.get("content", "")

            # 自分自身の投稿は無視
            if username == BOT_USERNAME:
                continue

            # 冷笑検知
            if any(word in content for word in WORDS):

                post_url = (
                    f"https://karotter.karon.jp/"
                    f"{username}/status/{post_id}"
                )

                message = (
                    "冷笑を検知しました！\n\n"
                    f"{post_url}"
                )

                create_post(message)

                print(
                    f"検知: @{username} "
                    f"({post_id})"
                )

        time.sleep(60)

    except Exception as e:
        print("エラー:", e)
        time.sleep(60)
