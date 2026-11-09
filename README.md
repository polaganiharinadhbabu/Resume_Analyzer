# Resume Analyzer

## Run the API

Install the Python dependencies:

```powershell
py -m pip install fastapi uvicorn requests python-multipart pymysql python-dotenv
```

Add your secrets to the local `.env` file, then start the server:

```powershell
py -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to use the API. The Gemini endpoints require
`GEMINI_API_KEY` to be set in the environment.

## Run the MySQL test

Set `DB_PASSWORD` in the same `.env` file, then run the test:

```powershell
py mysqlconnection_test.py
```

Do not commit API keys, database passwords, or personal documents. Uploaded
files and local environment files are excluded by `.gitignore`.

## Deploy the API to Render

1. Rotate any Gemini API key that has been exposed, then open the Render
   dashboard and choose **New → Blueprint**.
2. Connect the `Resume_Analyzer` GitHub repository. Render will read
   `render.yaml` and create the web service.
3. When prompted, enter the new `GEMINI_API_KEY` in Render's environment
   variable form. Do not upload `.env` or put secrets in GitHub.
4. After the deploy succeeds, open the service URL shown by Render and append
   `/docs` to try the API.

The API service does not connect to MySQL. `mysqlconnection_test.py` is a
local-only test; its `localhost` database is not available from Render.
