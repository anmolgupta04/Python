import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

INVENTORY_FILE = "inventory.json"

# --- Helper Functions ---

def load_inventory():
    """Load data from JSON file."""
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_inventory(inventory):
    """Save data to JSON file."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)

# --- GUI Application Class ---

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("750x500")
        self.root.resizable(False, False)

        self.inventory = load_inventory()

        # --- GUI Layout ---

        title = tk.Label(root, text="Inventory Management System", font=("Arial", 20, "bold"), fg="white", bg="#333")
        title.pack(fill=tk.X)

        form_frame = tk.Frame(root, padx=20, pady=10)
        form_frame.pack(fill=tk.X)

        tk.Label(form_frame, text="Item ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Price:").grid(row=1, column=2, padx=5, pady=5)

        self.id_entry = tk.Entry(form_frame)
        self.name_entry = tk.Entry(form_frame)
        self.qty_entry = tk.Entry(form_frame)
        self.price_entry = tk.Entry(form_frame)

        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        self.qty_entry.grid(row=1, column=1, padx=5, pady=5)
        self.price_entry.grid(row=1, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(root, pady=10)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Add", width=10, bg="#4CAF50", fg="white", command=self.add_item).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Update", width=10, bg="#2196F3", fg="white", command=self.update_item).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete", width=10, bg="#f44336", fg="white", command=self.delete_item).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear", width=10, bg="#9E9E9E", fg="white", command=self.clear_fields).pack(side=tk.LEFT, padx=10)

        # --- Inventory Table ---
        self.tree = ttk.Treeview(root, columns=("id", "name", "qty", "price"), show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("price", text="Price")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="center")
        self.tree.column("qty", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="center")

        self.tree.pack(fill=tk.BOTH, padx=20, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.select_item)

        self.refresh_table()

    # --- Functional Methods ---

    def refresh_table(self):
        """Refresh the inventory table."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item_id, item in self.inventory.items():
            self.tree.insert("", "end", values=(item_id, item["name"], item["quantity"], item["price"]))

    def clear_fields(self):
        """Clear input fields."""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def add_item(self):
        """Add a new item."""
        item_id = self.id_entry.get()
        name = self.name_entry.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get()

        if not (item_id and name and qty and price):
            messagebox.showerror("Error", "Please fill all fields!")
            return

        if item_id in self.inventory:
            messagebox.showerror("Error", "Item ID already exists!")
            return

        try:
            self.inventory[item_id] = {"name": name, "quantity": int(qty), "price": float(price)}
        except ValueError:
            messagebox.showerror("Error", "Quantity and Price must be numbers!")
            return

        save_inventory(self.inventory)
        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Item added successfully!")

    def select_item(self, event):
        """Select an item from table."""
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, values[2])
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, values[3])

    def update_item(self):
        """Update selected item."""
        item_id = self.id_entry.get()
        if item_id not in self.inventory:
            messagebox.showerror("Error", "Item not found!")
            return

        name = self.name_entry.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get()

        try:
            self.inventory[item_id] = {"name": name, "quantity": int(qty), "price": float(price)}
        except ValueError:
            messagebox.showerror("Error", "Quantity and Price must be numbers!")
            return

        save_inventory(self.inventory)
        self.refresh_table()
        messagebox.showinfo("Success", "Item updated successfully!")

    def delete_item(self):
        """Delete selected item."""
        item_id = self.id_entry.get()
        if item_id not in self.inventory:
            messagebox.showerror("Error", "Item not found!")
            return

        del self.inventory[item_id]
        save_inventory(self.inventory)
        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Deleted", "Item deleted successfully!")

# --- Main Execution ---

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
