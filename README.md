### Регистрация пользователя

Отправьте POST-запрос на `/user/signup/` с данными в формате JSON (например {"username": "yourusername", "password": "yourpassword"}).

### Авторизация пользователя

Отправьте POST-запрос на `/user/login/` с данными (например {"username": "yourusername", "password": "yourpassword"}).

В ответ вы получите токен. Используйте его для аутентификации в дальнейших запросах.

### Создание поста

Чтобы создать новый пост, отправьте POST-запрос на `/posts/` с данными (например {"title": "Another", "content": "Come text"}).

Чтобы получить пост, отправьте GET-запрос на `/posts/`. Там можно получить значения content_type и id для последующего комментирования.

### Создание комментария

Чтобы создать новый комментарий для поста, отправьте POST-запрос на `/comments/` с данными например ({"content": "Комментарий", "content_type": 11, "object_id": 1})

Или комментарий для комментария ({"content": "Ваш комментарий", "parent": 1}):

### Оценка комментария

Чтобы оценить комментарий, отправьте POST-запрос на `/comment/{comment_id}/add_rating/` с данными ({"rating": 1} для лайка или {"rating": -1}  для дизлайка)

### Получение информации о комментарии

Чтобы получить информацию о комментарии, отправьте GET-запрос на `/comments/{comment_id}/`. Там можно увидеть общий рейтинг самого комментария, так и всей ветки.

## Тестирование

Вы можете запустить тесты с помощью команды:

```bash
python manage.py test
```
