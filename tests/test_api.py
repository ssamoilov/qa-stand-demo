import pytest
import requests
import time

BASE_URL = "http://localhost:5000"

class TestAPI:
    
    def test_health_endpoint(self):
        """Проверка, что приложение живо"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
    
    def test_get_users(self):
        """Получение списка пользователей"""
        response = requests.get(f"{BASE_URL}/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) >= 3  # минимум 3 тестовых пользователя
        
        # Проверяем структуру данных
        first_user = users[0]
        assert "id" in first_user
        assert "name" in first_user
        assert "email" in first_user
    
    def test_create_user(self):
        """Создание нового пользователя"""
        new_user = {
            "name": "CI Test User",
            "email": f"ci_test_{int(time.time())}@example.com"
        }
        response = requests.post(f"{BASE_URL}/users", json=new_user)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        
        # Проверяем, что пользователь добавился
        get_response = requests.get(f"{BASE_URL}/users")
        users = get_response.json()
        emails = [u["email"] for u in users]
        assert new_user["email"] in emails
    
    def test_user_validation(self):
        """Проверка валидации (отсутствует email)"""
        invalid_user = {"name": "No Email"}
        response = requests.post(f"{BASE_URL}/users", json=invalid_user)
        # Должна быть ошибка 500 или 400 (зависит от реализации)
        assert response.status_code >= 400