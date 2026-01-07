# Kaggle Automation Cron (FastAPI on Vercel)

This project automates the pushing of a Kaggle kernel using a FastAPI endpoint, designed to be deployed on Vercel as a Cron Job.

## Structure

- `api/`: Contains the FastAPI application code.
  - `v1/endpoints/`: API routes.
  - `services/`: Business logic (Kaggle interactions).
  - `core/`: Configuration.
- `data/`: Contains the notebook source and metadata template.

## Setup

1. **Install Dependencies**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your Kaggle credentials.

   ```bash
   cp .env.example .env
   ```

3. **Run Locally**:
   ```bash
   uvicorn api.main:app --reload
   ```

## Deployment to Vercel

1. **Install Vercel CLI**:

   ```bash
   npm install -g vercel
   ```

2. **Deploy**:

   ```bash
   vercel
   ```

3. **Environment Variables on Vercel**:
   Go to your Vercel project settings -> Environment Variables and add:
   - `KAGGLE_USERNAME`
   - `KAGGLE_KEY`

## Cron Job

The `vercel.json` is configured to run the cron job daily at 00:00 UTC.

- Path: `/api/v1/cron/run-kaggle`
- Schedule: `0 0 * * *`
