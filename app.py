from flask import Flask, jsonify, send_file
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from database import create_table, get_connection
from datetime import datetime, timedelta, timezone


from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

app = Flask(__name__)
create_table()

# -----------------------------
# 1. Fetch & Store Weather Data
# -----------------------------
from datetime import datetime, timezone
import requests
from flask import jsonify

@app.route("/weather-report")
def weather_report():
    lat = 47.37
    lon = 8.55

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m"
        "&past_days=2"
        "&timezone=UTC"
    )

    response = requests.get(url, timeout=10).json()

    # Debug safety
    if "hourly" not in response:
        return jsonify({
            "error": "Failed to fetch hourly data",
            "api_response": response
        }), 400

    times = response["hourly"]["time"]
    temps = response["hourly"]["temperature_2m"]
    hums = response["hourly"]["relative_humidity_2m"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM weather")

    for t, temp, hum in zip(times, temps, hums):
        cur.execute(
            "INSERT INTO weather VALUES (?, ?, ?)",
            (t, temp, hum)
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "Weather data fetched & stored successfully"})



@app.route("/export/excel")
def export_excel():
    conn = get_connection()

    # Calculate 48 hours ago
    time_48h_ago = datetime.utcnow() - timedelta(hours=48)

    # Read last 48 hours of data
    query = """
        SELECT * FROM weather
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """
    df = pd.read_sql(query, conn, params=(time_48h_ago.isoformat(),))
    conn.close()

    if df.empty:
        return "No data available for the last 48 hours.", 400

    # Save to Excel
    os.makedirs("exports", exist_ok=True)
    file_path = "exports/weather.xlsx"
    df.to_excel(file_path, index=False)

    # Send as download
    return send_file(file_path, as_attachment=True)



@app.route("/export/pdf")
def export_pdf():
    # Connect to DB and get last 48 hours
    conn = get_connection()
    time_48h_ago = datetime.utcnow() - timedelta(hours=48)
    query = """
        SELECT * FROM weather
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """
    df = pd.read_sql(query, conn, params=(time_48h_ago.isoformat(),))
    conn.close()

    if df.empty:
        return "No data available for the last 48 hours.", 400

    # Create chart
    plt.figure(figsize=(8, 4))
    plt.plot(pd.to_datetime(df["timestamp"]), df["temperature"], label="Temperature (°C)")
    plt.plot(pd.to_datetime(df["timestamp"]), df["humidity"], label="Humidity (%)")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.title("Temperature & Humidity (Last 48 Hours)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save chart image
    os.makedirs("static", exist_ok=True)
    chart_path = "static/weather_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Create PDF
    os.makedirs("exports", exist_ok=True)
    pdf_path = "exports/weather.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title & Metadata
    elements.append(Paragraph("<b>Weather Report</b>", styles["Title"]))
    elements.append(Paragraph("Location: Latitude 47.37, Longitude 8.55", styles["Normal"]))
    elements.append(Paragraph(f"Date Range: Last 48 Hours ({time_48h_ago.strftime('%Y-%m-%d %H:%M')} UTC - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC)", styles["Normal"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    # Add Chart
    elements.append(Image(chart_path, width=6*inch, height=3*inch))

    # Build PDF
    doc.build(elements)

    # Return PDF file
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

  