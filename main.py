import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Настройки запуска
hostName: str = "localhost"
serverPort: int = 8080

# Путь к файлу HTML
HTML_FILE_PATH: str = "html/contacts.html"


class MyServer(BaseHTTPRequestHandler):
    """Класс, который отвечает за обработку входящих запросов от клиентов"""

    def _get_html_content(self) -> str:
        """Получить содержимое HTML-файла"""
        try:
            with open(HTML_FILE_PATH, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.send_error(404, f"File '{HTML_FILE_PATH}' not found")
            return ""
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
            return ""

    def do_GET(self) -> None:
        """Метод для обработки входящих GET-запросов"""
        html_content = self._get_html_content()
        if not html_content:
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(html_content, "utf-8"))

    def _print_post_data(self, content_length: int) -> None:
        """Вывести данные POST-запроса в консоль"""
        post_data = self.rfile.read(content_length).decode('utf-8')

        print("=" * 50)
        print("ПОЛУЧЕНЫ ДАННЫЕ ОТ ПОЛЬЗОВАТЕЛЯ:")
        print("=" * 50)
        print(f"Время: {self.date_time_string()}")
        print(f"Длина: {content_length} байт")
        print(f"Данные: {post_data}")
        print("=" * 50)

    def do_POST(self) -> None:
        """Метод для обработки входящих POST-запросов"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))

            if content_length > 0:
                self._print_post_data(content_length)

            # Отправляем тот же HTML с сообщением об успехе
            html_content = self._get_html_content()
            if not html_content:
                return

            success_message = '<div class="alert alert-success">Сообщение отправлено!</div>'
            modified_html = html_content.replace(
                '<h1 class="text-center mb-4">Контакты</h1>',
                f'<h1 class="text-center mb-4">Контакты</h1>\n{success_message}',
            )

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes(modified_html, "utf-8"))

        except Exception as e:
            print(f"Ошибка обработки POST: {e}")
            self.send_error(500, f"Server error: {str(e)}")


def main() -> None:
    """Основная функция запуска сервера"""
    if not os.path.exists(HTML_FILE_PATH):
        print(f"Ошибка: Файл '{HTML_FILE_PATH}' не найден!")
        exit(1)

    # Создание сервера
    server: HTTPServer = HTTPServer((hostName, serverPort), MyServer)

    print(f"Сервер запущен: http://{hostName}:{serverPort}")
    print(f"Файл: {os.path.abspath(HTML_FILE_PATH)}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
