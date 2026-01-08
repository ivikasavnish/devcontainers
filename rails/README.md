# Rails DevContainer

Drop-in development container for Ruby on Rails projects.

## Features
- Ruby 3.3 with Rails & Bundler
- PostgreSQL 16
- Redis 7
- Node.js LTS & Yarn
- VS Code extensions for Rails
- Oh-My-Zsh terminal

## Quick Start
1. Copy `.devcontainer` folder to Rails project root
2. Open in VS Code
3. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"
4. Auto-installs dependencies and starts server

## Services
- Rails: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Database Config (`config/database.yml`)
```yaml
development:
  adapter: postgresql
  host: <%= ENV['DATABASE_HOST'] || 'localhost' %>
  database: <%= ENV['POSTGRES_DB'] || 'rails_dev' %>
  username: <%= ENV['POSTGRES_USER'] || 'postgres' %>
  password: <%= ENV['POSTGRES_PASSWORD'] || 'postgres' %>
```

## Commands
```bash
rails console
rails db:migrate
bundle install
yarn build
```
