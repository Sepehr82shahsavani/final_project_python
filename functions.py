from data_base import get_db_connection
from classes import *
from mysql.connector import Error
import mysql.connector
import hashlib
import mysql.connector
from colorama import init, Fore, Style
init(autoreset=True)


# تابع مربوط به ثبت نام کاربر
def register_user():
    new_user = User()

    print(f"{Style.BRIGHT}{Fore.CYAN}--- فرم ثبت نام کاربر ---")

    while True:
        try:
            username_input = input(f"{Fore.GREEN}نام کاربری خود را وارد کنید: ")
            new_user.username = username_input
            break
        except ValueError as e:
            print(f"{Fore.RED}خطا: {e}")

    while True:
        try:
            password_input = input(f"{Fore.GREEN}رمز عبور خود را وارد کنید: ")
            new_user.password = password_input
            break
        except ValueError as e:
            print(f"{Fore.RED}خطا: {e}")

    while True:
        try:
            email_input = input(f"{Fore.GREEN}ایمیل خود را وارد کنید: ")
            new_user.email = email_input
            break
        except ValueError as e:
            print(f"{Fore.RED}خطا: {e}")

    while True:
        try:
            phone_input = input(f"{Fore.GREEN}شماره تلفن خود را وارد کنید (مثال: 09123456789): ")
            new_user.phone = phone_input
            break
        except ValueError as e:
            print(f"{Fore.RED}خطا: {e}")

    address_input = input(f"{Fore.YELLOW}آدرس خود را وارد کنید (اختیاری - برای رد شدن Enter بزنید): ")
    if address_input.strip() == "":
        address_input = None

    db_connection = get_db_connection(database="my_shop")

    if db_connection is None:
        print(f"{Fore.RED}عملیات ثبت نام به دلیل عدم اتصال به دیتابیس لغو شد.")
        return

    try:
        cursor = db_connection.cursor()

        sql_query = """
                    INSERT INTO users (username, password, email, phone, address)
                    VALUES (%s, %s, %s, %s, %s) \
                    """
        values = (new_user.username, new_user.password, new_user.email, new_user.phone, address_input)

        cursor.execute(sql_query, values)
        db_connection.commit()

        print(f"\n{Fore.GREEN}✅ ثبت نام با موفقیت انجام شد و در دیتابیس ذخیره گردید!")

    except mysql.connector.IntegrityError as err:
        print(f"\n{Fore.RED} خطا در پایگاه داده: این اطلاعات (نام کاربری، ایمیل یا شماره تلفن) قبلا ثبت شده است.")
        print(f"{Fore.YELLOW}جزئیات خطا: {err}")

    except mysql.connector.Error as err:
        print(f"\n{Fore.RED} خطای ارتباط با دیتابیس: {err}")

    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()

#تابع مربوط به وارد شدن به پنل کاربری
def login_user():
    print(Fore.CYAN + "\n=== ورود کاربر ===" + Fore.RESET)

    username = input("نام کاربری: ")
    password = input("رمز عبور: ")

    try:
        connection = get_db_connection(database='my_shop')
        cursor = connection.cursor()

        query = "SELECT user_id, username FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            print(Fore.GREEN + f"خوش آمدید {user[1]}" + Fore.RESET)
            return user[0]
        else:
            print(Fore.RED + "نام کاربری یا رمز عبور اشتباه است" + Fore.RESET)
            return None

    except Exception as e:
        print(Fore.RED + f"خطا در ورود: {e}" + Fore.RESET)
        return None

def register_seller(username, password, db_conn):
    if db_conn is None:
        print("خطا: اتصال به دیتابیس برقرار نیست.")
        return None

    try:
        new_seller = Seller()
        new_seller.username = username
        new_seller.password = password

        hashed_password = hashlib.sha256(new_seller.password.encode('utf-8')).hexdigest()
        new_seller.password = hashed_password

        cursor = db_conn.cursor()
        cursor.execute("USE my_shop")

        query = "INSERT INTO seller (username, password) VALUES (%s, %s)"
        cursor.execute(query, (new_seller.username, new_seller.password))
        db_conn.commit()

        new_seller.id = cursor.lastrowid
        print(f"فروشنده با موفقیت ثبت شد (ID: {new_seller.id}).")

        cursor.close()
        return new_seller

    except ValueError as ve:
        print(f"خطای اعتبارسنجی اطلاعات: {ve}")
        return None

    except mysql.connector.Error as e:
        print(f"خطای دیتابیس: {e}")
        return None
def login_seller(username, password, db_conn):
    try:
        # هش کردن رمز عبور ورودی برای جستجو در دیتابیس
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        cursor = db_conn.cursor()
        cursor.execute("USE my_shop")

        # جستجوی مستقیم در دیتابیس
        query = "SELECT id, username FROM seller WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))

        seller_data = cursor.fetchone()
        cursor.close()

        # اگر نتیجه‌ای پیدا شد یعنی اطلاعات درست است
        if seller_data:
            seller = Seller()
            seller.id = seller_data[0]
            seller.username = seller_data[1]
            print("ورود با موفقیت انجام شد.")
            return seller
        else:
            print("نام کاربری یا رمز عبور اشتباه است.")
            return None

    except Exception as e:
        print(f"خطا در ورود: {e}")
        return None

#لاگ این و ثبت نام ادمین

def register_admin(username, password, db_conn):
    if db_conn is None:
        print("خطا: اتصال به دیتابیس برقرار نیست.")
        return None

    try:
        new_admin = Admin()
        new_admin.username = username
        new_admin.password = password

        hashed_password = hashlib.sha256(new_admin.password.encode('utf-8')).hexdigest()
        new_admin.password = hashed_password

        cursor = db_conn.cursor()
        cursor.execute("USE my_shop")

        query = "INSERT INTO admins (username, password) VALUES (%s, %s)"
        cursor.execute(query, (new_admin.username, new_admin.password))
        db_conn.commit()

        new_admin.id = cursor.lastrowid
        print(f"ادمین با موفقیت ثبت شد (ID: {new_admin.id}).")

        cursor.close()
        return new_admin

    except ValueError as ve:
        print(f"خطای اعتبارسنجی اطلاعات: {ve}")
        return None

    except mysql.connector.Error as e:
        print(f"خطای دیتابیس: {e}")
        return None
def login_admin(username, password, db_conn):
    try:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        cursor = db_conn.cursor()
        cursor.execute("USE my_shop")

        query = "SELECT id, username FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))

        admin_data = cursor.fetchone()
        cursor.close()

        if admin_data:
            seller = Seller()
            seller.id = admin_data[0]
            seller.username = admin_data[1]
            print("ورود ادمین با موفقیت انجام شد.")
            return seller
        else:
            print("نام کاربری یا رمز عبور اشتباه است.")
            return None

    except Exception as e:
        print(f"خطا در ورود: {e}")
        return None

#توابع مربوط به منو ادمین

def admin_delete_user(db_conn):
    cursor = db_conn.cursor()

    cursor.execute("SELECT user_id, username FROM users")
    all_users = cursor.fetchall()

    if len(all_users) == 0:
        print(Fore.YELLOW + "\nهیچ کاربری در سیستم ثبت نشده است." + Fore.RESET)
        cursor.close()
        return

    print(Fore.CYAN + "\n--- لیست کاربران ---" + Fore.RESET)
    for user in all_users:
        user_id = user[0]
        user_name = user[1]
        print(f"ID: {user_id}  |  نام کاربری: {user_name}")
    print("--------------------")

    print("لطفاً ID کاربری که می‌خواهید حذف کنید را وارد کنید.")
    print("اگر می‌خواهید انصراف دهید، فقط دکمه Enter را بزنید.")
    target_id = input("شماره ID: ")

    if target_id == "":
        print("عملیات لغو شد.")
        cursor.close()
        return

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (target_id,))
    found_user = cursor.fetchall()

    if len(found_user) == 0:
        print(Fore.RED + "کاربری با این ID یافت نشد!" + Fore.RESET)
    else:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (target_id,))
        db_conn.commit()
        print(Fore.GREEN + f"کاربر با ID {target_id} با موفقیت حذف شد." + Fore.RESET)

    cursor.close()
def admin_delete_seller(db_conn):
    cursor = db_conn.cursor()

    cursor.execute("SELECT id, username FROM seller")
    all_sellers = cursor.fetchall()

    if len(all_sellers) == 0:
        print(Fore.YELLOW + "\nهیچ فروشنده‌ای در سیستم ثبت نشده است." + Fore.RESET)
        cursor.close()
        return

    print(Fore.CYAN + "\n--- لیست فروشندگان ---" + Fore.RESET)
    for seller in all_sellers:
        seller_id = seller[0]
        seller_name = seller[1]
        print(f"ID: {seller_id}  |  نام کاربری: {seller_name}")
    print("----------------------")

    print("لطفاً ID فروشنده‌ای که می‌خواهید حذف کنید را وارد کنید.")
    print("اگر می‌خواهید انصراف دهید، فقط دکمه Enter را بزنید.")
    target_id = input("شماره ID: ")

    if target_id == "":
        print("عملیات لغو شد.")
        cursor.close()
        return

    cursor.execute("SELECT * FROM seller WHERE id = %s", (target_id,))
    found_seller = cursor.fetchall()

    if len(found_seller) == 0:
        print(Fore.RED + "فروشنده‌ای با این ID یافت نشد!" + Fore.RESET)
    else:
        cursor.execute("DELETE FROM seller WHERE id = %s", (target_id,))
        db_conn.commit()
        print(Fore.GREEN + f"فروشنده با ID {target_id} با موفقیت حذف شد." + Fore.RESET)

    cursor.close()

#تابع اضافه کردن محصولات

def add_product_menu():
    while True:
        print("\n--- منوی اضافه کردن محصول ---")
        print("1. موبایل")
        print("2. لپ‌تاپ")
        print("3. محصولات عادی")
        print("4. بازگشت")

        choice = input("لطفاً گزینه مورد نظر خود را انتخاب کنید (1-4): ")

        if choice == '1':
            add_mobile()
        elif choice == '2':
            add_laptop()
        elif choice == '3':
            add_normal_product()
        elif choice == '4':
            print("بازگشت به منوی قبل...")
            break
        else:
            print("گزینه نامعتبر است. لطفاً دوباره تلاش کنید.")

def add_mobile():
    print("\n--- اضافه کردن موبایل جدید ---")
    mobile = Mobile()

    while True:
        try:
            mobile.name = input("نام موبایل را وارد کنید: ")
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            mobile.price = float(input("قیمت را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: مقدار نامعتبر است. {e}")

    while True:
        try:
            mobile.stock = int(input("موجودی را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: مقدار نامعتبر است. {e}")

    mobile.brand = input("برند را وارد کنید: ")
    mobile.description = input("توضیحات محصول را وارد کنید: ")

    while True:
        try:
            mobile.screen_size = float(input("اندازه صفحه نمایش (اینچ) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            mobile.ram = int(input("مقدار رم (گیگابایت) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            mobile.storage = int(input("حافظه داخلی (گیگابایت) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            mobile.battery = int(input("ظرفیت باتری (میلی‌آمپر) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            mobile.camera = float(input("کیفیت دوربین (مگاپیکسل) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    conn = get_db_connection(database="my_shop")
    if not conn:
        print("خطا: ارتباط با دیتابیس برقرار نشد.")
        return

    try:
        cursor = conn.cursor()
        insert_product_query = """
                               INSERT INTO products (name, price, stock, category, brand, description)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """
        cursor.execute(insert_product_query, (
            mobile.name,
            mobile.price,
            mobile.stock,
            mobile.category,
            mobile.brand,
            mobile.description
        ))

        product_id = cursor.lastrowid

        insert_mobile_query = """
                              INSERT INTO mobiles (product_id, screen_size, ram, storage, battery, camera)
                              VALUES (%s, %s, %s, %s, %s, %s)
                              """
        cursor.execute(insert_mobile_query, (
            product_id,
            mobile.screen_size,
            mobile.ram,
            mobile.storage,
            mobile.battery,
            mobile.camera
        ))

        conn.commit()
        print(f"\nموبایل '{mobile.name}' با موفقیت در دیتابیس ثبت شد!")

    except Exception as e:
        conn.rollback()
        print(f"\nخطا در ثبت اطلاعات در دیتابیس: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
def add_laptop():
    print("\n--- اضافه کردن لپ‌تاپ جدید ---")
    laptop = Laptop()

    while True:
        try:
            laptop.name = input("نام لپ‌تاپ را وارد کنید: ")
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            laptop.price = float(input("قیمت را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: مقدار نامعتبر است. {e}")

    while True:
        try:
            laptop.stock = int(input("موجودی را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: مقدار نامعتبر است. {e}")

    laptop.brand = input("برند را وارد کنید: ")
    laptop.description = input("توضیحات محصول را وارد کنید: ")

    while True:
        try:
            laptop.screen_size = float(input("اندازه صفحه نمایش (اینچ) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            laptop.ram = int(input("مقدار رم (گیگابایت) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            laptop.storage = int(input("حافظه داخلی (گیگابایت) را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            laptop.processor = input("مدل پردازنده (CPU) را وارد کنید: ")
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            laptop.gpu = input("مدل کارت گرافیک (GPU) را وارد کنید: ")
            break
        except ValueError as e:
            print(f"خطا: {e}")

    conn = get_db_connection(database="my_shop")
    if not conn:
        print("خطا: ارتباط با دیتابیس برقرار نشد.")
        return

    try:
        cursor = conn.cursor()
        insert_product_query = """
                               INSERT INTO products (name, price, stock, category, brand, description)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """
        cursor.execute(insert_product_query, (
            laptop.name,
            laptop.price,
            laptop.stock,
            laptop.category,
            laptop.brand,
            laptop.description
        ))

        product_id = cursor.lastrowid

        insert_laptop_query = """
                              INSERT INTO laptops (product_id, screen_size, ram, storage, processor, gpu)
                              VALUES (%s, %s, %s, %s, %s, %s)
                              """
        cursor.execute(insert_laptop_query, (
            product_id,
            laptop.screen_size,
            laptop.ram,
            laptop.storage,
            laptop.processor,
            laptop.gpu
        ))

        conn.commit()
        print(f"\nلپ‌تاپ '{laptop.name}' با موفقیت در دیتابیس ثبت شد!")

    except Exception as e:
        conn.rollback()
        print(f"\nخطا در ثبت اطلاعات در دیتابیس: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
def add_normal_product():
    print("\n--- اضافه کردن محصول عادی ---")
    product = Product()

    while True:
        try:
            product.name = input("نام محصول را وارد کنید: ")
            break
        except ValueError as e:
            print(f"خطا: {e}")

    while True:
        try:
            product.price = float(input("قیمت را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: مقدار نامعتبر است. {e}")

    while True:
        try:
            product.stock = int(input("موجودی را وارد کنید: "))
            break
        except ValueError as e:
            print(f"خطا: مقدار نامعتبر است. {e}")

    product.category = input("دسته‌بندی محصول را وارد کنید: ")
    product.brand = input("برند را وارد کنید: ")
    product.description = input("توضیحات محصول را وارد کنید: ")

    conn = get_db_connection(database="my_shop")
    if not conn:
        print("خطا: ارتباط با دیتابیس برقرار نشد.")
        return

    try:
        cursor = conn.cursor()
        insert_product_query = """
                               INSERT INTO products (name, price, stock, category, brand, description)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """
        cursor.execute(insert_product_query, (
            product.name,
            product.price,
            product.stock,
            product.category,
            product.brand,
            product.description
        ))

        conn.commit()
        print(f"\nمحصول '{product.name}' با موفقیت در دیتابیس ثبت شد!")

    except Exception as e:
        conn.rollback()
        print(f"\nخطا در ثبت اطلاعات در دیتابیس: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#منو نشان دادن محصولات
def view_products():
    while True:
        print("--- مشاهده محصولات ---")
        print("1. همه محصولات")
        print("2. موبایل‌ها")
        print("3. لپ‌تاپ‌ها")
        print("4. محصولات عادی")
        print("5. بازگشت")

        choice = input("لطفا یک گزینه را انتخاب کنید: ")

        if choice == '1':
            view_all_products()
        elif choice == '2':
            view_mobiles()
        elif choice == '3':
            pass
        elif choice == '4':
            pass

        elif choice == '5':
            break

        else:
            print("گزینه نامعتبر است. دوباره تلاش کنید.")

def view_all_products():
    print("--- مشاهده محصولات ---")

    conn = get_db_connection(database="my_shop")
    if not conn:
        print("خطا در اتصال به دیتابیس.")
        return

    try:
        cursor = conn.cursor()
        query = "SELECT product_id, name, price, stock, category, brand FROM products"
        cursor.execute(query)
        products = cursor.fetchall()

        if not products:
            print("هیچ محصولی در دیتابیس یافت نشد.")
            return

        print(f"{'ID':<5} | {'نام':<20} | {'قیمت':<12} | {'موجودی':<8} | {'دسته‌بندی':<15} | {'ID'}")
        print("-" * 80)

        for i in products:
            p_id, name, price, stock, category, brand = i
            print(f"{p_id:<5} | {name:<20} | {price:<12} | {stock:<8} | {category:<15} | ")

    except Exception as e:
        print(f"\nخطا در دریافت اطلاعات از دیتابیس: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn:
            conn.close()

def view_mobiles():
    print("\n--- مشاهده لیست موبایل‌ها ---")

    connection = get_db_connection(database='my_shop')
    if not connection:
        print("خطا در اتصال به دیتابیس.")
        return

    try:
        cursor = connection.cursor()

        query = """
                SELECT p.product_id,
                       p.name,
                       p.price,
                       p.brand,
                       m.screen_size,
                       m.ram,
                       m.storage,
                       m.battery,
                       m.camera
                FROM products p
                         INNER JOIN mobiles m ON p.product_id = m.product_id \
                """

        cursor.execute(query)
        mobiles = cursor.fetchall()

        if not mobiles:
            print("\nهیچ موبایلی در دیتابیس موجود نیست.")
            return

        print(
            f"\n{'کد':>5} | {'نام':>15} | {'قیمت':>12} | {'برند':>10} | {'صفحه':>8} | {'رم':>6} | {'حافظه':>8} | {'باتری':>8} | {'دوربین':>10}")
        print("-" * 110)

        for mobile in mobiles:
            pid, name, price, brand, screen, ram, storage, battery, camera = mobile
            print(
                f"{pid:>5} | {name:>15} | {price:>12,} | {brand:>10} | {screen:>8} | {ram:>6} | {storage:>8} | {battery:>8} | {camera:>10}")

        print("-" * 110)
        print(f"تعداد کل موبایل‌ها: {len(mobiles)}\n")

    except Exception as e:
        print(f"\nخطا در دریافت اطلاعات موبایل‌ها: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()
def view_laptops():
    print("\n--- مشاهده لیست لپ‌تاپ‌ها ---")

    connection = get_db_connection(database='my_shop')
    if not connection:
        print("خطا در اتصال به دیتابیس.")
        return

    try:
        cursor = connection.cursor()

        query = """
                SELECT p.product_id,
                       p.name,
                       p.price,
                       p.brand,
                       l.screen_size,
                       l.ram,
                       l.storage,
                       l.processor,
                       l.gpu
                FROM products p
                         INNER JOIN laptops l ON p.product_id = l.product_id \
                """

        cursor.execute(query)
        laptops = cursor.fetchall()

        if not laptops:
            print("\nهیچ لپ‌تاپی در دیتابیس موجود نیست.")
            return

        print(
            f"\n{'کد':>8} | {'نام':>15} | {'قیمت':>12} | {'برند':>10} | {'صفحه':>8} | {'رم':>6} | {'حافظه':>8} | {'پردازنده':>15} | {'گرافیک':>12}")
        print("-" * 120)

        for laptop in laptops:
            pid, name, price, brand, screen, ram, storage, cpu, gpu = laptop
            print(
                f"{pid:>8} | {name:>15} | {price:>12,} | {brand:>10} | {screen:>8} | {ram:>6} | {storage:>8} | {cpu:>15} | {gpu:>12}")

        print("-" * 120)
        print(f"تعداد کل لپ‌تاپ‌ها: {len(laptops)}\n")

    except Exception as e:
        print(f"\nخطا در دریافت اطلاعات لپ‌تاپ‌ها: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()
def view_regular_products():
    connection = get_db_connection(database='my_shop')
    cursor = connection.cursor()

    query = """
            SELECT p.product_id, p.name, p.price, p.category, p.brand
            FROM products p
            WHERE p.product_id NOT IN (SELECT product_id FROM mobiles)
              AND p.product_id NOT IN (SELECT product_id FROM laptops) \
            """
    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    if not products:
        print("\n هیچ محصول عادی موجود نیست")
        return

    print(f"\n{'کد':>8} {'نام محصول':>20} {'قیمت':>15} {'دسته':>12} {'برند':>15}")
    print("-" * 90)

    for product in products:
        pid, name, price, category, brand = product
        print(f"{pid:>8} {name:>20} {price:>15,} {category:>12} {brand:>15}")

    print("-" * 90)
    print(f"تعداد: {len(products)}")

#تابع ادیت محصول توسط ادمین

def edit_general_product():
    view_all_products()
    product_id = input(Fore.CYAN + "شناسه محصول را وارد کنید: ")
    db = get_db_connection(database='my_shop')

    cursor = db.cursor()

    cursor.execute("SELECT name, price, stock, category, brand, description FROM products WHERE product_id = %s",
                   (product_id,))
    row = cursor.fetchone()

    if row:
        prod = Product()

        while True:
            try:
                name = input(f"نام [{row[0]}]: ") or row[0]
                prod.name = str(name)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                price = input(f"قیمت [{row[1]}]: ") or row[1]
                prod.price = float(price)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: مقداری که وارد کردید نامعتبر است ({e})")

        while True:
            try:
                stock = input(f"موجودی [{row[2]}]: ") or row[2]
                prod.stock = int(stock)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: مقداری که وارد کردید نامعتبر است ({e})")

        while True:
            try:
                category = input(f"دسته‌بندی [{row[3]}]: ") or row[3]
                prod.category = str(category)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                brand = input(f"برند [{row[4]}]: ") or row[4]
                prod.brand = str(brand)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                desc = input(f"توضیحات [{row[5]}]: ") or row[5]
                prod.description = str(desc)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        cursor.execute("""
                       UPDATE products
                       SET name=%s,
                           price=%s,
                           stock=%s,
                           category=%s,
                           brand=%s,
                           description=%s
                       WHERE product_id = %s
                       """,
                       (prod.name, prod.price, prod.stock, prod.category, prod.brand, prod.description, product_id))

        db.commit()
        print(Fore.GREEN + "اطلاعات محصول با موفقیت ویرایش شد!")

    else:
        print(Fore.YELLOW + "محصولی پیدا نشد.")

    db.close()
def edit_mobile():
    view_all_products()
    product_id = input(Fore.CYAN + "شناسه موبایل را وارد کنید: ")
    db = get_db_connection(database='my_shop')
    cursor = db.cursor()

    cursor.execute("SELECT screen_size, ram, storage, battery, camera FROM mobiles WHERE product_id = %s",
                   (product_id,))
    row = cursor.fetchone()

    if row:
        mob = Mobile()

        while True:
            try:
                screen = input(f"سایز صفحه [{row[0]}]: ") or row[0]
                mob.screen_size = float(screen)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                ram = input(f"رم [{row[1]}]: ") or row[1]
                mob.ram = int(ram)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                storage = input(f"حافظه [{row[2]}]: ") or row[2]
                mob.storage = int(storage)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                battery = input(f"باتری [{row[3]}]: ") or row[3]
                mob.battery = int(battery)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                camera = input(f"دوربین [{row[4]}]: ") or row[4]
                mob.camera = float(camera)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        cursor.execute("""
                       UPDATE mobiles
                       SET screen_size=%s,
                           ram=%s,
                           storage=%s,
                           battery=%s,
                           camera=%s
                       WHERE product_id = %s
                       """, (mob.screen_size, mob.ram, mob.storage, mob.battery, mob.camera, product_id))
        db.commit()
        print(Fore.GREEN + "مشخصات موبایل ویرایش شد!")

    else:
        print(Fore.YELLOW + "موبایلی پیدا نشد.")

    db.close()
def edit_laptop():
    view_all_products()
    product_id = input(Fore.CYAN + "شناسه لپ‌تاپ را وارد کنید: ")
    db = get_db_connection(database='my_shop')
    cursor = db.cursor()

    cursor.execute("SELECT screen_size, ram, storage, processor, gpu FROM laptops WHERE product_id = %s", (product_id,))
    row = cursor.fetchone()

    if row:
        lap = Laptop()

        while True:
            try:
                screen = input(f"سایز صفحه [{row[0]}]: ") or row[0]
                lap.screen_size = float(screen)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                ram = input(f"رم [{row[1]}]: ") or row[1]
                lap.ram = int(ram)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                storage = input(f"حافظه [{row[2]}]: ") or row[2]
                lap.storage = int(storage)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                cpu = input(f"پردازنده [{row[3]}]: ") or row[3]
                lap.processor = str(cpu)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        while True:
            try:
                gpu = input(f"گرافیک [{row[4]}]: ") or row[4]
                lap.gpu = str(gpu)
                break
            except ValueError as e:
                print(Fore.RED + f"خطا: {e}")

        cursor.execute("""
                       UPDATE laptops
                       SET screen_size=%s,
                           ram=%s,
                           storage=%s,
                           processor=%s,
                           gpu=%s
                       WHERE product_id = %s
                       """, (lap.screen_size, lap.ram, lap.storage, lap.processor, lap.gpu, product_id))
        db.commit()
        print(Fore.GREEN + "مشخصات لپ‌تاپ ویرایش شد!")

    else:
        print(Fore.YELLOW + "لپ‌تاپی پیدا نشد.")

    db.close()

#تابع حذف کردن محصولات
def delete_product():
    print(Fore.CYAN + "\n=== حذف محصول ===" + Fore.RESET)
    view_all_products()
    product_id = int(input("شناسه محصول: "))

    try:
        connection = get_db_connection(database='my_shop')
        cursor = connection.cursor()

        query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))

        connection.commit()
        cursor.close()
        connection.close()

        print(Fore.GREEN + "محصول با موفقیت حذف شد" + Fore.RESET)

    except Exception as e:
        print(Fore.RED + f"خطا در حذف محصول: {e}" + Fore.RESET)

# تابع اضافه کردن محصول به سبد خرید
def buy_product(user_id):
    print(Fore.CYAN + "\n=== خرید محصول ===" + Fore.RESET)
    view_all_products()

    try:
        product_id = int(input("شناسه محصول: "))
        quantity = int(input("تعداد: "))

        if quantity <= 0:
            print(Fore.RED + "تعداد باید بیشتر از صفر باشد" + Fore.RESET)
            return

        connection = get_db_connection(database='my_shop')
        cursor = connection.cursor()

        cursor.execute("SELECT name, price, stock FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            print(Fore.RED + "محصول یافت نشد" + Fore.RESET)
            cursor.close()
            connection.close()
            return

        product_name = product[0]
        price = product[1]
        stock = product[2]

        if stock < quantity:
            print(Fore.RED + f"موجودی کافی نیست. موجودی فعلی: {stock}" + Fore.RESET)
            cursor.close()
            connection.close()
            return

        cursor.execute("SELECT cart_id, quantity FROM cart WHERE user_id = %s AND product_id = %s",
                       (user_id, product_id))
        existing_cart = cursor.fetchone()

        if existing_cart:
            new_quantity = existing_cart[1] + quantity
            if new_quantity > stock:
                print(Fore.RED + f"موجودی کافی نیست. موجودی فعلی: {stock}" + Fore.RESET)
                cursor.close()
                connection.close()
                return

            query = "UPDATE cart SET quantity = %s WHERE cart_id = %s"
            cursor.execute(query, (new_quantity, existing_cart[0]))
            print(Fore.GREEN + "تعداد محصول در سبد خرید به‌روزرسانی شد" + Fore.RESET)
        else:
            query = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, product_id, quantity))
            print(Fore.GREEN + "محصول به سبد خرید اضافه شد" + Fore.RESET)

        connection.commit()
        cursor.close()
        connection.close()

    except ValueError:
        print(Fore.RED + "لطفا عدد معتبر وارد کنید" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"خطا: {e}" + Fore.RESET)
#تابع سبد خرید مشتری
def view_cart(user_id):
    print(Fore.CYAN + "\n=== سبد خرید ===" + Fore.RESET)

    try:
        connection = get_db_connection(database='my_shop')

        cursor = connection.cursor()

        query = """
                SELECT c.cart_id, c.product_id, p.name, c.quantity, p.price
                FROM cart c
                         JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = %s \
                """
        cursor.execute(query, (user_id,))
        cart_items = cursor.fetchall()

        if cart_items:
            print(f"\n{'شناسه':<10} {'نام محصول':<25} {'تعداد':<10} {'قیمت واحد':<15} {'جمع':<15}")
            print("-" * 80)

            total_price = 0
            for item in cart_items:
                cart_id = item[0]
                product_name = item[2]
                quantity = item[3]
                price = item[4]
                item_total = quantity * price
                total_price = total_price + item_total
                print(f"{cart_id:<10} {product_name:<25} {quantity:<10} {price:<15} {item_total:<15}")

            print("-" * 80)
            print(f"{'جمع کل:':<55} {total_price:<15}")

            print("\nآیا می‌خواهید آیتمی را حذف کنید؟ (y/n)")
            choice = input().lower()
            if choice == 'y':
                cart_id = int(input("شناسه آیتم برای حذف: "))
                delete_query = "DELETE FROM cart WHERE cart_id = %s AND user_id = %s"
                cursor.execute(delete_query, (cart_id, user_id))
                connection.commit()
                print(Fore.GREEN + "آیتم از سبد خرید حذف شد" + Fore.RESET)
        else:
            print(Fore.YELLOW + "سبد خرید شما خالی است" + Fore.RESET)

        cursor.close()
        connection.close()

    except ValueError:
        print(Fore.RED + "لطفا عدد معتبر وارد کنید" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"خطا: {e}" + Fore.RESET)





