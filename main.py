from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def get_medium_publications(url):
    """
    Input: url - your Medium RSS Feed Url eg. https://medium.com/feed/@@ming.zhong
    Output: a list of dictionaries, each dictionary representing 1 article
    """
    r = requests.get(url)
    tree = ET.fromstring(r.content)

    out = []
    for item in tree.iter("item"):
        title = item.find("title").text
        link = item.find("link").text
        desc = BeautifulSoup(item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text, "html.parser")
        imgurl = desc.find("img")["src"]
        summary = desc.find("p").text[:50]+"..."

        out.append({
            "post_title": title,
            "post_link": link,
            "imgurl": imgurl,
            "summary": summary,
        })

    return out


posts = get_medium_publications(url="https://medium.com/feed/@ming.zhong")
app = Flask(__name__)

print(posts)
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/aboutme")
def aboutme():
    return render_template("aboutme.html")


@app.route("/project")
def project():
    return render_template("project.html", all_posts=posts)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
