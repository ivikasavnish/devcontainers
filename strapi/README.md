# Strapi DevContainer

Drop-in development container for Strapi CMS projects.

## Features
- Node.js 20
- PostgreSQL 16
- Strapi CLI
- VS Code JS/TS extensions
- Oh-My-Zsh terminal

## Quick Start
1. Copy `.devcontainer` folder to Strapi project root
2. Open in VS Code
3. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"
4. Auto-installs and starts on port 1337

## Services
- Admin: http://localhost:1337/admin
- API: http://localhost:1337/api
- PostgreSQL: localhost:5432

## Environment (`.env`)
```env
DATABASE_CLIENT=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=strapi
DATABASE_USERNAME=strapi
DATABASE_PASSWORD=strapi
```

## Commands
```bash
npm run develop    # Dev mode with admin
npm run build      # Build admin
strapi generate    # Generate API
```
