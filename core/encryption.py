#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZODI - Система шифрования для защиты данных пользователя
Использует Fernet для симметричного шифрования
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionManager:
    """Менеджер шифрования для защиты данных пользователя"""
    
    def __init__(self):
        self.key_file = os.path.join(os.path.dirname(__file__), '..', '.zodi_key')
        self.cipher_suite = self._get_or_create_cipher()
    
    def _get_or_create_cipher(self) -> Fernet:
        """Получить или создать ключ шифрования"""
        try:
            # Пытаемся загрузить существующий ключ
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                return Fernet(key)
        except Exception:
            pass
        
        # Создаем новый ключ
        return self._create_new_cipher()
    
    def _create_new_cipher(self) -> Fernet:
        """Создать новый ключ шифрования"""
        # Генерируем новый ключ
        key = Fernet.generate_key()
        
        # Сохраняем ключ в файл
        try:
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
        except Exception as e:
            print(f"Ошибка сохранения ключа шифрования: {e}")
        
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Зашифровать данные"""
        try:
            if not data:
                return ""
            
            # Конвертируем строку в байты
            data_bytes = data.encode('utf-8')
            
            # Шифруем данные
            encrypted_bytes = self.cipher_suite.encrypt(data_bytes)
            
            # Конвертируем в base64 для безопасного хранения
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            
            return encrypted_b64
        except Exception as e:
            print(f"Ошибка шифрования: {e}")
            return ""
    
    def decrypt(self, encrypted_data: str) -> str:
        """Расшифровать данные"""
        try:
            if not encrypted_data:
                return ""
            
            # Декодируем из base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Расшифровываем данные
            decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
            
            # Конвертируем обратно в строку
            decrypted_data = decrypted_bytes.decode('utf-8')
            
            return decrypted_data
        except Exception as e:
            print(f"Ошибка расшифровки: {e}")
            return ""
    
    def encrypt_file(self, input_file: str, output_file: str) -> bool:
        """Зашифровать файл"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read()
            
            encrypted_data = self.encrypt(data)
            
            if encrypted_data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(encrypted_data)
                return True
        except Exception as e:
            print(f"Ошибка шифрования файла: {e}")
        
        return False
    
    def decrypt_file(self, input_file: str, output_file: str) -> bool:
        """Расшифровать файл"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.decrypt(encrypted_data)
            
            if decrypted_data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(decrypted_data)
                return True
        except Exception as e:
            print(f"Ошибка расшифровки файла: {e}")
        
        return False
    
    def is_encrypted(self, data: str) -> bool:
        """Проверить, зашифрованы ли данные"""
        try:
            # Пытаемся декодировать как base64
            base64.b64decode(data.encode('utf-8'))
            return True
        except Exception:
            return False
    
    def get_key_info(self) -> dict:
        """Получить информацию о ключе шифрования"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                
                return {
                    'exists': True,
                    'size': len(key),
                    'created': os.path.getctime(self.key_file)
                }
        except Exception:
            pass
        
        return {'exists': False}
    
    def regenerate_key(self) -> bool:
        """Перегенерировать ключ шифрования"""
        try:
            # Создаем новый ключ
            new_cipher = self._create_new_cipher()
            self.cipher_suite = new_cipher
            return True
        except Exception as e:
            print(f"Ошибка перегенерации ключа: {e}")
            return False
    
    def backup_key(self, backup_path: str) -> bool:
        """Создать резервную копию ключа"""
        try:
            if os.path.exists(self.key_file):
                import shutil
                shutil.copy2(self.key_file, backup_path)
                return True
        except Exception as e:
            print(f"Ошибка создания резервной копии ключа: {e}")
        
        return False
    
    def restore_key(self, backup_path: str) -> bool:
        """Восстановить ключ из резервной копии"""
        try:
            if os.path.exists(backup_path):
                import shutil
                shutil.copy2(backup_path, self.key_file)
                
                # Перезагружаем cipher с восстановленным ключом
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                self.cipher_suite = Fernet(key)
                return True
        except Exception as e:
            print(f"Ошибка восстановления ключа: {e}")
        
        return False
