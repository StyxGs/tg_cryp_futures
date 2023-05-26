import os
from dataclasses import dataclass

from apscheduler.jobstores.redis import RedisJobStore
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('TOKEN')
ADMIN_ID: str = os.environ.get('ADMIN_ID')

DB_USER: str = os.environ.get('DB_USER')
DB_PASS: str = os.environ.get('DB_PASS')
DB_HOST: str = os.environ.get('DB_HOST')
DB_PORT: str = os.environ.get('DB_PORT')
DB_NAME: str = os.environ.get('DB_NAME')
REDIS_PORT: int = os.environ.get('REDIS_PORT')
REDIS_HOST: str = os.environ.get('REDIS_HOST')


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    tgbot: TgBot


def load_config(path: str | None = None) -> Config:
    """Функция для загрузки конфигурационных данных о боте"""
    return Config(TgBot(token=TOKEN, admin_id=ADMIN_ID))


jobstores: dict = {
<<<<<<< HEAD
    'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                             run_times_key='dispatched_trips_running',
                             host=REDIS_HOST,
                             db=0,
                             port=REDIS_PORT)
}
=======
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running',
                                 host='bot_redis',
                                 db=0,
                                 port=6379)
    }
>>>>>>> 2f5cf95b81cc95cf4c288a97356397f059332337
