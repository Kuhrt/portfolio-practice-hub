# Database Migrations with Alembic

This project uses Alembic for database schema management, which is the modern best practice for Python applications.

## Quick Start

The application will automatically run migrations on startup, so you don't need to do anything special to get started.

## Manual Migration Commands

### Check current migration status

```bash
uv run alembic current
```

### Run migrations

```bash
uv run alembic upgrade head
```

### Create a new migration (after model changes)

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

### Rollback to previous migration

```bash
uv run alembic downgrade -1
```

### Rollback to specific migration

```bash
uv run alembic downgrade <revision_id>
```

## Migration Workflow

1. **Make changes to your SQLModel classes** in `models/`
2. **Generate migration**: `uv run alembic revision --autogenerate -m "Your description"`
3. **Review the generated migration** in `alembic/versions/`
4. **Apply migration**: `uv run alembic upgrade head`
5. **Commit both model changes and migration files** to version control

## Important Notes

- **Always review generated migrations** before applying them
- **Test migrations** on a copy of your database first
- **Never edit migration files** after they've been applied to production
- **Keep migrations in version control** - they're part of your application code
