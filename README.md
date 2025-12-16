# Weather Backend Service

A Flask backend service that fetches **time-series weather data** (temperature & humidity) from the **Open-Meteo API**, stores it in a **SQLite database**, and provides endpoints to **export the last 48 hours of data** as **Excel** and **PDF reports with charts**.

---

## Features

- Fetch and store weather data (temperature & humidity) for a fixed location.
- Store time-series data in **SQLite**.
- Export **last 48 hours** of weather data to:
  - **Excel (.xlsx)**  
  - **PDF with line chart (temperature & humidity vs time)**  
- PDF includes:
  - Title & metadata (location, date range)  
  - Line chart visualizing weather trends  
- All endpoints are **RESTful** and easy to integrate.

---

## Technologies Used

- **Backend**: Python, Flask  
- **Database**: SQLite  
- **Data Processing & Export**: Pandas, Matplotlib  
- **PDF Generation**: ReportLab  
- **HTTP Requests**: `requests` library  

---

## Project Structure
weather-backend/

           ├── app.py           # Main Flask app with endpoints
           ├── database.py       # SQLite DB helper (create table, connection)
           ├── exports/           # Folder for generated Excel & PDF files
           ├── static/            # Folder for chart images
           ├── requirements.txt    # Python dependencies
           └── README.md           # Project documentation
           
---

## Setup Instructions

1. **Clone the repository**

       git clone <repository_url>
       cd weather-backend

2. Create virtual environment

       python -m venv venv

3. Activate virtual environment
   
Windows:

           venv\Scripts\activate
Linux / Mac:

      source venv/bin/activate
4. Install dependencies

       pip install -r requirements.txt
5. Run the app

       python app.py
6. Open browser or Postman
   
Access endpoints at http://127.0.0.1:5000/

## API Endpoints
1. Fetch & Store Weather Data
   
       GET /weather-report


-  Fetches weather data for Latitude: 47.37, Longitude: 8.55

-  Stores data in SQLite weather table

-   Returns:

        {
           "message": "Weather data fetched & stored successfully"
        }

2. Export Last 48 Hours to Excel
   
       GET /export/excel


- Returns .xlsx file with columns:

      timestamp | temperature | humidity


- Only includes last 48 hours of data.

3. Export Last 48 Hours to PDF
   
       GET /export/pdf


- Generates PDF including:

  - Title & metadata (location, date range)

  -  Line chart of temperature & humidity vs time

-  Only includes last 48 hours of data

-  File is sent as download (weather.pdf).

## Notes

- Call /weather-report first before exporting Excel or PDF, otherwise the database will be empty.

- Time zone is UTC.

- Excel & PDF files are saved in the exports folder automatically.

- Chart images for PDF are stored temporarily in static folder.

## Dependencies

- Flask  
- pandas
- matplotlib
- requests
- reportlab

Install dependencies using:

    pip install Flask pandas matplotlib requests reportlab

