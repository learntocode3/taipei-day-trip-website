from flask import *
from apiController.attraction import attractionAPI
from apiController.user import userAPI
from apiController.booking import bookingAPI
from apiController.order import orderAPI

app=Flask(__name__)
app.register_blueprint(attractionAPI)
app.register_blueprint(userAPI)
app.register_blueprint(bookingAPI)
app.register_blueprint(orderAPI)

app.secret_key="any string but secret"



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
# if __name__ == '__main__':
#     app.run(port=3000, debug=True)

# 上線
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)