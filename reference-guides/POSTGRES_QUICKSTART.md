# PostgreSQL Quickstart Guide

**Get up and running with PostgreSQL + pgvector in 5 minutes!**

This guide is for developers who want to use the high-performance PostgreSQL backend locally (without Docker).

---

## Why PostgreSQL?

- ✅ **10-100x faster** than SQLite for semantic search
- ✅ Scales to **millions of documents**
- ✅ Native vector similarity search with **pgvector**
- ✅ HNSW indexing for **logarithmic query time**

---

## Quick Setup (macOS/Linux)

### Step 1: Install PostgreSQL

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Run Setup Script

```bash
cd /path/to/ai-news-extractor
./scripts/embedding/setup_local_postgres.sh
```

**That's it!** The script will:
- ✅ Install pgvector extension
- ✅ Create the database
- ✅ Initialize the schema
- ✅ Configure your .env file
- ✅ Offer to migrate existing SQLite data

### Step 3: Verify Setup

```bash
# Test connection
python scripts/embedding/embedding_db_pg.py --test-connection

# Check stats
python scripts/embedding/embedding_db_pg.py --stats
```

---

## Manual Setup (If Script Fails)

### 1. Install pgvector

```bash
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### 2. Create Database

```bash
createdb ai_news_embeddings
psql -d ai_news_embeddings -c "CREATE EXTENSION vector;"
```

### 3. Install Python Dependencies

```bash
pip install -r requirements-postgres.txt
```

### 4. Configure Environment

Copy the example configuration:
```bash
cp .env.postgres.example .env
```

Edit `.env` and set:
```bash
EMBEDDING_DB_BACKEND=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_news_embeddings
POSTGRES_USER=your_username
```

### 5. Initialize Schema

```bash
python scripts/embedding/embedding_db_pg.py --init
```

---

## Migrating Existing Data

If you have existing SQLite data:

```bash
# Dry run first (shows what will be migrated)
python scripts/embedding/migrate_to_pgvector.py --dry-run

# Actual migration
python scripts/embedding/migrate_to_pgvector.py

# Verify
python scripts/embedding/migrate_to_pgvector.py --verify-only
```

---

## Using PostgreSQL in Your Code

**No code changes needed!** The adapter automatically uses PostgreSQL:

```python
from scripts.embedding.embedding_db_adapter import get_db_adapter

# Automatically uses PostgreSQL (based on .env config)
db = get_db_adapter()

# Everything works the same
results = db.query_embeddings(
    query_vector,
    top_n=10,
    min_score=0.15,
    source_pools=["hackernews", "arxiv"]
)

print(f"Found {len(results)} results")
for result in results:
    print(f"  {result['title']} (score: {result['_score']:.3f})")
```

---

## Switching Back to SQLite

Just change your `.env`:

```bash
EMBEDDING_DB_BACKEND=sqlite
```

Restart your application - that's it!

---

## Troubleshooting

### "PostgreSQL is not running"

**macOS:**
```bash
brew services start postgresql@15
```

**Linux:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Start on boot
```

### "Could not connect to database"

Check PostgreSQL is running:
```bash
pg_isready
```

Test connection:
```bash
psql -h localhost -U $USER -d ai_news_embeddings
```

### "pgvector extension not found"

Reinstall pgvector:
```bash
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make clean
make
sudo make install

# Then enable in database
psql -d ai_news_embeddings -c "CREATE EXTENSION vector;"
```

### "Permission denied"

If you get permission errors, you may need to configure PostgreSQL authentication:

```bash
# Edit pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Add this line (replace with your username):
# local   all   your_username   trust

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Python import errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements-postgres.txt
```

---

## Performance Tuning

### For Better Speed (Lower Accuracy)

Edit your query or add to `.env`:
```python
# Faster search, slightly less accurate
results = db.query_embeddings(
    query_vector,
    top_n=10,
    min_score=0.10  # Lower threshold = faster
)
```

### For Better Accuracy (Slower)

```sql
-- In PostgreSQL, increase search quality
psql -d ai_news_embeddings -c "SET hnsw.ef_search = 80;"  -- Default is 40
```

### Rebuild Index for Better Performance

```sql
-- Drop and recreate with optimized parameters
DROP INDEX IF EXISTS story_embeddings_embedding_idx;

CREATE INDEX story_embeddings_embedding_idx
ON story_embeddings USING hnsw (embedding vector_cosine_ops)
WITH (m = 32, ef_construction = 128);  -- Higher quality, more memory
```

---

## What Gets Installed?

When you run the setup script:

1. **Database**: `ai_news_embeddings` (PostgreSQL database)
2. **Extension**: `pgvector` (vector similarity search)
3. **Python packages**:
   - `psycopg2-binary` - PostgreSQL adapter
   - `pgvector` - Python bindings
   - `numpy` - Vector operations
4. **Tables**:
   - `story_embeddings` - Story vectors with HNSW index
   - `section_embeddings` - Section vectors
   - `report_embeddings` - Report vectors

---

## FAQ

**Q: Do I need to change my code?**
A: No! The adapter handles everything. Just configure `.env`.

**Q: Can I use both SQLite and PostgreSQL?**
A: Yes! Switch by changing `EMBEDDING_DB_BACKEND` in `.env`.

**Q: What if PostgreSQL is already installed?**
A: The setup script detects existing installations and reuses them.

**Q: How much faster is PostgreSQL?**
A: 10-100x faster depending on database size. See benchmarks in PGVECTOR_MIGRATION_GUIDE.md.

**Q: Does this work on Windows?**
A: Yes, but you'll need to install PostgreSQL manually. Use the manual setup steps above.

**Q: Can I use my own PostgreSQL server?**
A: Yes! Just set `POSTGRES_HOST`, `POSTGRES_PORT`, etc. in `.env`.

---

## Next Steps

1. ✅ Setup complete? Great!
2. 📊 Migrate existing data (optional)
3. 🔍 Test semantic search performance
4. 📖 Read full guide: [PGVECTOR_MIGRATION_GUIDE.md](PGVECTOR_MIGRATION_GUIDE.md)

---

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/j-webtek/ai-news-extractor/issues)
- **Full Documentation**: [PGVECTOR_MIGRATION_GUIDE.md](PGVECTOR_MIGRATION_GUIDE.md)
- **Module README**: [scripts/embedding/README.md](../scripts/embedding/README.md)

---

**Ready to try it?**

```bash
./scripts/embedding/setup_local_postgres.sh
```

Enjoy your 10-100x faster semantic search! 🚀
