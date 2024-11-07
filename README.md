# Running Without Docker

# 1. Clone the repository and create a virtual environment with Python 3.10:
git clone <repository_url>
cd <repository_directory>
python3.10 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# 2. Install dependencies:
pip install -r requirements.txt

# 3. Rename `.env.example` to `.env`:
mv .env.example .env

# 4. Generate a secret key:
python -c "import secrets; print(secrets.token_hex(64))"

# 5. Add the generated secret key to the `.env` file:
# SECRET_KEY=your_generated_key

# 6. Start the application from the root directory (not from the `app` directory):
flask --app app run

# 7. Open the application in your browser:
# http://127.0.0.1:5000
