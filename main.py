from colorama import init, Fore
from functions import *
from data_base import *

def main():
    db_conn = get_db_connection()
    if db_conn is None:
        print(Fore.RED + "خطا: اتصال به دیتابیس برقرار نشد. برنامه متوقف می‌شود." + Fore.RESET)
        return

    try:
        while True:
            print(Fore.MAGENTA + "\n=== فروشگاه لوازم الکترونیکی سپهر ===" + Fore.RESET)
            print("1. ثبت نام کاربر")
            print("2. ورود کاربر")
            print("3. بخش فروشندگان")
            print("4. بخش ادمین ها")
            print("5. خروج")

            choice = input("انتخاب کنید: ")

            if choice == "1":
                register_user()

            elif choice == "2":
                user_id = login_user()
                if user_id:
                    user_menu(user_id)

            elif choice == "3":
                while True:
                    print(Fore.CYAN + "\n=== بخش فروشندگان ===" + Fore.RESET)
                    print("1. ثبت‌ نام فروشنده جدید")
                    print("2. ورود به حساب کاربری")
                    print("3. بازگشت به منوی اصلی")

                    seller_choice = input("انتخاب شما: ")

                    if seller_choice == "1":
                        print(Fore.CYAN + "\n--- ثبت‌نام فروشنده ---" + Fore.RESET)
                        username = input("نام کاربری دلخواه: ")
                        password = input("رمز عبور: ")

                        seller = register_seller(username, password, db_conn)

                        if seller:
                            print(Fore.GREEN + "ثبت‌نام موفقیت‌آمیز بود! اکنون می‌توانید وارد شوید." + Fore.RESET)

                    elif seller_choice == "2":
                        print(Fore.CYAN + "\n--- ورود فروشنده ---" + Fore.RESET)
                        username = input("نام کاربری فروشنده: ")
                        password = input("رمز عبور: ")

                        if login_seller(username, password, db_conn):
                            seller_menu()
                            break

                    elif seller_choice == "3":
                        break

                    else:
                        print(Fore.RED + "گزینه نامعتبر است. دوباره تلاش کنید." + Fore.RESET)

            elif choice == "4":
                while True:
                    print(Fore.CYAN + "\n=== بخش ادمین ها ===" + Fore.RESET)
                    print("1. ورود به حساب کاربری")
                    print("2. بازگشت به منوی اصلی")

                    admin_choice = input("انتخاب شما: ")

                    if admin_choice == "1":
                        print(Fore.CYAN + "\n--- ورود ادمین ---" + Fore.RESET)
                        username = input("نام کاربری ادمین: ")
                        password = input("رمز عبور: ")

                        if login_admin(username, password, db_conn):
                            admin_menu(db_conn)


                    elif admin_choice == "2":
                        break

                    else:
                        print(Fore.RED + "گزینه نامعتبر است. دوباره تلاش کنید." + Fore.RESET)

            elif choice == "5":
                print(Fore.GREEN + "خداحافظ!" + Fore.RESET)
                break

            else:
                print(Fore.RED + "گزینه اشتباه است" + Fore.RESET)

    finally:
        if db_conn and db_conn.is_connected():
            db_conn.close()
            print(Fore.GREEN + "اتصال به دیتابیس بسته شد." + Fore.RESET)
#منو کاربر
def user_menu(user_id):
    while True:
        print(Fore.YELLOW + "\n=== منوی کاربر ===" + Fore.RESET)
        print("1. مشاهده محصولات")
        print("2. خرید محصول")
        print("3. مشاهده سبد خرید")
        print("4. خروج")

        choice = input("انتخاب کنید: ")

        if choice == "1":
            view_products()
        elif choice == "2":
            buy_product(user_id)
        elif choice == "3":
            view_cart(user_id)
        elif choice == "4":
            print(Fore.GREEN + "خروج از حساب کاربری" + Fore.RESET)
            break
        else:
            print(Fore.RED + "گزینه اشتباه است " + Fore.RESET)

#منو فروشنده
def seller_menu():
    while True:
        print(Fore.YELLOW + "\n=== منوی فروشنده ===" + Fore.RESET)
        print("1. افزودن محصول")
        print("2. مشاهده محصولات")
        print("3. ویرایش محصول")
        print("4. حذف محصول")
        print("5. خروج")

        choice = input("انتخاب کنید: ")

        if choice == "1":
            add_product_menu()
        elif choice == "2":
            view_products()
        elif choice == "3":
            edit_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            print(Fore.GREEN + "خروج از پنل فروشنده" + Fore.RESET)
            break
        else:
            print(Fore.RED + "گزینه نامعتبر" + Fore.RESET)

#منو ادمین
def admin_menu(db_conn):
    while True:
        print(Fore.MAGENTA + "\n=== داشبورد مدیریت ادمین ===" + Fore.RESET)
        print("1. حذف کاربر ")
        print("2. حذف فروشنده")
        print("3. ثبت‌ نام ادمین جدید")
        print("4. خروج از حساب ادمین")

        choice = input("انتخاب شما: ")

        if choice == "1":
            admin_delete_user(db_conn)
        elif choice == "2":
            admin_delete_seller(db_conn)

        elif choice == "3":
                print(Fore.CYAN + "\n--- ثبت‌نام ادمین ---" + Fore.RESET)
                username = input("نام کاربری دلخواه: ")
                password = input("رمز عبور: ")
                register_admin(username, password, db_conn)

        elif choice == "4":
            main()
        else:
            print(Fore.RED + "گزینه نامعتبر است. دوباره تلاش کنید." + Fore.RESET)

def edit_product():
    while True:
        print(Fore.BLUE + Style.BRIGHT + "\n--- منوی ویرایش ---")
        print("1. محصول کلی")
        print("2. موبایل")
        print("3. لپ‌تاپ")
        print(Fore.RED + "4. خروج")

        choice = input(Fore.CYAN + "انتخاب شما: ")

        if choice == '1':
            edit_general_product()
        elif choice == '2':
            edit_mobile()
        elif choice == '3':
            edit_laptop()
        elif choice == '4':
            break
        else:
            print(Fore.RED + "اشتباه وارد کردید.")


if __name__ == "__main__":
    main()
