from pydantic_settings import BaseSettings, SettingsConfigDict

# Need to make sure all env variables are set before starting app. Pydantic has a way
class BaseConfig(BaseSettings):
    # DB sys var
    database_url: str
    database_port: str
    database_user: str
    database_pwd: str
    database_name: str

    # oauth sys vars
    secret_key: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env")

base_config = BaseConfig()
