from pathlib import Path
from flask import Flask, render_template, Response
from flask_scss import Scss
from blog_engine.parse_markdown import JSON_Feed, Blog, MicroBlog
from blog_engine.render_post import render_post
from urllib.parse import unquote
import json
import config
import string

app = Flask(__name__)
app.config.from_object('config')


pages = JSON_Feed('content/pages')

blog = Blog('content',
            json_base='blog_feed.json',
            json_filename='blog.json',
            json_title=config.SITE_TITLE)

micro = MicroBlog('content/microblog',
             json_base='micro_feed.json',
             json_filename='micro.json',
             json_title=f'{config.SITE_TITLE} - Microblog')
feeds = {
        'pages': pages,
        'blog': blog,
        'microblog': micro,
        }
@app.route("/<feed>.json")
def generate_json_feed(feed):
    json_feed = feeds[feed].create_feed()
    return json.dumps(json_feed), 200, {'content-type':'application/json'}

@app.route("/")
def index():
    return render_template(
            'index.html',
            config=config,
            latest_posts=blog.sorted_items(2),
            latest_micropost=micro.sorted_items(3),
            )


@app.route("/<JSON_FEED>/<id>.html")
def post(JSON_FEED, id):
    metadata = feeds[JSON_FEED].json_object[(id)]
    return render_template(f'blog.html', metadata = metadata)


@app.route("/<JSON_FEED>_posts.html")
def blog_posts(JSON_FEED):
    json_object = feeds[JSON_FEED].json_object
    sorted_list = sorted(json_object,
                         key=lambda x: json_object[x]['date_published'],
                         reverse=True)

    return render_template('blog_list.html',
                           title_list= sorted_list,
                           json_object = json_object,
    )
if __name__ == '__main__':
    Scss(app, static_dir='static', asset_dir='assets')
    app.run(host='0.0.0.0', port=8000, debug=True)
