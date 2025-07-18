from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def goToMain():
    return render_template("goToMain.html")

@app.route('/1/none')
def notTelegram():
    return "Error, you aren't in Telegram Mini App"


@app.route('/<int:user_id>')
@app.route('/<int:user_id>/main')
def game(user_id):
    return f"Main page, your id {user_id}" #render_template("currentPlanes.html")


@app.route('/<int:user_id>/deleted_tasks')
def deleted_tasks(user_id):
    return f"Deleted tasks page, your id {user_id}" #render_template("deletedTasks.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")