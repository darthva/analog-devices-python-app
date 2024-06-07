# from pydantic_settings import BaseSettings

# class DatabaseSettings(BaseSettings):
#     db_user: str = "postgres"
#     db_password: str = "example"
#     db_host: str = "192.168.106.2"
#     db_port: int = 5432
#     db_name: str = "db"

#     @property
#     def db_url(self):
#         return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

# # Create an instance of the DatabaseSettings class
# settings = DatabaseSettings()
