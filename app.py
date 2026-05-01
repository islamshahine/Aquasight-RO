from flask import Flask, request, jsonify

app = Flask(__name__)

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
    chem_intensity = chem

    # Simple performance scoring
    score = 100

    alerts = []

    if recovery < 35:
        alerts.append("Low recovery → possible under-utilization")
        score -= 15

    if rejection < 98:
        alerts.append("Low rejection → membrane issue or fouling")
        score -= 25

    if sec > 4:
        alerts.append("High energy consumption")
        score -= 20

    if chem > 5:
        alerts.append("Possible chemical overdosing")
        score -= 10

    # Savings estimation
    energy_saving = max(0, (sec - 3.5)) * Qp * 24 * 0.1
    chem_saving = max(0, chem - 3) * 0.2
    total_savings = energy_saving + chem_saving

    return jsonify({
        "recovery": round(recovery,2),
        "rejection": round(rejection,2),
        "sec": round(sec,2),
        "score": score,
        "alerts": alerts,
        "estimated_savings": round(total_savings,2)
    })

app.run(host="0.0.0.0", port=8080)
