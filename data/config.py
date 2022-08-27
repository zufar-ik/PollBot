from environs import Env

# Используем библиотеку environs
env = Env()
env.read_env()

# Считываем данные из .env

BOT_TOKEN = env.str('BOT_TOKEN')  # Токен бота
ADMINS = env.list('ADMIN')  # Список админов
DB_USER = env.str("POSTGRES_USER")
DB_PASS = env.str("POSTGRES_PASSWORD")
DB_NAME = env.str("POSTGRES_DB")
DB_HOST = env.str("POSTGRES_HOST")
