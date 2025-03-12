import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import re

class LegoTrackerApp:
    DATA_FILE = "lego_speed_champions.json"
    FIELDS = ["Brand", "Name", "Product Number", "Piece Count", "Release Date", "Price", "Notes", "Width", "Car Count", "URL"]
    FILTER_OPTIONS = ["Brand", "Width", "Release Date", "Piece Count", "Car Count", "Owned"]

    def __init__(self, root):
        self.root = root
        self.root.title("Lego Speed Champions Tracker")
        self.root.geometry("750x600")  # Increase height for statistics
        
        self.lego_data = self.load_data()
        self.filtered_data = self.lego_data  # Store filtered data
        self.selected_index = None  # Store the index of the selected entry
        
        self.filter_own_var = tk.BooleanVar()  # Initialize filter_own_var
        self.create_widgets()
        self.populate_listbox()
        self.update_statistics()  # Display initial statistics
    
    def load_data(self):
        # Load data from JSON file
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    for item in data:
                        item["Price"] = self.extract_euro_price(item["Price"])
                        item["Release Date"] = item["Release Date"].split(".")[1]  # Extract year from release date
                    return data
                except json.JSONDecodeError:
                    return []
        return []

    def extract_euro_price(self, price_str):
        # Extract euro price from string
        match = re.search(r'€\d+(\.\d{2})?', price_str)
        return match.group(0) if match else price_str

    def create_widgets(self):
        # Create all the widgets
        self.create_input_frame()
        self.create_listbox_frame()
        self.create_filter_frame()
        self.create_statistics_frame()

    def create_input_frame(self):
        # Create input frame for data entry
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.Y)
        
        self.entries = {}
        for idx, field in enumerate(self.FIELDS):
            tk.Label(self.input_frame, text=field).grid(row=idx, column=0, sticky=tk.W, pady=2)
            entry = tk.Entry(self.input_frame, width=30)
            entry.grid(row=idx, column=1, pady=2, padx=5)
            self.entries[field] = entry
        
        tk.Label(self.input_frame, text="Owned").grid(row=len(self.FIELDS), column=0, sticky=tk.W, pady=2)
        self.own_var = tk.BooleanVar()
        self.own_checkbox = tk.Checkbutton(self.input_frame, variable=self.own_var)
        self.own_checkbox.grid(row=len(self.FIELDS), column=1, pady=2, padx=5)

    def create_listbox_frame(self):
        # Create listbox frame to display data
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(self.listbox_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.add_button = tk.Button(self.button_frame, text="Add/Edit", command=self.add_or_edit_entry)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_entry)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.clear_filter_button = tk.Button(self.button_frame, text="Clear Filter", command=self.clear_filter)
        self.clear_filter_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.show_pie_chart_button = tk.Button(self.button_frame, text="Show Pie Chart", command=self.show_pie_chart)
        self.show_pie_chart_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.listbox = tk.Listbox(self.listbox_frame, width=50, height=20)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.load_selected_entry)

    def create_filter_frame(self):
        # Create filter frame for filtering data
        self.filter_frame = tk.Frame(self.input_frame)
        self.filter_frame.grid(row=len(self.FIELDS) + 1, columnspan=2, pady=10)
        
        tk.Label(self.filter_frame, text="Filter by:").grid(row=0, column=0, sticky=tk.W)
        self.filter_option = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.filter_option, values=self.FILTER_OPTIONS, state="readonly")
        self.filter_dropdown.grid(row=0, column=1, padx=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", self.update_filter_field)
        
        self.filter_value_var = tk.StringVar()
        self.filter_entry = tk.Entry(self.filter_frame, width=20, textvariable=self.filter_value_var)
        self.filter_entry.grid(row=1, column=1, pady=5)
        
        self.brand_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.filter_value_var, state="readonly")
        self.brand_dropdown.grid(row=1, column=1, pady=5)
        self.brand_dropdown.grid_remove()
        
        self.year_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.filter_value_var, state="readonly")
        self.year_dropdown.grid(row=1, column=1, pady=5)
        self.year_dropdown.grid_remove()
        
        self.release_date_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.filter_value_var, state="readonly")
        self.release_date_dropdown.grid(row=1, column=1, pady=5)
        self.release_date_dropdown.grid_remove()
        
        self.filter_own_checkbox = tk.Checkbutton(self.filter_frame, text="Owned", variable=self.filter_own_var)
        self.filter_own_checkbox.grid(row=1, column=1, pady=5)
        self.filter_own_checkbox.grid_remove()
        
        self.piece_count_var = tk.StringVar()
        self.piece_count_entry = tk.Entry(self.filter_frame, width=20, textvariable=self.piece_count_var)
        self.piece_count_entry.grid(row=1, column=1, pady=5)
        self.piece_count_entry.grid_remove()
        
        self.piece_count_option = tk.StringVar()
        self.piece_count_option.set("higher")
        self.piece_count_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.piece_count_option, values=["higher", "lower"], state="readonly")
        self.piece_count_dropdown.grid(row=1, column=0, pady=5)
        self.piece_count_dropdown.grid_remove()
        
        self.width_var = tk.StringVar()
        self.width_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.width_var, values=[6, 8], state="readonly")
        self.width_dropdown.grid(row=1, column=1, pady=5)
        self.width_dropdown.grid_remove()
        
        self.car_count_var = tk.StringVar()
        self.car_count_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.car_count_var, state="readonly")
        self.car_count_dropdown.grid(row=1, column=1, pady=5)
        self.car_count_dropdown.grid_remove()
        
        self.apply_filter_button = tk.Button(self.filter_frame, text="Apply Filter", command=self.apply_filter)
        self.apply_filter_button.grid(row=2, column=0, pady=5)

    def create_statistics_frame(self):
        # Create statistics frame to display statistics
        self.stats_frame = tk.Frame(self.input_frame)
        self.stats_frame.grid(row=len(self.FIELDS) + 2, columnspan=2, pady=10)
        
        self.stats_label = tk.Label(self.stats_frame, text="", justify=tk.LEFT)
        self.stats_label.pack()
    
    def add_or_edit_entry(self):
        # Add or edit an entry
        new_entry = {}
        for field in self.FIELDS:
            value = self.entries[field].get().strip()
            if field in ["Piece Count", "Width", "Car Count"]:
                if not value.isdigit():
                    messagebox.showwarning("Invalid input", f"Please enter a valid number for {field}.")
                    return
            elif field == "Release Date":
                if not re.match(r'\d{2}\.\d{4}', value):
                    messagebox.showwarning("Invalid input", "Please enter a valid date in the format mm.yyyy.")
                    return
            elif field == "Price":
                if not re.match(r'€\d+(\.\d{2})?', value):
                    messagebox.showwarning("Invalid input", "Please enter a valid price in the format €xx.xx.")
                    return
            new_entry[field] = value
        new_entry["Owned"] = self.own_var.get()
        
        if self.selected_index is not None:
            self.lego_data[self.selected_index] = new_entry
            self.selected_index = None
        else:
            self.lego_data.append(new_entry)
        
        self.save_data()
        self.populate_listbox()
        self.update_statistics()  # Update statistics
    
    def delete_entry(self):
        # Delete an entry
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Delete not possible", "Please select an entry!")
            return
        
        selected_item = self.filtered_data[selected_index[0]]
        self.lego_data = [item for item in self.lego_data if item != selected_item]
        self.save_data()
        self.populate_listbox()
        self.update_statistics()  # Update statistics
    
    def save_data(self):
        # Save data to JSON file
        self.lego_data.sort(key=lambda x: x["Brand"])
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.lego_data, file, indent=4, ensure_ascii=False)
    
    def populate_listbox(self, filter_field=None, filter_value=None):
        # Populate listbox with data
        self.listbox.delete(0, tk.END)
        for item in self.filtered_data:
            own_status = "✅" if item.get("Owned", False) else "❌"
            self.listbox.insert(tk.END, f"{own_status} {item['Brand']} - {item['Name']} ({item['Product Number']})")
        self.update_statistics()  # Update statistics
    
    def load_selected_entry(self, event):
        # Load selected entry into input fields
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        self.selected_index = selected_index[0]
        selected_item = self.filtered_data[self.selected_index]
        for field in self.FIELDS:
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, selected_item[field])
        self.own_var.set(selected_item.get("Owned", False))
    
    def update_filter_field(self, event):
        # Update filter field based on selected filter option
        selected_field = self.filter_option.get()
        self.filter_entry.grid_remove()
        self.brand_dropdown.grid_remove()
        self.year_dropdown.grid_remove()
        self.release_date_dropdown.grid_remove()
        self.filter_own_checkbox.grid_remove()
        self.piece_count_entry.grid_remove()
        self.piece_count_dropdown.grid_remove()
        self.width_dropdown.grid_remove()
        self.car_count_dropdown.grid_remove()
        
        if selected_field == "Brand":
            self.brand_dropdown.grid()
            brands = list(set(item["Brand"] for item in self.lego_data))
            unique_brands = []
            for brand in brands:
                if brand not in unique_brands:
                    unique_brands.append(brand)
            unique_brands.sort()  # Sort the brands alphabetically
            self.brand_dropdown["values"] = unique_brands
        elif selected_field == "Owned":
            self.filter_own_checkbox.grid()
        elif selected_field == "Piece Count":
            self.piece_count_dropdown.grid()
            self.piece_count_entry.grid()
        elif selected_field == "Width":
            self.width_dropdown.grid()
        elif selected_field == "Car Count":
            self.car_count_dropdown.grid()
            car_counts = list(set(int(item["Car Count"]) for item in self.lego_data if isinstance(item["Car Count"], int) or (isinstance(item["Car Count"], str) and item["Car Count"].isdigit())))
            car_counts.sort()
            self.car_count_dropdown["values"] = car_counts
        elif selected_field == "Release Date":
            self.release_date_dropdown.grid()
            release_years = list(set(item["Release Date"] for item in self.lego_data))
            release_years.sort()
            self.release_date_dropdown["values"] = release_years
        else:
            self.filter_entry.grid()
    
    def apply_filter(self):
        # Apply the selected filter to the LEGO sets list
        filter_field = self.filter_option.get()
        filter_value = self.filter_value_var.get()

        if not filter_field:
            self.filtered_data = self.lego_data
        elif filter_field == "Owned":
            self.filtered_data = [item for item in self.lego_data if item.get("Owned", False) == self.filter_own_var.get()]
        elif filter_field == "Piece Count":
            try:
                piece_count = int(self.piece_count_var.get())
                if self.piece_count_option.get() == "higher":
                    self.filtered_data = [item for item in self.lego_data if int(item["Piece Count"]) > piece_count]
                else:
                    self.filtered_data = [item for item in self.lego_data if int(item["Piece Count"]) < piece_count]
            except ValueError:
                messagebox.showwarning("Invalid input", "Please enter a valid number for Piece Count.")
                return
        elif filter_field == "Width":
            try:
                width = int(self.width_var.get())
                self.filtered_data = [item for item in self.lego_data if int(item["Width"]) == width]
            except ValueError:
                messagebox.showwarning("Invalid input", "Please select a valid width.")
                return
        elif filter_field == "Car Count":
            try:
                car_count = int(self.car_count_var.get())
                self.filtered_data = [item for item in self.lego_data if int(item["Car Count"]) == car_count]
            except ValueError:
                messagebox.showwarning("Invalid input", "Please select a valid car count.")
                return
        elif filter_field == "Release Date":
            self.filtered_data = [item for item in self.lego_data if item["Release Date"] == filter_value]
        else:
            self.filtered_data = [item for item in self.lego_data if filter_value.lower() in str(item.get(filter_field, "")).lower()]

        # Update the list with the filtered data
        self.populate_listbox()

    def clear_filter(self):
        # Clear the applied filter
        self.filter_option.set("")
        self.filter_value_var.set("")
        self.filter_own_var.set(False)
        self.filter_own_checkbox.grid_remove()
        self.filter_entry.grid()
        self.filtered_data = self.lego_data
        self.populate_listbox()
    
    def show_pie_chart(self):
        # Show pie chart of brand distribution
        brand_counter = Counter(item["Brand"] for item in self.filtered_data)
        labels = brand_counter.keys()
        sizes = brand_counter.values()
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        plt.title("Brand Distribution")
        plt.show()
    
    def update_statistics(self):
        # Update statistics based on filtered data
        total_parts = sum(int(item["Piece Count"]) for item in self.filtered_data if isinstance(item["Piece Count"], int) or (isinstance(item["Piece Count"], str) and item["Piece Count"].isdigit()))
        total_price = sum(float(item["Price"].replace('€', '').replace(',', '.')) for item in self.filtered_data if item["Price"].replace('€', '').replace(',', '.').replace('.', '', 1).isdigit())
        total_cars = sum(int(item["Car Count"]) for item in self.filtered_data if isinstance(item["Car Count"], int) or (isinstance(item["Car Count"], str) and item["Car Count"].isdigit()))
        
        stats_text = f"Total Pieces: {total_parts}\n"
        stats_text += f"Total Price: €{total_price:.2f}\n"
        stats_text += f"Number of Cars: {total_cars}\n"
        
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = LegoTrackerApp(root)
    root.mainloop()
