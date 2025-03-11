import webbrowser
from app import app


if __name__ == '__main__':
    webbrowser.open_new("http://localhost:8050")
    app.run_server()
