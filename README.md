## How to generate secret?
```shell
python -c "import secrets;print(secrets.token_hex(64))"
```

Now paste this secret to your .env file and do not expose it to your friend :)

