from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов

PG_HOST = env.str("PG_HOST")
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")
