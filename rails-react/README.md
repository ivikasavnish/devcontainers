# Rails + React DevContainer

Drop-in development container for Rails API + React frontend projects.

## Features
- Ruby 3.3 with Rails
- Node.js 20 LTS
- PostgreSQL 16
- Redis 7
- VS Code extensions for Rails & React
- Oh-My-Zsh terminal

## Quick Start
1. Copy `.devcontainer` folder to project root
2. Ensure structure: Rails root + `frontend/` subdirectory
3. Open in VS Code
4. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"

## Project Structure
```
project/
├── .devcontainer/
├── app/              # Rails app
├── config/
├── frontend/         # React app
│   ├── src/
│   └── package.json
└── Gemfile
```

## Services
- Rails API: http://localhost:3000
- React: http://localhost:3001
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Commands
```bash
# Rails backend
rails server -p 3000
rails console
rails db:migrate

# React frontend
cd frontend
npm run dev -- --port 3001
npm run build
```

## Config
Rails API mode (`config/application.rb`):
```ruby
config.api_only = true
config.middleware.use ActionDispatch::Cookies
config.middleware.use ActionDispatch::Session::CookieStore
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'localhost:3001'
    resource '*', headers: :any, methods: [:get, :post, :patch, :put, :delete]
  end
end
```
