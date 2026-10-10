import mysql.connector
from mysql.connector import Error
import hashlib


def initialize_database():
    create_database()
    create_tables()
    setup_seller()
    setup_admin()
    print("راه‌اندازی کامل شد!")

def get_db_connection(database=None):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sepehr@1382',
            database=database
        )
        return connection
    except Error as e:
        print(f"خطا در اتصال: {e}")
        return None

def create_database():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS my_shop")
            print("دیتابیس my_shop ساخته شد")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"خطا در ساخت دیتابیس: {e}")

def create_tables():
    connection = get_db_connection(database='my_shop')
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(15) UNIQUE NOT NULL,
                    address TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seller (
                    id       INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255)       NOT NULL
                )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS  admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
               )
            """)


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id  INT AUTO_INCREMENT PRIMARY KEY,
                    name        VARCHAR(100)   NOT NULL,
                    price       DECIMAL(10, 2) NOT NULL,
                    stock       INT            NOT NULL,
                    category    VARCHAR(50),
                    brand       VARCHAR(50),
                    description TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mobiles (
                    mobile_id   INT AUTO_INCREMENT PRIMARY KEY,
                    product_id  INT NOT NULL,
                    screen_size VARCHAR(50),
                    ram         VARCHAR(50),
                    storage     VARCHAR(50),
                    battery     VARCHAR(50),
                    camera      VARCHAR(100),
                    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS laptops (
                    laptop_id   INT AUTO_INCREMENT PRIMARY KEY,
                    product_id  INT NOT NULL,
                    screen_size VARCHAR(50),
                    ram         VARCHAR(50),
                    storage     VARCHAR(50),
                    processor   VARCHAR(100),
                    gpu         VARCHAR(100),
                    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                )
            """)


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    cart_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL ,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                )
            """)


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                )
            """)

            connection.commit()
            print("تمام جداول با موفقیت ساخته شدند")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"خطا در ساخت جداول: {e}")

def setup_seller():
    connection = get_db_connection(database='my_shop')
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM seller WHERE username = 'seller'")
            if cursor.fetchone()[0] == 0:
                hashed_password = hashlib.sha256("1234".encode()).hexdigest()

                cursor.execute("""
                    INSERT INTO seller (username, password)
                    VALUES (%s, %s)
                """, ('seller', hashed_password))

                connection.commit()
                print("فروشنده پیش‌فرض ایجاد شد (نام کاربری: seller، رمز: 1234)")
            else:
                print("فروشنده  قبلاً ایجاد شده است")

            cursor.close()
            connection.close()
        except Error as e:
            print(f"خطا در ایجاد ادمین: {e}")

def setup_admin():
    connection = get_db_connection(database='my_shop')
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                hashed_password = hashlib.sha256("Sepehr@1382".encode()).hexdigest()

                cursor.execute("""
                    INSERT INTO admins (username, password)
                    VALUES (%s, %s)
                """, ('admin', hashed_password))

                connection.commit()
                print("ادمین پیش‌فرض ایجاد شد (نام کاربری: admin، رمز: Sepehr@1382)")
            else:
                print("ادمین  قبلاً ایجاد شده است")

            cursor.close()
            connection.close()
        except Error as e:
            print(f"خطا در ایجاد ادمین: {e}")

if __name__ == "__main__":
    initialize_database()
