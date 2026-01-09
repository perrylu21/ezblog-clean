# Zeabur Deployment Guide

This guide will help you deploy the ezblog application to Zeabur with PostgreSQL database.

## Prerequisites

- A Zeabur account ([zeabur.com](https://zeabur.com))
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Deploy PostgreSQL Database

1. Log in to your Zeabur dashboard
2. Create a new project or select an existing one
3. Click **"Add Service"** → **"Template"**
4. Search for **"PostgreSQL"** and select the official PostgreSQL template
5. Click **"Deploy"** to create the PostgreSQL service
6. Wait for the deployment to complete

## Step 2: Get PostgreSQL Connection Details

After PostgreSQL is deployed:

1. Go to your PostgreSQL service in Zeabur
2. Navigate to the **"Variables"** tab
3. You'll see the following environment variables available:
   - `POSTGRES_CONNECTION_STRING` (recommended)
   - `POSTGRES_HOST`
   - `POSTGRES_PORT`
   - `POSTGRES_USERNAME`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DATABASE`

## Step 3: Deploy Backend Service

1. In your Zeabur project, click **"Add Service"** → **"Git"**
2. Connect your Git repository and select the `ezblog-clean` repository
3. Zeabur will auto-detect it as a Python application
4. Configure the service:
   - **Root Directory**: `backend` (if your backend code is in a subdirectory)
   - **Build Command**: Leave default or use `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Port**: `8000` (or use `$PORT` environment variable)

5. Go to the **"Variables"** tab and add:
   - `POSTGRES_CONNECTION_STRING`: `${POSTGRES_CONNECTION_STRING}` (reference the PostgreSQL service)
   - Or alternatively, set individual variables:
     - `POSTGRES_HOST`: `${POSTGRES_HOST}`
     - `POSTGRES_PORT`: `${POSTGRES_PORT}`
     - `POSTGRES_USERNAME`: `${POSTGRES_USERNAME}`
     - `POSTGRES_PASSWORD`: `${POSTGRES_PASSWORD}`
     - `POSTGRES_DATABASE`: `${POSTGRES_DATABASE}`

6. Click **"Deploy"** and wait for the backend to deploy

## Step 4: Deploy Frontend Service

1. In your Zeabur project, click **"Add Service"** → **"Git"** (same repository)
2. Configure the service:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview` (or use a static file server)
   - **Framework Preset**: Select "Vite" if available

3. Go to the **"Variables"** tab and add:
   - `VITE_API_BASE_URL`: Use your backend service's public URL (e.g., `https://your-backend-service.zeabur.app`)

4. Click **"Deploy"** and wait for the frontend to deploy

## Step 5: Configure CORS

After both services are deployed:

1. Go to your **Backend** service → **"Variables"** tab
2. Add or update:
   - `CORS_ORIGINS`: Set to your frontend service's public URL (e.g., `https://your-frontend-service.zeabur.app`)
   - If you have multiple origins, separate them with commas: `https://frontend1.zeabur.app,https://frontend2.zeabur.app`

## Step 6: Verify Deployment

1. Check backend health: Visit `https://your-backend-service.zeabur.app/health`
2. Check frontend: Visit your frontend service URL
3. Test creating a post through the frontend interface

## Environment Variables Reference

### Backend Service

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_CONNECTION_STRING` | Full PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `POSTGRES_HOST` | PostgreSQL host (alternative format) | `postgres.zeabur.app` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_USERNAME` | PostgreSQL username | `root` |
| `POSTGRES_PASSWORD` | PostgreSQL password | (auto-generated) |
| `POSTGRES_DATABASE` | Database name | `postgres` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `https://frontend.zeabur.app` |

### Frontend Service

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `https://backend.zeabur.app` |

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL service is running and healthy
- Verify environment variables are correctly set in the backend service
- Check that `POSTGRES_CONNECTION_STRING` or individual `POSTGRES_*` variables are properly referenced

### CORS Errors

- Verify `CORS_ORIGINS` includes your frontend URL
- Ensure URLs don't have trailing slashes
- Check browser console for specific CORS error messages

### Build Failures

- Check build logs in Zeabur dashboard
- Verify `requirements.txt` includes all dependencies
- Ensure Python version is compatible (check `runtime.txt` if present)

## Notes

- Zeabur automatically provides `$PORT` environment variable - your application should use this
- Database migrations run automatically on startup via `Base.metadata.create_all(bind=engine)`
- For production, consider using Alembic for proper database migrations instead

