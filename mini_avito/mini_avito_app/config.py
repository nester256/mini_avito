from os.path import join
from dotenv import load_dotenv
from os import getenv


load_dotenv()
# App
APP = 'app'
HOMEPAGE = join(APP, 'index.html')
PROFILE_ACCOUNTS = join(APP, 'profile.html')
PRODUCT_LIST = join(APP, 'products_list.html')
PRODUCT_PAGE = join(APP, 'product.html')
MY_PRODUCT_PAGE = join(APP, 'my_products.html')
ORDERS_PAGE = join(APP, 'my_orders.html')
SALES_PAGE = join(APP, 'my_sales.html')
CREATE_PRODUCT_PAGE = join(APP, 'create_product.html')
# Price values
DECIMAL_PLACES = 2
DECIMAL_MAX_DIGITS = 10
# Paginator default
PAGINATE_THRESHOLD = 20
# CHARS DEFAULT
CHARS_DEFAULT = 40
# DEFAULT AWAIT TIME
TIME_AWAIT = 30

BOOST_URL = 'https://boostbank.ru/rest/{instance}/'
BOOST_HEADERS = {'Authorization': f'Token {getenv("BOOST_TOKEN")}'}
BOOST_ACCOUNT = f"{getenv('BOOST_MY_ACCOUNT')}"
BOOST_CALLBACK_URL = 'http://185.105.89.164:8000/rest/Order/{order_id}/'
BOOST_CALLBACK_HEADERS = {'Authorization': f"Token {getenv('TOKEN')}"}
BOOST_CALLBACK_REDIRECT = 'http://185.105.89.164:8000/profile/'
BOOST_REDIRECT = 'https://boostbank.ru/payment/{payment_id}'
