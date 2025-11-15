import json
import os
from typing import List
import csv

from models import Item

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
STORAGE_PATH = os.path.join(os.path.dirname(__file__), "storage.json")


class DatabaseManager:
    def __init__(self):
        self.use_json = True
        self.conn = None
        self.cursor = None
        self.config = self._load_config()
        try:
            import mysql.connector
            cfg = self.config
            self.conn = mysql.connector.connect(
                host=cfg.get("host"),
                user=cfg.get("user"),
                password=cfg.get("password"),
                database=cfg.get("database"),
            )
            self.cursor = self.conn.cursor(dictionary=True)
            self.use_json = False
            self._ensure_table()
        except Exception:
            # fallback to JSON file
            self.use_json = True

    def _load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _ensure_table(self):
        q = (
            "CREATE TABLE IF NOT EXISTS items ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "name VARCHAR(255),"
            "description VARCHAR(512),"
            "quantity INT,"
            "price DOUBLE"
            ")"
        )
        self.cursor.execute(q)
        self.conn.commit()

    # JSON helpers
    def _read_json(self):
        try:
            with open(STORAGE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"items": []}

    def _write_json(self, data):
        with open(STORAGE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # CRUD
    def add_item(self, item: Item) -> Item:
        if not self.use_json:
            q = "INSERT INTO items (name, description, quantity, price) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(q, (item.name, item.description, item.quantity, item.price))
            self.conn.commit()
            item.id = self.cursor.lastrowid
            return item
        else:
            data = self._read_json()
            items = data.get("items", [])
            new_id = max([i.get("id", 0) for i in items] + [0]) + 1
            new = {"id": new_id, "name": item.name, "description": item.description, "quantity": item.quantity, "price": item.price}
            items.append(new)
            data["items"] = items
            self._write_json(data)
            item.id = new_id
            return item

    def update_item(self, item: Item) -> bool:
        if not self.use_json:
            q = "UPDATE items SET name=%s, description=%s, quantity=%s, price=%s WHERE id=%s"
            self.cursor.execute(q, (item.name, item.description, item.quantity, item.price, item.id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        else:
            data = self._read_json()
            items = data.get("items", [])
            for i in items:
                if i.get("id") == item.id:
                    i["name"] = item.name
                    i["description"] = item.description
                    i["quantity"] = item.quantity
                    i["price"] = item.price
                    self._write_json(data)
                    return True
            return False

    def delete_item(self, item_id: int) -> bool:
        if not self.use_json:
            q = "DELETE FROM items WHERE id=%s"
            self.cursor.execute(q, (item_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        else:
            data = self._read_json()
            items = data.get("items", [])
            new_items = [i for i in items if i.get("id") != item_id]
            if len(new_items) == len(items):
                return False
            data["items"] = new_items
            self._write_json(data)
            return True

    def get_all_items(self) -> List[Item]:
        if not self.use_json:
            q = "SELECT id, name, description, quantity, price FROM items ORDER BY id DESC"
            self.cursor.execute(q)
            rows = self.cursor.fetchall()
            return [Item(id=r["id"], name=r["name"], description=r.get("description", ""), quantity=r["quantity"], price=r["price"]) for r in rows]
        else:
            data = self._read_json()
            return [Item(id=i.get("id"), name=i.get("name"), description=i.get("description", ""), quantity=i.get("quantity", 0), price=i.get("price", 0.0)) for i in data.get("items", [])]

    def search_items(self, term: str) -> List[Item]:
        if not self.use_json:
            q = "SELECT id, name, description, quantity, price FROM items WHERE name LIKE %s OR description LIKE %s"
            like = f"%{term}%"
            self.cursor.execute(q, (like, like))
            rows = self.cursor.fetchall()
            return [Item(id=r["id"], name=r["name"], description=r.get("description", ""), quantity=r["quantity"], price=r["price"]) for r in rows]
        else:
            data = self._read_json()
            found = [i for i in data.get("items", []) if term.lower() in i.get("name", "").lower() or term.lower() in i.get("description", "").lower()]
            return [Item(id=i.get("id"), name=i.get("name"), description=i.get("description", ""), quantity=i.get("quantity", 0), price=i.get("price", 0.0)) for i in found]

    def export_json(self, out_path: str):
        items = [it.to_dict() for it in self.get_all_items()]
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"items": items}, f, indent=2, ensure_ascii=False)

    def export_excel(self, out_path: str):
        try:
            from openpyxl import Workbook
        except Exception:
            raise
        wb = Workbook()
        ws = wb.active
        ws.title = "Items"
        ws.append(["id", "name", "description", "quantity", "price"])
        for it in self.get_all_items():
            ws.append([it.id, it.name, it.description, it.quantity, it.price])
        wb.save(out_path)

    def export_csv(self, out_path: str):
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "description", "quantity", "price"])
            for it in self.get_all_items():
                writer.writerow([it.id, it.name, it.description, it.quantity, it.price])

    def import_csv(self, in_path: str):
        with open(in_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name") or row.get("Name")
                if not name:
                    continue
                description = row.get("description") or row.get("Description") or ""
                try:
                    quantity = int(row.get("quantity") or row.get("Quantity") or 0)
                except Exception:
                    quantity = 0
                try:
                    price = float(row.get("price") or row.get("Price") or 0.0)
                except Exception:
                    price = 0.0
                item = Item(id=None, name=name, description=description, quantity=quantity, price=price)
                self.add_item(item)

    def create_database(self) -> bool:
        """Try to create the configured MySQL database if the server is reachable."""
        try:
            import mysql.connector
            cfg = self.config
            conn = mysql.connector.connect(host=cfg.get("host"), user=cfg.get("user"), password=cfg.get("password"))
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{cfg.get('database')}`")
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception:
            return False
