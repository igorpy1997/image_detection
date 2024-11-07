# Running Without Docker

# 1. Clone the repository and create a virtual environment with Python 3.10:
```shell
git clone <repository_url>
cd <repository_directory>
python3.10 -m venv venv(maybe you before this you need to use sudo apt install python3.10-venv
 on linux)
source venv/bin/activate  # Linux
`venv\Scripts\activate` #Windows
```
# 2. Install dependencies:
```shell
pip install -r app/requirements.txt
```
# 3. Rename `.env.example` to `.env`:
```shell
mv .env.example .env
```
# 4. Generate a secret key:
```shell
python -c "import secrets; print(secrets.token_hex(64))"
```
# 5. Add the generated secret key to the `.env` file:
```shell
SECRET_KEY=your_generated_key
```
# 6. Start the application from the root directory (not from the `app` directory):
```shell
cd app
flask --app api run
```
# 7. Open the application in your browser:
```shell
http://127.0.0.1:5000
```
