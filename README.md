# 🧪 QA Test Stand Demo

## Быстрый старт

### Локальный запуск стенда
```bash
# Поднять стенд
docker-compose up -d --build

# Проверить работу
curl http://localhost:5000/health

# Посмотреть пользователей
curl http://localhost:5000/users

# Запустить тесты
cd tests
pip install -r requirements.txt
pytest -v

# Остановить стенд
docker-compose down -v