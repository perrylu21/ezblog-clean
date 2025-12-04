## ezblog

A simple blog editor project with a React frontend and a FastAPI backend.

### Structure

- **backend**: FastAPI application.
- **frontend**: React single-page application for the blog editor UI.

### Backend (FastAPI)

- **Install dependencies**:

```bash
cd ezblog/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- **Run the API**:
cd /Users/chao-peilu/Projects/vibe_coding/ezblog/backend
python -m uvicorn app.main:app --reload

```bash
#uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Frontend (React)

- **Install dependencies**:

```bash
cd ezblog/frontend
npm install
```

- **Run the dev server**:

```bash
npm run dev
```

The app will be available at the URL printed in your terminal (typically `http://localhost:5173` for Vite).


