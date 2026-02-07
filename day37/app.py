from flask import Flask, render_template


app = Flask(__name__)

posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post."
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post."
    },
    {
        "id": 3,
        "title": "Third Post",
        "content": "This is the content of the third post."
    }
]
@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = posts[post_id-1]
    posts_to_show = [p for p in posts if p['id'] != post_id]
    return render_template('post.html', post=post, posts=posts_to_show)

if __name__ == '__main__':
    app.run(debug=True)