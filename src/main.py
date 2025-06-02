from http.server import BaseHTTPRequestHandler, HTTPServer
import os


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    """ Специальный класс, который отвечает за обработку входящих запросов от клиентов """

    def do_GET(self):
        if self.path == "/contacts":  # Путь для контактов
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Создаем правильный путь к файлу
            file_path = os.path.join(os.path.dirname(__file__), 'templates', 'contacts.html')

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.wfile.write(bytes(content, "utf-8"))
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("<html><body><h1>404 Not Found</h1></body></html>", "utf-8"))
        elif self.path == "/":  # Добавлена обработка корневого пути
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><h1>Welcome to the home page!</h1></body></html>", "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("<html><body><h1>404 Not Found</h1></body></html>", "utf-8"))

    def do_POST(self):
        """ Метод для обработки входящего POST-запроса """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")