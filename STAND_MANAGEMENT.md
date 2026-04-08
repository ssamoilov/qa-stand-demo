# 🧪 Управление тестовыми стендами

## Быстрый старт

### Создать стенд через Issue:

1. **Создай Issue** с названием стенда (например: `feature-auth`)
2. **Добавь лейбл** `create-stand`
3. **Жди комментарий** с URL стенда

### Создать стенд через Actions:

1. **Actions** → **Create Test Stand** → **Run workflow**
2. **Укажи имя** и время жизни
3. **Нажми Run**

### Удалить стенд:

- **Через Issue:** Добавь лейбл `destroy-stand`
- **Через Actions:** Запусти `Destroy Test Stand`

## Команды

```bash
# Список всех стендов
gh workflow run list-stands.yml

# Создать стенд через CLI
gh workflow run create-stand.yml -f stand_name=my-stand -f duration=120

# Удалить стенд
gh workflow run destroy-stand.yml -f stand_name=my-stand