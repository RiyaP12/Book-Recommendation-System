import flask
from flask import Flask, render_template, request
import pickle
import numpy as np
from flask_fontawesome import FontAwesome

dfPopular = pickle.load(open("popularbooks.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
dfBooks = pickle.load(open("dfBooks.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

app = Flask(__name__)
fa = FontAwesome(app)


@app.route("/", methods=["get"])
def index():
    lsBookTitles = list(dfBooks["book_title"].values)
    return render_template("index.html", lsBookTitles=lsBookTitles)


@app.route("/recommend", methods=["post"])
def recommend():
    pBookName = request.form.get("txtBookName")
    if len(pBookName) > 0:

        index = np.where(pt.index == pBookName)[0][0]
        similarBooks = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similarBooks:
            item = []
            dfTemp = dfBooks[dfBooks["book_title"] == pt.index[i[0]]]
            item.extend(list(dfTemp.drop_duplicates("book_title")["book_title"].values))
            item.extend(list(dfTemp.drop_duplicates("book_title")["book_author"].values))
            item.extend(list(dfTemp.drop_duplicates("book_title")["image_url_m"].values))

            data.append(item)

        # print(data)

        return render_template("index.html", data=data)

    else:
        flask.flash("Please enter Book Name")
        return render_template("index.html")


@app.route("/popular")
def popular():
    return render_template("popular.html",
                           book_title=list(dfPopular["book_title"].values),
                           book_author=list(dfPopular["book_author"].values),
                           image=list(dfPopular["image_url_m"].values)
                           )


if __name__ == "__main__":
    app.run(debug=True)
