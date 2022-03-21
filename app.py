from flask import *
from api.attraction import attractions
from api.user import userAPI

app=Flask(__name__)
app.register_blueprint(attractions)
app.register_blueprint(userAPI)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# 開發
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)

# 上線
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=3000)