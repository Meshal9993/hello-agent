# Verification guide

## Intended local services

- Backend: `http://127.0.0.1:8000` — start from `backend/` with `.venv\\Scripts\\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000`.
- Frontend: `http://127.0.0.1:5173` — start from `frontend/` with `npm run dev -- --host 127.0.0.1 --port 5173`.

The Vite `/api` proxy forwards frontend calculator requests to the backend. Confirm `GET /multiply?a=7&b=6` returns `{"result": 42.0}` and `GET /divide?a=1&b=0` returns HTTP 400 with `{"detail": "Cannot divide by zero."}`.
