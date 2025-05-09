import os
import sqlite3
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

dir_path = Path(__file__).parent

grocery_db = dir_path/'grocery.db'

grocery_db.touch(exist_ok=True)

class GroceryDB:
    """Create the necessary schema to hold the data"""

    def __init__(self):
        self.conn = sqlite3.connect(grocery_db)
        self.cursor = self.conn.cursor()
        self.tables = [
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL UNIQUE,
                contact TEXT NOT NULL    
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id INTEGER NOT NULL,
                category_name TEXT NOT NULL,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )""",
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
            """,
             """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            """
            ]
        
        for table in self.tables:
            self.cursor.execute(table)
        self.conn.commit()
        logging.info(f"Success: {len(self.tables)} tables have been added to the grocery database")

class Admin:
    """Manages admin related functions for now it will just add but the idea is to have"""

    def __init__(self):
        self.actions = ['suppliers', 'categories', 'products']

    def selected_key(self):
        """Gives the key to be executed"""
        for idx, key in enumerate(self.actions, start=1):
            logging.info(f" {idx}. {key}")
        while True:
            key = input(f"Enter a number between 1 and {len(self.actions)}\nEnter ('q') to terminate: ").strip()
            
            if key == 'q':
                logging.info("Exiting the program:")
                return None
            if not key:
                logging.warning("The Key can't be blank")
                continue

            if not key.isdigit():
                logging.warning(f"{key} is not an integer,  the key has to be an integer")
                continue
            key = int(key)
            if key > len(self.actions):
                logging.warning(f"Error: '{key}' is out of range")
                continue
            
            return int(key) - 1

class AdminAction:
    """Pushing admin related action"""

    def __init__(self):
        self.key = Admin().selected_key()
        self.act = Admin().actions[self.key]

        self.value_prompts = {
            'suppliers':{'name': 'Name of supplier: ',
                         'contact': 'Email address of the supplier: '},
            'categories': {'category': 'Category name: '},
            'products': {'name': 'Product name: ',
                         'quantity': 'Quantity: ',
                         'price': 'Price: '}
        }

        self.full_details = {key: {prompt_key: None for prompt_key in self.value_prompts[key]} for  key in self.value_prompts
                            }
        
        

    def collect_data(self):
        """Prompts user for inputs dynamically"""
        logging.info(f"We shall be performing an action on {self.act}")

        for key, prompts in self.value_prompts[self.act].items():
            self.full_details[self.act][key] = input(prompts).strip()
        return self.full_details[self.act]




print(AdminAction().collect_data())