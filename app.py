from flask import Flask, render_template, request
import sqlCommands as sqlCom
import taskHtmlBlock
import datetime

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
    with open("templates/currentPlanes.html", "r", encoding="utf-8") as file:
        html = file.read().split("&")
        htmlCenterData = taskHtmlBlock.open(sqlCom.open_user_tasks(user_id))

        retStr = None

        if len(htmlCenterData) == 0:
            retStr = html[0] + "\n<div id='h3'><h3>Нет записей</h3></div>" + html[1]
        else:
            retStr = html[0] + htmlCenterData + html[1]
    return retStr #render_template("currentPlanes.html")


@app.route('/<int:user_id>/deleted_tasks')
def deleted_tasks(user_id):
    return f"Deleted tasks page, your id {user_id}" #render_template("deletedTasks.html")

@app.route("/<int:user_id>/sumbit", methods=["POST"])
def sumbit(user_id):
    text = request.form['text']
    time = request.form['time']
    date = request.form['date']
    now = datetime.datetime.now()
    when_publ_time = now.strftime("%H:%M:%S")
    when_publ_date = now.strftime("%Y-%m-%d")
    when_edit_time = None
    when_edit_date = None
    print(user_id, text, time, date, when_publ_time, when_publ_date, when_edit_time, when_edit_date)
    return render_template("goToMain.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")