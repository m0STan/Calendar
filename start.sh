#!/bin/bash
#timeout 90s bash -c "until docker exec $DB_HOST pg_isready ; do sleep 5 ; done"

### Repeat command until port 5432 on address db is not ready.
#until nc -z -v -w30 db_postgres 5432
until !</dev/tcp/db/5432
do
echo "Waiting for database connection for 5 seconds..."

## Wait for 5 seconds before check again.
sleep 5
done
echo "Database server ready..."

#### run your server afterwards
alembic upgrade head
python main.py