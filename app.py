from website import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

app.secret_key = 'dev-key-replace-in-production'

if __name__ == "__main__":
    app.run(debug=True)