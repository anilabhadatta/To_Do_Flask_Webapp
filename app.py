from flask import Flask, render_template, request, redirect
# from flask_login import login_required, current_user
from model import db, notes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


# @app.route("/")
# @app.route("/login/", methods=['GET','POST'])
# def auth():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if request.form.get('submit_login'):
#             print(username, password)
#         elif request.form.get('submit_signup'):
#             print(username, password)
#         if username != "" and password != "":
#             return redirect('/')
#         # login_user(user, remember=remember)
#     return render_template("login.html",auth=False)


# @app.route("/home/", methods=['POST', 'GET'])
# # @login_required
# def home():
#     if request.method == 'POST':
#         if request.form.get('submit_logout'):
#             return redirect('/')
#     # if request.method == 'GET' and request.form.get('submit_logout') is not True:

#     return render_template("home.html", auth=True)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST" and request.form.get('add'):
        if request.form.get('notes') != "":
            notesdb = notes(request.form.get('notes'))
            db.session.add(notesdb)
            db.session.commit()
    return render_template("newhome.html", notes=notes.query.all()[::-1], condition=0)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        note_to_delete = notes.query.get_or_404(id)
        db.session.delete(note_to_delete)
        db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST' and request.form.get('update'):
        return render_template("newhome.html", notes=notes.query.all()[::-1], condition=id)
    if request.method == 'POST' and request.form.get('save'):
        note_to_update = notes.query.filter_by(id=id).first()
        note_to_update.notes = request.form.get('newnote')
        db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
