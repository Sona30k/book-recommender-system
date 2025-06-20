from flask import Flask, render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           book_name=popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_rating'].to_list()
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    #index = np.where(pt.index == user_input)[0][0]
    # Step 1: Safely check if user_input exists in pt.index
    matches = np.where(pt.index == user_input)[0]
    if len(matches) == 0:
        return render_template('recommend.html', data=[], message="❌ Book not found. Please try another title.")

    index = matches[0]  # now safe to access


    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].to_list())
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].to_list())
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].to_list())

        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
