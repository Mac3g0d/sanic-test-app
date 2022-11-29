from dataclasses import dataclass


@dataclass
class LoadBalancerConfig:
    REQUESTS_COUNT: int = 0
    REDIRECT_REQUEST_NUM: int = 3
    DB_HOST: str = 'db'
    DB_NAME: str = 'test_db'
    DB_USER: str = 'test_user'
    DB_PASSWORD: str = 'test_password'

    DATABASE_URI: str = f'mysql+aiomysql://test_user:test_password@db:3306/test_db'


