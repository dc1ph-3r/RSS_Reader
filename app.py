from flask import Flask, render_template # type: ignore
import feedparser # type: ignore

app = Flask(__name__)

# list rss feeds to read from
rss_feeds = {
    "Krebs on security":"https://krebsonsecurity.com/feeds",
    "The hacker news":"https://feeds.feedburner.com/TheHackerNews",
    "BleepingComputer":"https://www.bleepingcomputer.com/feed/",
    "Dark Reading":"https://www.darkreading.com/rss.cxml",
    "ThreatPost":"https://threatpost.com/feed/",
    "TechCrunch (All)":"https://techcrunch.com/feed/",
    "How-to-Geek":"https://howtogeek.com/feed/",
}

def get_feeds():
    all_news = {}
    for source, url in rss_feeds.items():
        parsed = feedparser.parse(url)
        all_news[source] = parsed.entries[:5] # top5 entries
    return all_news

@app.route("/")
def home():
    news = get_feeds()
    return render_template("index.html", news=news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)