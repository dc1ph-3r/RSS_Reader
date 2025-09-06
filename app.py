from flask import Flask, render_template # type: ignore
import feedparser # type: ignore

app = Flask(__name__)

# list rss feeds to read from
rss_feeds = {
    "BleepingComputer":"https://www.bleepingcomputer.com/feed/",
    "TechCrunch (All)":"https://techcrunch.com/feed/",
    "How-to-Geek":"https://howtogeek.com/feed/",
    "The Register":"https://www.theregister.com/",
    "Dark Reading":"https://www.darkreading.com/",
    "Databreaches.net":"https://databreaches.net/",
}

def get_feeds():
    all_news = {}
    for source, url in rss_feeds.items():
        parsed = feedparser.parse(url)
        all_news[source] = parsed.entries[:10] # top 10 entries
    return all_news

@app.route("/")
def home():
    news = get_feeds()
    return render_template("index.html", news=news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
