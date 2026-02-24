import feedparser
import json

feeds = {
    "Google Japan Blog": "https://japan.googleblog.com/feeds/posts/default?alt=rss",
    "Google Cloud AI": "https://cloud.google.com/blog/ja/topics/ai-machine-learning/rss",
    "note (akira_papa_ai)": "https://note.com/akira_papa_ai/rss",
    "note (#生成AI)": "https://note.com/hashtag/生成AI/rss",
    "note (#AntiGravity)": "https://note.com/hashtag/AntiGravity/rss",
    "Zenn (AI)": "https://zenn.dev/topics/ai/feed",
    "Qiita (AI)": "https://qiita.com/tags/ai/feed"
}

results = {}
for name, url in feeds.items():
    feed = feedparser.parse(url)
    if feed.entries:
        entry = feed.entries[0]
        results[name] = {
            "status": "Success",
            "title": entry.get('title')
        }
    else:
        results[name] = {"status": "No entries or failed"}

print(json.dumps(results, indent=2, ensure_ascii=False))
