from app import app
import webbrowser


if __name__ == '__main__':
    webbrowser.open_new("http://localhost:8050")
    app.run_server()

