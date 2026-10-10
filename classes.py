class User:
    def __init__(self):
        self._username = ""
        self._password = ""
        self._email = ""
        self._phone = ""

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("نام کاربری نمی‌تواند خالی باشد")
        if len(value) < 3:
            raise ValueError("نام کاربری باید حداقل 3 کاراکتر باشد")
        if len(value) > 30:
            raise ValueError("نام کاربری نباید بیشتر از 30 کاراکتر باشد")
        if not value.replace('_', '').replace('.', '').isalnum():
            raise ValueError("نام کاربری فقط می‌تواند شامل حروف، اعداد، _ و . باشد")
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("رمز عبور نمی‌تواند خالی باشد")
        if len(value) < 6:
            raise ValueError("رمز عبور باید حداقل 6 کاراکتر باشد")
        if len(value) > 100:
            raise ValueError("رمز عبور نباید بیشتر از 100 کاراکتر باشد")
        if not any(c.isdigit() for c in value):
            raise ValueError("رمز عبور باید حداقل یک عدد داشته باشد")
        if not any(c.isalpha() for c in value):
            raise ValueError("رمز عبور باید حداقل یک حرف داشته باشد")
        self._password = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("ایمیل نمی‌تواند خالی باشد")
        if "@" not in value or "." not in value:
            raise ValueError("فرمت ایمیل نامعتبر است")
        if value.count("@") != 1:
            raise ValueError("ایمیل باید فقط یک @ داشته باشد")
        local, domain = value.split("@")
        if len(local) == 0 or len(domain) == 0:
            raise ValueError("ایمیل نامعتبر است")
        if "." not in domain:
            raise ValueError("دامنه ایمیل باید شامل . باشد")
        if len(value) > 100:
            raise ValueError("ایمیل نباید بیشتر از 100 کاراکتر باشد")
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("شماره تلفن نمی‌تواند خالی باشد")
        cleaned = value.replace(" ", "").replace("-", "")
        if not cleaned.isdigit():
            raise ValueError("شماره تلفن فقط باید شامل اعداد باشد")
        if len(cleaned) != 11:
            raise ValueError("شماره تلفن باید 11 رقم باشد")
        if not cleaned.startswith("09"):
            raise ValueError("شماره تلفن باید با 09 شروع شود")
        self._phone = cleaned

class Product:
    def __init__(self):
        self._name = ""
        self._price = 0
        self._stock = 0
        self._category = ""
        self._brand = ""
        self._description = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("نام محصول نباید خالی باشد و باید حداقل ۲ کاراکتر باشد.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("قیمت محصول باید بیشتر از صفر باشد.")
        self._price = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("موجودی محصول نمی‌تواند منفی باشد.")
        self._stock = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

class Mobile(Product):
    def __init__(self):
        super().__init__()
        self.category = "موبایل"
        self._screen_size = 0.0
        self._ram = 0
        self._storage = 0
        self._battery = 0
        self._camera = 0

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self._screen_size = value
        else:
            raise ValueError("Screen size must be a positive number.")

    @property
    def ram(self):
        return self._ram

    @ram.setter
    def ram(self, value):
        if isinstance(value, int) and value > 0:
            self._ram = value
        else:
            raise ValueError("RAM must be a positive integer.")

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        if isinstance(value, int) and value > 0:
            self._storage = value
        else:
            raise ValueError("Storage must be a positive integer.")

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if isinstance(value, int) and value > 0:
            self._battery = value
        else:
            raise ValueError("Battery capacity must be a positive integer.")

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self._camera = value
        else:
            raise ValueError("Camera resolution must be a positive number.")

class Laptop(Product):
    def __init__(self):
        super().__init__()
        self.category = "لپ‌تاپ"
        self._screen_size = 0.0
        self._ram = 0
        self._storage = 0
        self._processor = ""
        self._gpu = ""

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self._screen_size = value
        else:
            raise ValueError("Screen size must be a positive number.")

    @property
    def ram(self):
        return self._ram

    @ram.setter
    def ram(self, value):
        if isinstance(value, int) and value > 0:
            self._ram = value
        else:
            raise ValueError("RAM must be a positive integer.")

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        if isinstance(value, int) and value > 0:
            self._storage = value
        else:
            raise ValueError("Storage must be a positive integer.")

    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._processor = value.strip()
        else:
            raise ValueError("Processor cannot be empty.")

    @property
    def gpu(self):
        return self._gpu

    @gpu.setter
    def gpu(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._gpu = value.strip()
        else:
            raise ValueError("GPU cannot be empty.")
        
# class CartItem:
#     def __init__(self):
#         self._product_id = ""
#         self._product_name = ""
#         self._quantity = 0
#         self._price = 0.0
#
#     @property
#     def product_id(self):
#         return self._product_id
#
#     @product_id.setter
#     def product_id(self, value):
#         self._product_id = value
#
#     @property
#     def product_name(self):
#         return self._product_name
#
#     @product_name.setter
#     def product_name(self, value):
#         self._product_name = value
#
#     @property
#     def quantity(self):
#         return self._quantity
#
#     @quantity.setter
#     def quantity(self, value):
#         self._quantity = value
#
#     @property
#     def price(self):
#         return self._price
#
#     @price.setter
#     def price(self, value):
#         self._price = value
#
#     def get_total_price(self):
#         return self._quantity * self._price
class Seller:
    def __init__(self):
        self._id = 0
        self._username = ""
        self._password = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("شناسه (id) باید یک عدد صحیح و بزرگتر از صفر باشد.")
        self._id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise ValueError("نام کاربری (username) باید رشته‌ای با حداقل ۳ کاراکتر باشد.")
        self._username = value.strip()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) or len(value) < 6:
            raise ValueError("رمز عبور (password) باید حداقل شامل ۶ کاراکتر باشد.")
        self._password = value

class Admin:
    def __init__(self):
        self._id = 0
        self._username = ""
        self._password = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("شناسه (id) باید یک عدد صحیح مثبت باشد.")
        self._id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise ValueError("نام کاربری باید حداقل ۳ کاراکتر باشد.")
        self._username = value.strip()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) or len(value) < 8:
            raise ValueError("رمز عبور مدیر باید حداقل ۸ کاراکتر باشد.")
        self._password = value
