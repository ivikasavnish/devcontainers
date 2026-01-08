# Go + React DevContainer

Drop-in development container for Go backend + React frontend projects.

## Features
- Go 1.22 (gopls, delve, air)
- Node.js 20 LTS
- PostgreSQL 16
- Redis 7
- VS Code extensions for Go & React
- Oh-My-Zsh terminal

## Quick Start
1. Copy `.devcontainer` folder to project root
2. Ensure structure: `backend/` (Go), `frontend/` (React)
3. Open in VS Code
4. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"

## Project Structure
```
project/
├── .devcontainer/
├── backend/          # Go API
│   ├── main.go
│   └── go.mod
└── frontend/         # React app
    ├── src/
    └── package.json
```

## Services
- Go API: http://localhost:8080
- React: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Commands
```bash
# Backend (Go)
cd backend
go run main.go
air                  # Hot reload
go test ./...

# Frontend (React)
cd frontend
npm run dev
npm run build
```

## Environment
```env
DATABASE_URL=postgres://postgres:postgres@db:5432/appdb?sslmode=disable
REDIS_URL=redis://redis:6379
PORT=8080
```
