import hashlib
import time
# Согласно ТЗ создаём 3 класса, каждый со своими атрибутами и методами прописанными в тех задании.
class UrTube:
    def __init__(self):
        self.users = []
        self.current_user = None
        self.videos = []

    def register(self, nickname, password_hash, age):
        if any(user.nickname == nickname for user in self.users):
            print(f"Ошибка: Пользователь с никнеймом '{nickname}' уже существует.")
            return
        user = User(nickname, password_hash, age)
        self.users.append(user)
        print(f"Пользователь {nickname} успешно зарегистрирован!")

    def log_in(self, nickname, password):
        for user in self.users:
            if user.nickname == nickname and user.check_password(password):
                self.current_user = user
                print(f"Пользователь {nickname} успешно вошел в систему!")
                return

        print("Ошибка: Неверный никнейм или пароль.")

    def log_out(self):
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел из системы.")
            self.current_user = None
        else:
            print("Ошибка: Нет активного пользователя.")

    def add(self, *videos):
        for video in videos:
            if any(existing_video.title == video.title for existing_video in self.videos):
                print(f"Ошибка: Видео с названием '{video.title}' уже существует.")
            else:
                self.videos.append(video)
                print(f"Видео '{video.title}' успешно добавлено!")

    def get_videos(self, search_term):
        search_term_lower = search_term.lower()
        found_videos = [video for video in self.videos if search_term_lower in video.title.lower()]

        if found_videos:
            print("Найденные видео:")
            for video in found_videos:
                print(f"- {video.title}")
        else:
            print("Видео не найдены.")

    def watch_video(self, title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        video_to_watch = next((video for video in self.videos if video.title == title), None)  # Поиск с точным

        if video_to_watch is None:
            print("Видео не найдено.")
            return

        if video_to_watch.adult_mode == True and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        print(f"Начало просмотра видео: '{video_to_watch.title}'")

        current_time = 0
        is_paused = False

        while current_time < video_to_watch.duration:
            if is_paused:
                command = input("Введите 'play' для продолжения или 'stop' для остановки: ")
                if command == 'play':
                    is_paused = False
                    continue
                elif command == 'stop':
                    print("Просмотр остановлен.")
                    return
            else:
                time.sleep(1)
                current_time += 1
                print(f"Просмотр: {current_time} сек.")

                if current_time % 5 == 0:
                    print("Видео на паузе. Введите 'play' для продолжения или 'stop' для остановки.")
                    is_paused = True

        print("Конец видео")


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == self.hash_password(password)


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.adult_mode = adult_mode

# Проверяем, как будут работать методы в своих классах
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

ur.watch_video('Для чего девушкам парень программист?') # попытка просмотра без входа
ur.register('vasya_pupkin', 'lolkekcheburek', 13) # регистрация
ur.log_in('vasya_pupkin', 'lolkekcheburek') # вход
ur.watch_video('Для чего девушкам парень программист?') # попытка просмотра с возрастным ограничением
print({ur.current_user.nickname}) # Вывод на экран текущего пользователя
ur.log_out() # выход
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25) # регистрация
ur.log_in('urban_pythonist', 'iScX4vIJClb9YQavjAgF')
ur.watch_video('Для чего девушкам парень программист?')
print({ur.current_user.nickname})  # Вывод на экран текущего пользователя
ur.log_out() # выход
# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55) # регистрация
# с существующим ником
ur.log_in('vasya_pupkin', 'F8098FM8fjm9jmi') # попытка входа с неверным паролем
# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')