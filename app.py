from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

SERVICE_ACCOUNT_FILE = "credentials.json"
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPE
)

gc = gspread.authorize(credentials)
SHEET_NAME = "EarnNOBI"
worksheet = gc.open(SHEET_NAME).sheet1

@app.route('/add-data', methods=['POST'])
def add_data():
    try:
        data = request.json
        required_fields = ["Datetime", "Ticker", "Type", "Amount", "InquiryID", "UserID"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        worksheet.append_row([
            data["Datetime"],
            data["Ticker"],
            data["Type"],
            data["Amount"],
            data["InquiryID"],
            data["UserID"]
        ])

        return jsonify({"message": "Data added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)