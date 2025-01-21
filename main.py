import sqlalchemy 
from sqlalchemy.orm import sessionmaker

from session import SESSION
from models import Book, Publisher, Stock, Sale, Shop

publisher = input('Введите имя или идентификатор издателя: ')

DSN = 'postgresql://postgres:postgres@localhost:5432/bookstore_db'


def get_shops(num):
    query = SESSION.query(Book.title, Shop.name, Sale.count, Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if publisher.isdigit():
        filtered_query = query.filter(Publisher.id == num).all()
    else:
        filtered_query = query.filter(Publisher.name == num).all()
    for book_title, shop_name, sale_count, sale_date in filtered_query:
        print(f'{book_title:<40} | {shop_name:<10} | {sale_count:<8} | {sale_date.strftime('%d-%m-%Y')}')

SESSION.close()

if __name__ == '__main__':
    get_shops(publisher)