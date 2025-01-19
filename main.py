import sqlalchemy 
from sqlalchemy.orm import sessionmaker
from pprint import pprint
from models import create_tables, Book, Publisher, Stock, Sale, Shop

publisher = input('Введите имя или идентификатор издателя: ')

DSN = 'postgresql://postgres:postgres@localhost:5432/bookstore_db'

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

session = Session()


class Manager:
    def __init__(self, publisher):
        self.publisher = publisher
        self.books = self.__get_books()
        self.books_data = self.__add_stock()
        self.sales_data = self.__get_sales()

    def __get_books(self):
    # 1) Получение списка данных из таблицы book, фильтруя по Publisher.id
        result = []
        subq = session.query(Publisher).filter(Publisher.id == self.publisher).subquery()
        for c in session.query(Book).join(subq, Book.id_publisher == subq.c.id).all():
            book_title = c.title
            book_id = c.id
            result.append((book_id, book_title))
        return result

    def __get_shop(self, id_book, book_title):
    # 2) Получение списка данных из таблицы shop, фильтруя по Stock.id_book
        result = []
        subq = session.query(Stock).filter(Stock.id_book == id_book).subquery()
        for c in session.query(Shop).filter(Stock.id_shop==Shop.id).join(subq, Shop.id == subq.c.id_shop).all():
            shop_name = c.name
            id_shop = c.id
            result.append((id_book, id_shop, book_title, shop_name))
        return result

    def __get_shops(self):
    # 3) Объединяет результат __get_shop в один список
        result = []
        for data in self.books:
            shops = self.__get_shop(*data)
            result.append(shops)
        return result

    def __get_stock(self, id_book, id_shop):
    # 4) Получение stock.id из id_book, id_shop
        result = ''
        for c in session.query(Stock).filter(Stock.id_book == id_book).filter(Stock.id_shop == id_shop).all():
            result = c.id
        return result

    def __add_stock(self):
    # 5) Замена id_book, id_shop из списка на stock.id
        result = {}
        for shop_data in self.__get_shops():
            for shop in shop_data:
                data_for_stock = shop[:2]
                id_stock = self.__get_stock(*data_for_stock)
                result[id_stock] = [shop[2], shop[3]]
        return result

    def __get_sale(self, id_stock):
        result = ''
        for c in session.query(Sale).filter(Sale.id_stock==id_stock).all():
            date_sale = c.date_sale
            price = c.price
            id_stock = c.id_stock
            result = [price, date_sale]
        return result

    def __get_sales(self):
        result = {}
        for key, _ in self.books_data.items():
            sales = self.__get_sale(key)
            if sales:
                result[key] = sales
        return result

    def get_sales_data(self):
        result = []
        for id_stock, values in self.sales_data.items():
            for _id_stock, _values in self.books_data.items():
                if id_stock == _id_stock:
                    result.append(_values + values)
        return result

    
a = Manager(publisher)
    
pprint(a.get_sales_data())

session.close()