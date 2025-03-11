# Lego Speed Champions Tracker

## 📄 Project Description
This program is a **Lego Speed Champions Tracker**, allowing you to manage your collection of Lego Speed Champions sets. The application enables you to **add**, **edit**, **delete**, and **filter** sets. Additionally, **statistics** about the collection are displayed, and a **graphical representation** in the form of a pie chart is available to show brand distribution.

The data is stored in a JSON file (`lego_speed_champions.json`) and can be updated at any time.

## 📚 Features
### 1. **Adding & Editing Entries**
- New Lego sets can be added through the input form.
- Existing sets can be edited by selecting them from the list.
- Changes are saved in the JSON file.

### 2. **Deleting Entries**
- Select an entry in the list and click "Delete" to remove it.
- Deleting an entry is irreversible.

### 3. **Filtering Function**
- Filter the list based on the following criteria:
  - **Brand** (e.g., Ferrari, Porsche, Audi)
  - **Width** (6 or 8 studs)
  - **Release Date** (e.g., 03.2024)
  - **Piece Count** (with an option to filter greater or lesser than a certain amount)
  - **Number of Cars in the Set**
  - **Owned?** (Checkbox filter)
- Filtering is performed via dropdown menus and input fields.

### 4. **Statistics**
- Total number of **pieces** in the collection.
- Total price of the sets.
- Total number of **cars** in the collection.
- Statistics are updated automatically after every change.

### 5. **Pie Chart for Brand Distribution**
- Displays a graphical breakdown of Lego sets by brand.
- Provides a visual analysis of the collection.

## 🛠️ Installation & Setup
### **Requirements**
- **Python 3.x** installed
- **Required libraries:** `tkinter`, `matplotlib`, `json`, `os`
- If `matplotlib` is not installed, install it using the following command:
  ```sh
  pip install matplotlib


### **Starting the Application**
1. Ensure that `speedchampionsTracker.py` and `lego_speed_champions.json` are in the same directory.
2. Open a terminal and run the script:
   ```sh
   python speedchampionsTracker.py

3. The graphical user interface will open, allowing you to manage your Lego collection.

## 🔧 Technical Details
- **GUI**: Built with `tkinter`
- **Data Management**: JSON file as a persistent storage
- **Filtering**: Dynamically handled using `tkinter` widgets
- **Graphs**: Generated with `matplotlib`
- **Automatic Price Formatting**: Extracts prices in `€xx.xx` format using regular expressions (`re` module)

## 💡 Usage Notes
- When editing or adding a set, all required fields must be filled in.
- The JSON file is **automatically updated**, so changes persist after restarting the application.
- If issues occur, check the **JSON file** for proper formatting.

Enjoy using the Lego Speed Champions Tracker! 🚗💨


