import feedparser
from flask import Flask, render_template, request
from pyspark.sql.connect.functions import array_insert

app = Flask(__name__)

RSS_FEEDS = {
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'Hacker News': 'https://news.ycombinator.com/rss',
    'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'
}

RSS_FEEDS = {"L'Equipe":"https://dwh.lequipe.fr/api/edito/rss?path=/Football/",
             "Eye Football":"https://www.eyefootball.com/football_news.xml",
             "4 4 2":"https://www.fourfourtwo.com/rss.xml",
             
}
             

@app.route('/')
def index():
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)

    articles = sorted(articles, key=lambda x: x[1].published_parsed, reverse=True)

    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    start = (page-1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]

    return render_template('index.html', articles=paginated_articles, page=page,
                           total_pages = total_articles // per_page + 1)


@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        articles = []
        for source, feed in RSS_FEEDS.items():
            parsed_feed = feedparser.parse(feed)
            entries = [(source, entry) for entry in parsed_feed.entries]
            articles.extend(entries)

        results = [article for article in articles if query.lower() in article[1].title.lower()]
    else:
        results = []

    return render_template('search_results.html', articles=results, query=query)


@app.route('/about')
def about():
    return render_template('about.html', sources=RSS_FEEDS)



if __name__ == '__main__':
    app.run(debug=True)
