import os
import re
import schedule
import time
import  shutil
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox



LOGS = "logs.txt"  # log file
DATA = "data.json"
if not os.path.exists(LOGS):
    with open(LOGS, "w") as f:
        f.write("")  # Creates an empty file

if not os.path.exists(DATA):
    with open(DATA, "w") as f1:
        f1.write("")

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        # Source folder picker
        self.src_label = tk.Label(root, text="Source Folder:")
        self.src_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.src_entry = tk.Entry(root, width=50)
        self.src_entry.grid(row=0, column=1, padx=5, pady=5)

        self.src_button = tk.Button(root, text="Browse", command=self.browse_src)
        self.src_button.grid(row=0, column=2, padx=5, pady=5)

        # Destination folder picker
        self.dest_label = tk.Label(root, text="Destination Folder:")
        self.dest_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.grid(row=1, column=1, padx=5, pady=5)

        self.dest_button = tk.Button(root, text="Browse", command=self.browse_dest)
        self.dest_button.grid(row=1, column=2, padx=5, pady=5)

        # Dropdown menu for automation mode
        self.mode_label = tk.Label(root, text="Automation Mode:")
        self.mode_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.mode_var = tk.StringVar()
        self.mode_dropdown = ttk.Combobox(root, textvariable=self.mode_var, state='readonly')
        self.mode_dropdown['values'] = ['Instant Move', 'Scheduled every 2 minute', 'Scheduled every 5 minute']
        self.mode_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.mode_dropdown.current(0)

        # Tracked folders list
        self.tracked_label = tk.Label(root, text="Tracked Folders:")
        self.tracked_label.grid(row=3, column=0, padx=5, pady=5, sticky='ne')

        self.tracked_listbox = tk.Listbox(root, height=5, width=70)
        self.tracked_listbox.grid(row=3, column=1, padx=5, pady=5)

        # Logs list
        self.logs_label = tk.Label(root, text="Logs:")
        self.logs_label.grid(row=4, column=0, padx=5, pady=5, sticky='ne')

        self.logs_listbox = tk.Listbox(root, height=10, width=70)
        self.logs_listbox.grid(row=4, column=1, padx=5, pady=5)

        # Show logs button
        self.show_logs_button = tk.Button(root, text="Show All Logs", command=self.show_logs)
        self.show_logs_button.grid(row=4, column=2, padx=5, pady=5)

        # Start button
        self.start_button = tk.Button(root, text="Start Automation", bg="green", fg="white", command=self.start_automation)
        self.start_button.grid(row=5, column=1, padx=5, pady=10)

    def browse_src(self):
        folder = filedialog.askdirectory()
        if folder:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, folder)
            self.tracked_listbox.insert(tk.END, f"Source: {folder}")

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)
            self.tracked_listbox.insert(tk.END, f"Destination: {folder}")

    def show_logs(self):
        self.logs_listbox.delete(0, tk.END)
        try:
            with open("logs.txt", "r") as file:
                for line in file:
                    log=line.strip() # Removes trailing newline characters
                    self.logs_listbox.insert(tk.END, log)
        except FileNotFoundError:
            msg = "The logfile was not found."
            self.logs_listbox.insert(tk.END, msg)
        except IOError:
            msg ="An I/O error occurred while reading the log  file."
            self.logs_listbox.insert(tk.END, msg)

    
        
        
        
    def start_automation(self):
        mode = self.mode_var.get()
        src = self.src_entry.get()
        dest = self.dest_entry.get()
        if not src or not dest:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return
        log_entry = f"Automation started in '{mode}' mode from '{src}' to '{dest}'"
        self.logs_listbox.insert(tk.END, log_entry)
        messagebox.showinfo("Started", "Automation has started!")
        if (mode == "Scheduled every 2 minute" or mode == "Scheduled every 5 minute" ):
            self.schedule_task(mode)
        else:
            self.find_files()
           
            
    def find_files(self):
        src = self.src_entry.get()
        dest = self.dest_entry.get()
        source_dic= os.listdir(src)
        desti_direc = [name for name in os.listdir(dest) if os.path.isdir(os.path.join(dest, name))] # to get directory names
        for i in source_dic:
                match = re.search(r'\.([a-zA-Z0-9]+)$', i)
                if match:
                    folder_name = match.group(1)
                    if (folder_name not in desti_direc):
                        os.mkdir(dest+'\\'+folder_name)
                        desti_direc.append(folder_name)
                        self.move_files(src,i,dest,folder_name)
                        
                        
                    else:
                        self.move_files(src,i,dest,folder_name)


    def move_files(self,source,file,destination,f_name):
        try:
            shutil.move(source+'\\'+file,destination+f_name)
            msg =f"Successfully moved '{file}' to '{destination}'."
            self.insert_logs(msg)
        except FileNotFoundError:
            msg =f"Error: The source '{source}' does not exist."
            self.insert_logs(msg)
        except PermissionError:
            msg =f"Error: Permission denied while moving '{source}' to '{destination}'."
            self.insert_logs(msg)
        except shutil.Error as e:
            msg=f"Error: {e}"
            self.insert_logs(msg)
        except Exception as e:
            msg=f"An unexpected error occurred: {e}"
            self.insert_logs(msg)
    
    def schedule_two_min(self):
        pass
    def schedule_five_min(self):
        pass

    

    def insert_logs(self,msg):
        self.logs_listbox.insert(tk.END, msg)
        msg+='\n'
        with open(LOGS, "a") as f:
            f.write(msg)

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    def schedule_task(self, md):
        if md == "Scheduled every 2 minute":
            schedule.every(2).minutes.do(self.find_files)
        elif md == "Scheduled every 5 minute":
            schedule.every(5).minutes.do(self.find_files)

        # Start the scheduler in a background thread
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
   

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
