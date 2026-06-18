#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_SOURCE="$PROJECT_DIR/data/db.sqlite3"
BACKUP_DIR="$PROJECT_DIR/data/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_$TIMESTAMP.sqlite3"

mkdir -p "$BACKUP_DIR"

if [ ! -f "$DB_SOURCE" ]; then
    echo "Erro: banco de dados não encontrado em $DB_SOURCE"
    exit 1
fi

cp "$DB_SOURCE" "$BACKUP_FILE"
echo "Backup criado: $BACKUP_FILE"
