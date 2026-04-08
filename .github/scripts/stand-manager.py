#!/usr/bin/env python3
"""
Управление тестовыми стендами
Использование: python3 stand-manager.py [create|destroy|list] [stand_name]
"""

import os
import json
import subprocess
import sys
import time
from datetime import datetime

class StandManager:
    def __init__(self):
        self.stands_dir = "stands"
        self.port_base = 5000
        os.makedirs(self.stands_dir, exist_ok=True)
    
    def create_stand(self, stand_name, duration_minutes=60):
        """Создать новый стенд"""
        print(f"🚀 Создаем стенд: {stand_name}")
        
        # Проверяем, не существует ли уже
        if self.stand_exists(stand_name):
            print(f"❌ Стенд {stand_name} уже существует!")
            return False
        
        # Назначаем порт (на основе хэша имени)
        port = self.get_port_for_stand(stand_name)
        
        # Создаем папку для стенда
        stand_path = os.path.join(self.stands_dir, stand_name)
        os.makedirs(stand_path, exist_ok=True)
        
        # Копируем docker-compose.yml с заменой порта
        compose_src = "docker-compose.yml"
        compose_dst = os.path.join(stand_path, "docker-compose.yml")
        
        with open(compose_src, 'r') as f:
            content = f.read()
        
        # Заменяем порт
        content = content.replace("5000:5000", f"{port}:5000")
        content = content.replace("container_name: qa-app", f"container_name: qa-app-{stand_name}")
        content = content.replace("container_name: qa-postgres", f"container_name: qa-postgres-{stand_name}")
        
        with open(compose_dst, 'w') as f:
            f.write(content)
        
        # Запускаем стенд
        os.chdir(stand_path)
        result = subprocess.run(["docker", "compose", "up", "-d", "--build"], 
                               capture_output=True, text=True)
        os.chdir("../..")
        
        if result.returncode != 0:
            print(f"❌ Ошибка запуска: {result.stderr}")
            return False
        
        # Сохраняем метаданные
        metadata = {
            "name": stand_name,
            "port": port,
            "created_at": datetime.now().isoformat(),
            "duration_minutes": duration_minutes,
            "url": f"http://localhost:{port}",
            "status": "running"
        }
        
        with open(os.path.join(stand_path, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Стенд {stand_name} создан!")
        print(f"📍 URL: http://localhost:{port}")
        print(f"⏱️  Будет жить: {duration_minutes} минут")
        
        return True
    
    def destroy_stand(self, stand_name):
        """Удалить стенд"""
        print(f"🗑️ Удаляем стенд: {stand_name}")
        
        if not self.stand_exists(stand_name):
            print(f"❌ Стенд {stand_name} не найден!")
            return False
        
        stand_path = os.path.join(self.stands_dir, stand_name)
        
        # Останавливаем контейнеры
        os.chdir(stand_path)
        subprocess.run(["docker", "compose", "down", "-v"], 
                      capture_output=True, text=True)
        os.chdir("../..")
        
        # Удаляем папку
        import shutil
        shutil.rmtree(stand_path)
        
        print(f"✅ Стенд {stand_name} удален!")
        return True
    
    def list_stands(self):
        """Показать все стенды"""
        stands = []
        
        for stand_name in os.listdir(self.stands_dir):
            stand_path = os.path.join(self.stands_dir, stand_name)
            metadata_path = os.path.join(stand_path, "metadata.json")
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                stands.append(metadata)
        
        if not stands:
            print("📭 Нет активных стендов")
            return
        
        print("\n" + "="*60)
        print("АКТИВНЫЕ ТЕСТОВЫЕ СТЕНДЫ")
        print("="*60)
        
        for stand in stands:
            status = "🟢" if stand["status"] == "running" else "🔴"
            print(f"{status} {stand['name']}")
            print(f"   URL: {stand['url']}")
            print(f"   Создан: {stand['created_at']}")
            print(f"   Осталось: {self.get_remaining_time(stand)}")
            print("-"*40)
    
    def stand_exists(self, stand_name):
        """Проверить существование стенда"""
        stand_path = os.path.join(self.stands_dir, stand_name)
        return os.path.exists(stand_path)
    
    def get_port_for_stand(self, stand_name):
        """Получить порт для стенда на основе имени"""
        # Простой хэш для получения порта в диапазоне 5000-5999
        port_hash = sum(ord(c) for c in stand_name) % 1000
        return 5000 + port_hash
    
    def get_remaining_time(self, stand):
        """Рассчитать оставшееся время жизни стенда"""
        created = datetime.fromisoformat(stand["created_at"])
        duration = stand["duration_minutes"]
        expires = created.replace(minute=created.minute + duration)
        now = datetime.now()
        
        if now > expires:
            return "истекло"
        
        remaining = expires - now
        minutes = remaining.seconds // 60
        return f"{minutes} минут"

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 stand-manager.py [create|destroy|list] [arguments]")
        print("\nПримеры:")
        print("  python3 stand-manager.py list")
        print("  python3 stand-manager.py create feature-auth 60")
        print("  python3 stand-manager.py destroy feature-auth")
        sys.exit(1)
    
    manager = StandManager()
    command = sys.argv[1]
    
    if command == "list":
        manager.list_stands()
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ Укажите имя стенда")
            sys.exit(1)
        stand_name = sys.argv[2]
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        manager.create_stand(stand_name, duration)
    elif command == "destroy":
        if len(sys.argv) < 3:
            print("❌ Укажите имя стенда")
            sys.exit(1)
        manager.destroy_stand(sys.argv[2])
    else:
        print(f"❌ Неизвестная команда: {command}")

if __name__ == "__main__":
    main()