---
title: Todo AI Backend
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Todo AI Backend API

Phase V Todo AI Assistant Backend - FastAPI with Gemini AI integration.

## Features

- User authentication (JWT)
- Task CRUD operations
- AI-powered chat assistant (Gemini)
- Event-driven architecture support

## API Endpoints

- `GET /health` - Health check
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `POST /api/{user_id}/chat` - AI chat

## Environment Variables

Set these in your Space secrets:

- `DATABASE_URL` - PostgreSQL connection string
- `GEMINI_API_KEY` - Google Gemini API key
- `JWT_SECRET_KEY` - JWT signing secret
- `BETTER_AUTH_SECRET` - Auth secret
