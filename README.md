# Socialcode 

Socialcode - программа, предоставляющая возможность обработки расчетных выписок с пожертвованиями в [Фонд борьбы с лейкемией](https://leikozu.net). В качестве результата работы программы в фонд отправляетс информация об отправителе денежных средств, сумма пожертвований, дата транзакции,  

## Документация

### Старт

1. Запуск в Docker-контейнере:

Требование: установленный Docker; 
  
- Сборка Docker-образа:
  
  ```bash
  docker build -t {{ наименование Docker-образа }} .
  ```

- Запуск Docker-контейнера:
     
  ```bash
  docker run -d  --name {{ наименование Docker-контейнера }} -v {{ директория на локальном узле с данными }}:{{ директория в Docker-контейнере с данными }} -e PATH_DIR={{директория с данными}} -p 8000:8000 {{ наименование Docker-образа }}
  ```

2. Запуск в стандартном режиме:

```bash
uvicorn main:app
```

### Запуск крон-джобы в битрикс24

1. Добавить импорта нашего модуля в файл local/php_interface/init.php
```require_once __DIR__ . '/include/hack.php';```
2. Создать файл local/php_interface/include/hack.php скопировав содержимое agent/agent.php, предварительно указав в нем в переменной $url адрес файлового сервера на котором запущен FastAPI сервер парсера из этого репозитория
3. В поиске админ панели битрикс найти "Агенты"
4. Нажать кнопку ![Кнопка](images/Screen%20Capture_select-area_20240519113114.png)
5. Заполнить форму создания агента ![Агент](images/Screen%20Capture_select-area_20240519113828.png)