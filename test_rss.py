import feedparser
import json

feeds = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "AI News": "https://www.artificialintelligence-news.com/feed/"
}

results = {}
for name, url in feeds.items():
    feed = feedparser.parse(url)
    if feed.entries:
        entry = feed.entries[0]
        
        # Look for images
        image_url = None
        if 'media_content' in entry and len(entry.media_content) > 0:
            image_url = entry.media_content[0].get('url')
        elif 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
            image_url = entry.media_thumbnail[0].get('url')
        elif 'links' in entry:
            for link in entry.links:
                if link.get('type', '').startswith('image/'):
                    image_url = link.get('href')
                    break
        
        results[name] = {
            "title": entry.get('title'),
            "summary": entry.get('summary', '')[:100],
            "has_image": image_url is not None,
            "image_url": image_url
        }
    else:
        results[name] = "No entries found"

print(json.dumps(results, indent=2, ensure_ascii=False))
