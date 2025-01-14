import schedule
import time
from scheduler import job
from db_manager import create_db

# Создаём базу данных
create_db()

schedule.every(1).minutes.do(job)

print("Сбор данных запущен...")
while True:
    schedule.run_pending()
    time.sleep(1)
