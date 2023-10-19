# Менеджер паролей
Api для менеджера паролей

## Стек программы
FastApi, PostgreSql

## Как запустить проект
1. Требуется сделать git clone проекта
```bash
git clone https://github.com/LYAKAKOY/ManagerPassword.git
```
2. Перейти в папку ManagerPassword
```bash
cd ManagerPassword 
```
3. Собрать образы и запустить контейнеры 
```bash
docker compose -f docker-compose.yaml up -d 
```
4. Совершить миграции внутри контейнера backend с помощью alembic
```bash
docker-compose run --rm backend sh -c 'alembic upgrade heads'
```

## Как остановить проект
Чтобы остановить все контейнеры
```bash
docker compose -f docker-compose.yaml down --remove-orphans
```

## Documentation
После запуска будет доступна
[Documentation](http://localhost:8000/docs) по адресу http://localhost:8000/docs