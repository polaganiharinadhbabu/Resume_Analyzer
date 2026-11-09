# Resume Analyzer

## Run the API

Install the Python dependencies:

```powershell
py -m pip install fastapi uvicorn requests python-multipart pymysql
```

Set your Gemini API key in PowerShell, then start the server:

```powershell
$env:GEMINI_API_KEY = "your-api-key"
py -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to use the API. The Gemini endpoints require
`GEMINI_API_KEY` to be set in the environment.

## Run the MySQL test

Set the MySQL password and run the test:

```powershell
$env:DB_PASSWORD = "your-database-password"
py mysqlconnection_test.py
```

Do not commit API keys, database passwords, or personal documents. Uploaded
files and local environment files are excluded by `.gitignore`.
