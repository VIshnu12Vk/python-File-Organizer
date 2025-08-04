# 🗂️ File Organizer
**File Organizer** is a Python-based utility that automates the process of organizing files within a selected folder. It helps users maintain a tidy and efficient workspace by sorting files into designated subfolders based on their type (e.g. PDFs, images, documents, etc.).

## 🚀 Features
- Select a folder to track for file organization
- Automatically moves files into categorized folders based on file extension
- Real-time tracking and organizing with scheduling support
- Graphical User Interface (GUI) built with Tkinter for easy interaction

## 🛠️ Technologies Used
- **Language:** Python
- **GUI Toolkit:** Tkinter
- **Libraries:**
  - `os`
  - `re`
  - `schedule`
  - `time`
  - `shutil`
  - `threading`
  - `tkinter` (`filedialog`, `ttk`, `messagebox`)
 
  ## 📁 How It Works
  1. **User selects a folder** to monitor through a simple GUI.
2. The program **scans the folder periodically** using a scheduler.
3. Files are **automatically sorted and moved** into respective subfolders:
   - `.pdf` files → `/PDFs/`
   - `.jpg`, `.png` files → `/png/` or `/jpg/`
  
## 💻 Setup & Usage
1. Clone the repository:
   ```bash
   create folder file-organizer
   git clone https://github.com/VIshnu12Vk/python-File-Organizer
   cd file-organizer
   ```

2. Install required dependencies (if any):
   ```bash
   pip install schedule
   ```

3. Run the script:
   ```bash
   python main.py

4. Use the GUI to select the folder you'd like to monitor and organize.
   - `.docx`, `.txt` files → `/Documents/`
   - And so on...
