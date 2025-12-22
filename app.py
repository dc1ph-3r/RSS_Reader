import os
from flask import Flask, render_template, jsonify # type: ignore
from flask import send_from_directory # type: ignore
from datetime import datetime, timezone
import feedparser # type: ignore

app = Flask(__name__)

# list rss feeds to read from
feed_url = {
    "BleepingComputer":"https://www.bleepingcomputer.com/feed/",
    "TechCrunch (All)":"https://techcrunch.com/feed/",
    "How-to-Geek":"https://howtogeek.com/feed/",
    "This Week In 4n6":"https://thisweekin4n6.com/feed/atom",
    "Reddit RSS":"https://www.reddit.com/r/cybersecurity/.rss",
    "CVEfeed.io":"https://cvefeed.io/rssfeed/latest.xml"
} 

def fetch_all_articles(feed_url):
    all_articles = []
    for url in feed_url.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = None
            if hasattr(entry, "published_parsed"):
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            all_articles.append({
                "feed_title": name,
                "title": entry.title,
                "link": entry.link,
                "published": published.isoformat() if published else None
            })
    return all_articles

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/dashboard")
def api_dashboard():
    # dashboard logic here
    articles = fetch_all_articles()
    articles.sort(key=lambda x: x["published"] or "", reverse=True)
    return jsonify(articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
