#!/bin/bash
# Восстанавливаем переменные окружения контейнера для cron.
while IFS= read -r -d '' entry; do
    case "$entry" in
        DB_NAME=*|DB_USER=*|DB_PASSWORD=*|DB_HOST=*|DB_PORT=*|TZ=*)
            export "$entry"
            ;;
    esac
done < /proc/1/environ

BACKUP_DIR="/backups"
MEDIA_DIR="/workspace/media"
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:?DB_NAME is required}"
DB_USER="${DB_USER:?DB_USER is required}"
TIMESTAMP="$(date +%Y-%m-%d_%H-%M-%S)"
TEMP_DIR="$(mktemp -d "${BACKUP_DIR}/.backup-${TIMESTAMP}.XXXXXX")"

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

export PGPASSWORD="${DB_PASSWORD:?DB_PASSWORD is required}"

mkdir -p "$BACKUP_DIR"

# Дожидаемся готовности PostgreSQL.
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"; do
    sleep 5
done

# Создаём дамп базы и проверяем его.
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -d "$DB_NAME" -Fc -f "${TEMP_DIR}/database.dump"

pg_restore --list "${TEMP_DIR}/database.dump" >/dev/null

# Архивируем загруженные документы.
tar -czf "${TEMP_DIR}/media.tar.gz" -C /workspace media

# Проверяем архив документов.
tar -tzf "${TEMP_DIR}/media.tar.gz" >/dev/null

# Публикуем комплект только после успешных проверок.
mv "$TEMP_DIR" "${BACKUP_DIR}/backup-${TIMESTAMP}"
trap - EXIT

# Оставляем пять последних комплектов.
mapfile -t BACKUPS < <(
    find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 \
        -type d -name 'backup-*' -printf '%f\n' | sort
)

while [ "${#BACKUPS[@]}" -gt 5 ]; do
    rm -rf -- "${BACKUP_DIR}/${BACKUPS[0]}"
    BACKUPS=("${BACKUPS[@]:1}")
done

echo "Backup completed: backup-${TIMESTAMP}"
