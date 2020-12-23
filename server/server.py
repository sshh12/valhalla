from flask import Flask, request
import time

app = Flask(__name__)


@app.route("/")
def index():
    temp = request.args["temp"]
    hum = request.args["hum"]
    with open("temp.csv", "a") as fp:
        fp.write("{},{},{}\n".format(time.time(), temp, hum))
    return ""


if __name__ == "__main__":
    app.run("0.0.0.0", 8111, debug=False)
