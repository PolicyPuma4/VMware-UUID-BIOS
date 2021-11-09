from tkinter import *
import os

window = Tk()

window.title("VMware UUID BIOS")
window.geometry("600x400")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

list_frame = Frame(window)
list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
list_frame.rowconfigure(1, weight=1)
list_frame.columnconfigure(0, weight=1)

label = Label(list_frame, text="Virtual machines:")
label.grid(row=0, column=0, sticky="sw")

listbox = Listbox(list_frame, exportselection=False)
listbox.grid(row=1, column=0, sticky="nsew")

scrollbar = Scrollbar(list_frame)
scrollbar.grid(row=1, column=1, sticky="ns")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


def on_select(event):
    widget = event.widget
    if widget.curselection():
        index = widget.curselection()[0]
        value = widget.get(index)
        if os.path.isfile(value):
            with open(value, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    if line.startswith("uuid.bios = \"") and line.endswith("\"\n"):
                        guid = line.removeprefix("uuid.bios = \"").removesuffix("\"\n")
                        entry.delete(0, END)
                        entry.insert(0, guid)
        return


listbox.bind('<<ListboxSelect>>', on_select)


def refresh_virtual_machines():
    listbox.delete(0, END)
    if os.name == "nt":
        import ctypes.wintypes
        CSIDL_PERSONAL = 5
        SHGFP_TYPE_CURRENT = 0
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        documents_path = buf.value
        if os.path.isdir(f"""{documents_path}\\Virtual Machines"""):
            for directory in os.listdir(f"{documents_path}\\Virtual Machines"):
                if os.path.isdir(f"{documents_path}\\Virtual Machines\\{directory}"):
                    for filename in os.listdir(f"{documents_path}\\Virtual Machines\\{directory}"):
                        if filename.endswith(".vmx"):
                            listbox.insert(END, f"{documents_path}\\Virtual Machines\\{directory}\\{filename}")
    return


refresh_virtual_machines()
refresh_button = Button(list_frame, text="Refresh", command=refresh_virtual_machines)
refresh_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))

input_frame = Frame(window)
input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=1)

label = Label(input_frame, text="UUID BIOS:")
label.grid(row=0, column=0, sticky="sw")

entry = Entry(input_frame)
entry.grid(row=1, column=0, sticky="ew", columnspan=2)


def randomise_guid():
    import uuid
    import re
    string = f"{uuid.uuid4()}".replace("-", "")
    string = ' '.join(string[i:i + 2] for i in range(0, len(string), 2))
    string = f"{string[:len(string) // 2]}-{string[(len(string) // 2) + 1:]}"
    entry.delete(0, END)
    entry.insert(0, string)
    return


randomise_button = Button(input_frame, text="Randomise", command=randomise_guid, width=50)
randomise_button.grid(row=2, column=0, sticky="ew", pady=(10, 0), padx=(0, 5))


def apply_guid():
    if listbox.curselection() and entry.get():
        selection = listbox.get(listbox.curselection()[0])
        if os.path.isfile(selection):
            replacement = ""
            with open(selection, "r") as file:
                for line in file.readlines():
                    if not line.startswith("uuid.bios = \"") and not line.startswith("uuid.action = \""):
                        replacement = f"{replacement}{line}"
            replacement = f"{replacement}uuid.bios = \"{entry.get()}\"\nuuid.action = \"keep\"\n"
            with open(selection, "w") as file:
                file.write(replacement)
    return


apply_button = Button(input_frame, text="Apply", command=apply_guid, width=50)
apply_button.grid(row=2, column=1, sticky="ew", pady=(10, 0), padx=(5, 0))

window.mainloop()
