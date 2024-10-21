#!/usr/bin/env bash
set -e

# Check for missed migrations and raise error if one found
MIGRATION_CLASHES=$(PYTHONWARNINGS="ignore" TESTING_SKIP_MIGRATIONS=0 python manage.py makemigrations --dry-run)

if [ "$MIGRATION_CLASHES" != 'No changes detected' ];
then
    echo "Found missing migrations:"
    echo $MIGRATION_CLASHES
    exit 1
fi
echo "No missing migrations."

# http://codeinthehole.com/writing/avoiding-clashing-django-migrations/
MIGRATION_CLASHES=$(find . -type f -name "*.py" | grep -o ".*/migrations/[0-9]\+" | sort | uniq -c | awk '$1 > 1 {print $2}')
if [ -n "$MIGRATION_CLASHES" ]; then
    echo "Migration clashes!  The following migrations numbers are duplicated:"
    echo $MIGRATION_CLASHES
    exit 1
fi
echo "No conflicting migrations."
