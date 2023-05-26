from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    api_key_faceit: SecretStr
    api_key_tracker: SecretStr
    database_hostname: SecretStr
    database_port: SecretStr
    database_password: SecretStr
    database_name: SecretStr
    database_username: SecretStr

    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings()