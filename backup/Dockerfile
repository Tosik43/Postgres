FROM postgres:16

RUN apt-get update \
    && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backup

COPY backup/backup.sh /backup/backup.sh
COPY backup/backup.cron /etc/cron.d/student-db-backup

RUN chmod 750 /backup/backup.sh \
    && chmod 0644 /etc/cron.d/student-db-backup \
    && touch /var/log/cron.log

CMD ["cron", "-f"]