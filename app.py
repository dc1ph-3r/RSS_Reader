from flask import Flask, render_template # type: ignore
import feedparser # type: ignore

app = Flask(__name__)

# list rss feeds to read from
rss_feeds = {
    "BleepingComputer":"https://www.bleepingcomputer.com/feed/",
    "TechCrunch (All)":"https://techcrunch.com/feed/",
    "How-to-Geek":"https://howtogeek.com/feed/",
    "This Week In 4n6":"https://thisweekin4n6.com/feed/atom",
    "Reddit RSS":"https://www.reddit.com/r/cybersecurity/.rss",
    "CVEfeed.io":"https://cvefeed.io/rssfeed/latest.xml"
} 


def get_feeds():
    all_news = {}
    for source, url in rss_feeds.items():
        parsed = feedparser.parse(url)
        if parsed.entries:
            all_news[source] = parsed.entries[:5] # top 5 entries for each site
        else:
            all_news[source] = []
    return all_news

@app.route("/")
def home():
    news = get_feeds()
    return render_template("index.html", news=news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
