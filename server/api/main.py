# main.py
from . import create_app

app = create_app()

if __name__ == '__main__':
    # Use a production-ready WSGI server like Gunicorn
    # For development, you can use app.run()
    app.run(host='0.0.0.0', port=8080) # Or your preferred port