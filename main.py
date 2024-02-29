from classes.Database import Database
from classes.AppManager import AppManager
from classes.SeleniumHandler import SeleniumHandler
from classes.RequestHandler import RequestHandler
from tkinter import Tk
from dotenv import load_dotenv
import os

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")


def main():
    database: Database = None
    try:
        database = Database(host=db_host, port=db_port, database=db_database, username=db_username, password=db_password)
        database.connect()
        request_handler = RequestHandler()
        selenium_handler = SeleniumHandler()
        app_manager = AppManager(request=request_handler, selenium=selenium_handler, database=database)
        app_manager.start()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
