---
description: How to run the FastFoodie backend project
---
1. Ensure Python 3.9+ and MySQL are installed.
2. Run the startup script:
   ```bash
   ./run.sh
   ```
   - This script will:
     - Create/Activate a virtual environment.
     - Install dependencies from `requirements.txt`.
     - Check/Create `.env` file.
     - Ask to run database migrations (optional).
     - Start the FastAPI server with Uvicorn.

Alternative manual steps:
1. Activate virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations (if needed): `python migrate.py`
4. Start server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
