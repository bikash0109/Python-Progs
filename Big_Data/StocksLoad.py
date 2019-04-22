import psycopg2
import zipfile
'''
@author-name:rishab katta
@author-name: milind kamath
@author-name: Bikash Roy
@author-name: Ankit Jain
'''

'''
Python Program to load stocks data into Postgresql server for phase 1 of Project.

Dataset link: https://www.kaggle.com/ehallmar/daily-historical-stock-prices-1970-2018#historical_stocks.csv
'''


class DatabaseConnection:

    def __init__(self, h, db, username, pwd):
        try:
            self.connection = psycopg2.connect(host=str(h), database=str(db), user=str(username), password=str(pwd))
            # self.connection = psycopg2.connect(host="localhost", database="stocks", user="user101", password="abcde")
            self.connection.autocommit=True
            self.cursor=self.connection.cursor()
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            print(getattr(e, 'message', str(e)))

    def create_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS company CASCADE')

        self.cursor.execute('DROP TABLE IF EXISTS historical_stock_price CASCADE')

        self.cursor.execute('DROP TABLE IF EXISTS sector CASCADE')

        self.cursor.execute('DROP TABLE IF EXISTS industry CASCADE')

        self.cursor.execute("CREATE TABLE company(ticker VARCHAR NOT NULL, exchange VARCHAR, "
                            "company_name VARCHAR, sector VARCHAR, industry VARCHAR, PRIMARY KEY(ticker))")

        self.cursor.execute("Create table historical_stock_price(id BIGSERIAL PRIMARY KEY, ticker VARCHAR, open_price float, "
                            "close_price float, adj_close_price float, low_price float, high_price float, volume BIGINT, "
                            "stock_date DATE, FOREIGN KEY(ticker) REFERENCES Company(ticker))")

        self.cursor.execute("CREATE TABLE sector(sectorid SERIAL primary key, sector text)")

        self.cursor.execute("CREATE TABLE industry(industryid SERIAL primary key, industry text)")

    def insert_tables(self, path):

        # with zipfile.ZipFile(str(path) +"daily-historical-stock-prices-1970-2018.zip", "r") as zip_ref:
        #     zip_ref.extractall(str(path))

        file = path + "historical_stocks.csv"
        self.cursor.execute("copy company(ticker, exchange, company_name, sector,"
                            " industry) FROM %s DELIMITER ',' CSV HEADER", (file,))

        file = path + "historical_stock_prices.csv"
        self.cursor.execute("copy historical_stock_price(ticker, open_price, close_price, adj_close_price,"
                            " low_price, high_price, volume, stock_date) FROM %s DELIMITER ',' CSV HEADER", (file,))

        self.cursor.execute('INSERT INTO sector (sector) SELECT distinct sector FROM company')
        self.cursor.execute('INSERT INTO industry (industry) SELECT distinct industry FROM company')
        self.connection.commit()

        queryAlter = 'ALTER TABLE company ' \
                     'ALTER COLUMN sector TYPE number'

        queryAlter1 = 'ALTER TABLE company ' \
                      'ALTER COLUMN industry TYPE number'
        self.cursor.execute(queryAlter)
        self.cursor.execute(queryAlter1)
        self.connection.commit()
        query = 'UPDATE company SET sector = s.sectorid  ' \
                'FROM company c ' \
                'JOIN sector s ON c.sector = s.sector '
        self.cursor.execute(query)
        self.connection.commit()
        query1 = 'UPDATE company SET industry = i.industryid  ' \
                 'FROM company c ' \
                 'JOIN industry i ON c.industry = i.industry '
        self.cursor.execute(query1)
        self.connection.commit()


if __name__ == '__main__':
    h = str(input("Enter host name"))
    db = str(input("Enter Database Name"))
    username = str(input("Enter username"))
    pwd = str(input("Enter password"))
    path = str(input("Enter Path except the file name - example- C:/users/files/"))

    database_connection = DatabaseConnection(h, db, username, pwd)
    database_connection.create_tables()
    database_connection.insert_tables(path)