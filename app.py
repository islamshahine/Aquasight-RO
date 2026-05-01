from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    Qf = float(data["feed_flow"])
    Qp = float(data["perm_flow"])
    TDSf = float(data["feed_tds"])
    TDSp = float(data["perm_tds"])
    energy = float(data["energy"])
    chem = float(data["antiscalant"])

    recovery = (Qp / Qf) * 100
    rejection = ((TDSf - TDSp) / TDSf) * 100
    sec = energy / (Qp * 24)

    return jsonify({
        "recovery": round(recovery, 2),
        "rejection": round(rejection, 2),
        "sec": round(sec, 2)
    })