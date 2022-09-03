from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open("Book_recommender_system\\popular.pkl", "rb"))
pt = pickle.load(open("Book_recommender_system\\pt.pkl", "rb"))
books = pickle.load(open("Book_recommender_system\\mybooks.pkl", "rb"))
similarity_scores = pickle.load(
    open("Book_recommender_system\\similarity_scores.pkl", "rb"))

app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello World"
    return render_template("index.html",
                           book_name=list(popular_df["Book-Title"].values),
                           Author=list(popular_df["Book-Author_y"].values),
                           Image=list(popular_df["Image-URL-M_y"].values),
                           Votes=list(popular_df["num_ratings"].values),
                           Rating=list(popular_df["avg_rating"].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
