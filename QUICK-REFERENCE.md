# DevContainer Quick Reference

## One-Line Setup

```bash
# Copy devcontainer to your project
cp -r ~/devcontainers/rails/.devcontainer /path/to/your/project/

# Or use the setup script
~/devcontainers/setup-devcontainer.sh rails /path/to/your/project
```

## Stack Comparison

| Stack | Languages | Database | Cache | Ports | Best For |
|-------|-----------|----------|-------|-------|----------|
| **rails** | Ruby 3.3 | PostgreSQL 16 | Redis 7 | 3000, 5432 | Full-stack Rails apps |
| **strapi** | Node.js 20 | PostgreSQL 16 | - | 1337, 5432 | Headless CMS projects |
| **go-react** | Go 1.22, Node 20 | PostgreSQL 16 | Redis 7 | 8080, 3000, 5432 | Go API + React frontend |
| **rails-react** | Ruby 3.3, Node 20 | PostgreSQL 16 | Redis 7 | 3000, 3001, 5432 | Rails API + React frontend |
| **python** | Python 3.12 | PostgreSQL 16 | Redis 7 | 8000, 5432, 6379 | FastAPI, Django, Flask |

## VS Code Extensions Included

### Rails
- Ruby LSP (Solargraph)
- RuboCop
- Endwise
- Gem Lens

### Strapi / Go-React / Rails-React
- ESLint
- Prettier
- React snippets
- Tailwind CSS

### Go (go-react)
- Go (gopls)
- Delve debugger
- Air (hot reload)
- Staticcheck

### Python
- Pylance
- Black formatter
- Ruff linter
- Auto docstring

## Common Commands

### Container Management
```bash
# Rebuild container
Cmd+Shift+P → "Dev Containers: Rebuild Container"

# Stop container
Cmd+Shift+P → "Dev Containers: Close Remote Connection"

# View logs
docker compose logs -f
```

### Database Access
```bash
# PostgreSQL
docker compose exec db psql -U postgres -d <dbname>

# Redis CLI (where available)
docker compose exec redis redis-cli
```

### Framework Commands

#### Rails
```bash
rails server
rails console
rails db:migrate
rails db:seed
bundle install
```

#### Strapi
```bash
npm run develop     # Dev mode with admin panel
npm run start       # Production mode
npm run build       # Build admin
strapi generate     # Generate API
```

#### Go
```bash
go run main.go
air                 # Hot reload (if configured)
go test ./...
go build -o app
```

#### Python
```bash
# FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Django
python manage.py runserver 0.0.0.0:8000
python manage.py migrate

# Flask
flask run --host=0.0.0.0 --port=8000

# Testing
pytest
```

#### React/Node
```bash
npm run dev
npm run build
npm test
npm install <package>
```

## Environment Variables

### Rails
```yaml
# config/database.yml
development:
  host: <%= ENV['DATABASE_HOST'] || 'localhost' %>
  database: <%= ENV['POSTGRES_DB'] %>
  username: <%= ENV['POSTGRES_USER'] %>
  password: <%= ENV['POSTGRES_PASSWORD'] %>
```

### Strapi (.env)
```env
DATABASE_CLIENT=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=strapi
DATABASE_USERNAME=strapi
DATABASE_PASSWORD=strapi
```

### Go
```go
// Use environment variables from docker-compose
dbURL := os.Getenv("DATABASE_URL")
redisURL := os.Getenv("REDIS_URL")
```

### Python
```python
import os
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
```

## Customization Tips

### Add VS Code Extensions
Edit `.devcontainer/devcontainer.json`:
```json
"customizations": {
  "vscode": {
    "extensions": [
      "your.extension-id"
    ]
  }
}
```

### Change Ports
1. Update `docker-compose.yml` service ports
2. Update `devcontainer.json` forwardPorts
3. Rebuild container

### Add Environment Variables
Edit `docker-compose.yml`:
```yaml
services:
  app:
    environment:
      - YOUR_VAR=value
```

### Install Additional Tools
Edit `Dockerfile`:
```dockerfile
RUN apt-get install -y your-package
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :3000

# Change port in docker-compose.yml and devcontainer.json
```

### Container Build Fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
Cmd+Shift+P → "Dev Containers: Rebuild Without Cache"
```

### Dependencies Won't Install
```bash
# Check your dependency files
# requirements.txt, package.json, Gemfile, go.mod

# Manually install inside container
docker compose exec app bash
pip install -r requirements.txt  # Python
bundle install                    # Rails
npm install                       # Node
go mod download                   # Go
```

### Database Connection Issues
```bash
# Verify database is running
docker compose ps

# Check connection inside container
docker compose exec app bash
psql -h db -U postgres -d <dbname>
```

## Performance Tips

1. **Use Docker volumes** (already configured) instead of bind mounts for better performance
2. **Increase Docker resources**: Docker Desktop → Settings → Resources → 4GB+ RAM
3. **Exclude large directories** from sync: Add to `.dockerignore`:
   ```
   node_modules/
   __pycache__/
   *.log
   .git/
   ```

## Security Notes

⚠️ **Development Only**: These configurations use default credentials suitable for development only.

For production:
1. Use environment-specific secrets
2. Change all default passwords
3. Enable SSL for databases
4. Use secret management tools (Vault, AWS Secrets Manager)
5. Don't commit `.env` files with real credentials

## Getting Help

- Main README: `devcontainers/README.md`
- Stack-specific docs: `devcontainers/<stack>/README.md`
- VS Code Docs: https://code.visualstudio.com/docs/devcontainers/containers
- Docker Compose: https://docs.docker.com/compose/

## License

MIT - Use freely in your projects!
