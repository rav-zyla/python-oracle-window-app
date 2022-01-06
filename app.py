from tkinter import Tk, StringVar, Label, Entry, Listbox, Button, END, W, messagebox
import re

from database import Database

selected_item = None


class AppGUI:
    def __init__(self, app: Tk, db: Database):
        self.app = app
        self.db = db

        # Start program
        self.app.title("Database")
        self.app.geometry("700x400")
        self.app.resizable(False, False)

        # Part
        self.part_text = StringVar()
        self.part_label = Label(app, text='Part name', font=('bold', 15))
        self.part_label.grid(row=0, column=0, sticky=W, padx=10, pady=5)
        self.part_entry = Entry(app, textvariable=self.part_text)
        self.part_entry.grid(row=0, column=1)

        # Customer
        self.customer_text = StringVar()
        self.customer_label = Label(app, text='Customer', font=('bold', 15))
        self.customer_label.grid(row=0, column=2, sticky=W, padx=10, pady=5)
        self.customer_entry = Entry(app, textvariable=self.customer_text)
        self.customer_entry.grid(row=0, column=3)

        # Retail
        self.retailer_text = StringVar()
        self.retailer_label = Label(app, text='Retailer', font=('bold', 15))
        self.retailer_label.grid(row=1, column=0, sticky=W, padx=10, pady=5)
        self.retailer_entry = Entry(app, textvariable=self.retailer_text)
        self.retailer_entry.grid(row=1, column=1)

        # Price
        self.price_text = StringVar()
        self.price_label = Label(app, text='Price', font=('bold', 15))
        self.price_label.grid(row=1, column=2, sticky=W, padx=10, pady=5)
        self.price_entry = Entry(app, textvariable=self.price_text)
        self.price_entry.grid(row=1, column=3)

        # Parts list (Listbox)
        self.parts_list = Listbox(app, height=10, width=60, border=2)
        self.parts_list.grid(row=3, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

        # Bind select
        self.parts_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_btn = Button(app, text='Add part', width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = Button(app, text='Remove part', width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1, pady=20)

        self.update_btn = Button(app, text='Update part', width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2, pady=20)

        self.clear_btn = Button(app, text='Clear input', width=12, command=self.clear_text)
        self.clear_btn.grid(row=2, column=3, pady=20)

        self.default_sort_btn = Button(app, text='Default sort', width=14, command=self.populate_list)
        self.default_sort_btn.grid(row=10, column=0, pady=20)

        self.sort_by_price_asc_btn = Button(app, text='Sort by price ASC', width=14, command=self.sort_by_price_asc)
        self.sort_by_price_asc_btn.grid(row=10, column=1, pady=20)

        self.sort_by_price_desc_btn = Button(app, text='Sort by price DESC', width=14, command=self.sort_by_price_desc)
        self.sort_by_price_desc_btn.grid(row=10, column=2, pady=20)

        # Populate
        self.populate_list()

    def populate_list(self):
        self.parts_list.delete(0, END)
        for row in self.db.fetch_all(table='parts'):
            self.parts_list.insert(END, row)

    def sort_by_price_asc(self):
        self.parts_list.delete(0, END)
        for row in self.db.fetch_all(table='parts', additional='ORDER BY price'):
            self.parts_list.insert(END, row)

    def sort_by_price_desc(self):
        self.parts_list.delete(0, END)
        for row in self.db.fetch_all(table='parts', additional='ORDER BY price DESC'):
            self.parts_list.insert(END, row)

    def add_item(self):
        part = self.part_text.get()
        customer = self.customer_text.get()
        retailer = self.retailer_text.get()
        price = self.price_text.get()
        if '' or None in (part, customer, retailer, price):
            messagebox.showerror('Required fields', 'Pleas include all fields')
            return

        if not re.match(r'^[1-9][0-9]*.?[0-9]{,2}$', price):
            messagebox.showinfo('Warning!', 'Please include correct price!')
            return

        self.db.insert(table='parts', values=(None, part, customer, retailer, float(price)))
        self.parts_list.delete(0, END)
        self.parts_list.insert(END, (part, customer, retailer, price))
        self.clear_text()
        self.populate_list()

    def select_item(self, event):
        try:
            global selected_item
            index = self.parts_list.curselection()[0]
            selected_item = self.parts_list.get(index)

            self.clear_text()

            self.part_entry.insert(END, selected_item[1])
            self.customer_entry.insert(END, selected_item[2])
            self.retailer_entry.insert(END, selected_item[3])
            self.price_entry.insert(END, selected_item[4])
        except IndexError:
            pass

    def remove_item(self):
        self.db.remove(table='parts', additional=f"id={selected_item[0]}")
        self.clear_text()
        self.populate_list()

    def update_item(self):
        part = self.part_text.get()
        customer = self.customer_text.get()
        retailer = self.retailer_text.get()
        price = self.price_text.get()
        self.db.update(table='parts',
                       additional=f"part='{part}', customer='{customer}', retailer='{retailer}', price='{price}'"
                                  f" WHERE id={selected_item[0]}")
        self.populate_list()

    def clear_text(self):
        self.part_entry.delete(0, END)
        self.customer_entry.delete(0, END)
        self.retailer_entry.delete(0, END)
        self.price_entry.delete(0, END)

    def run(self):
        self.app.mainloop()
