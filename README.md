#  Console-based Electronics Store System

A robust, object-oriented console-based e-commerce platform built with **Python** and **MySQL**. It simulates an electronics shop (Laptops, Mobiles, and General Products) supporting multi-role access control, data validation, and database persistence.

---

##  Features

- **Role-Based Access Control (RBAC):**
  - **Customer:** Register, login, browse categories, add/remove items to/from shopping cart.
  - **Seller:** Add new products (General, Mobile, Laptop), edit prices/stock, delete items, and view inventory.
  - **Admin:** Manage users, delete spam accounts, register new administrators.
- **Object-Oriented Design (OOP):**
  - Clear domain models with inheritance (`Product` -> `Mobile`, `Laptop`).
  - Robust property validation for emails, phone numbers, and prices.
- **Security & Data Integrity:**
  - Password hashing (SHA-256) for privileged accounts.
  - Relational schema with foreign keys connecting products, carts, and user profiles.
- **Relational Database:** Fully persistent storage via MySQL (`mysql-connector-python`).

---

##  Project Structure
```text
├── main.py          # Entry point & interactive CLI menus
├── functions.py     # Business logic & database operations
├── classes.py       # Data models, OOP entities & validation
└── data_base.py     # Database schema, table migrations & connection
