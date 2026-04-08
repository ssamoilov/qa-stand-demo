import pytest
import time
import requests

def pytest_configure():
    """Ожидание готовности приложения перед тестами"""
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:5000/health")
            if response.status_code == 200:
                print("\n✅ Приложение готово к тестированию")
                return
        except:
            pass
        print(f"⏳ Ожидание приложения... {i+1}/{max_retries}")
        time.sleep(2)
    
    raise Exception("❌ Приложение не запустилось вовремя")