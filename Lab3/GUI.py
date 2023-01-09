import customtkinter
from Btree import BTree


class Interface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.tree = BTree(10)

        self.title("B-Tree DBMS")
        self.geometry("720x720")
        self.minsize(360, 360)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.upper_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=("#EBEBEC", "#212325"))
        self.upper_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.upper_frame.grid(row=0, column=0, sticky="nsew")

        customtkinter.CTkLabel(self.upper_frame, width=60, text="Key:").grid(row=0, column=0, padx=10, pady=10)

        self.key = customtkinter.StringVar(value="")
        self.key_field = customtkinter.CTkEntry(self.upper_frame, textvariable=self.key, width=80)
        self.key_field.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(self.upper_frame, width=80, text="Value:").grid(row=0, column=2, padx=10, pady=10)

        self.value = customtkinter.StringVar(value="")
        self.value_field = customtkinter.CTkEntry(self.upper_frame, textvariable=self.value, width=120)
        self.value_field.grid(row=0, column=3, padx=10, pady=10)

        self.button_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.button_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.button_frame.grid(row=1, column=0, sticky="nsew")

        customtkinter.CTkButton(self.button_frame, text="Search", command=self.search, fg_color='#ea9148',
                                hover_color='#cc873d').grid(row=0, column=0, padx=10, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Insert", command=self.insert, fg_color='#ea9148',
                                hover_color='#cc873d').grid(row=0, column=1, padx=10, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Edit", command=self.edit, fg_color='#ea9148',
                                hover_color='#cc873d').grid(row=0, column=2, padx=10, pady=10)
        customtkinter.CTkButton(self.button_frame, text="Delete", command=self.delete, fg_color='#ea9148',
                                hover_color='#cc873d').grid(row=0, column=3, padx=10, pady=10)
        customtkinter.CTkLabel(self, width=60, text="Schema:").grid(row=2, column=0, sticky="W")
        self.schema = customtkinter.CTkTextbox(self, font=("Arial", 14))
        self.schema.grid(row=3, column=0, sticky="nsew", padx=10)

        customtkinter.CTkLabel(self, width=40, text="Log:").grid(row=4, column=0, sticky="W")
        self.logbox = customtkinter.CTkTextbox(self, font=("Arial", 14))
        self.logbox.grid(row=5, column=0, sticky="nsew", padx=10, pady=(0, 20))

    def search(self):
        try:
            self.log(f"Search:\tKey: {self.key.get()}")
            val = self.tree.search(int(self.key.get()))
            if val:
                self.value.set(val)
                self.log(f"\nSuccessful, value = {val[0]}")
            else:
                self.value.set("")
                self.log("\nKey is not found")
        except ValueError:
            self.log("\nIncorrect value")

    def insert(self):
        try:
            self.log(f"Insert:\tKey: {self.key.get()}\tValue: {self.value.get()}")
            if self.tree.search(int(self.key.get())):
                self.log("\nKey is already in tree")
            elif self.value.get() == "":
                self.log("\nPlease, enter value")
            else:
                self.tree.insert((int(self.key.get()), *self.value.get().split(" ")))
                self.update_schema()
                self.log("\nSuccessful")
                self.value.set("")
                self.key.set("")
        except ValueError:
            self.log("\nIncorrect value")

    def edit(self):
        try:
            self.log(f"Edit:\tKey: {self.key.get()}\tNew value: {self.value.get()}")
            if self.value.get() == "":
                self.log("\nPlease, enter value")
            elif self.tree.edit((int(self.key.get()), *self.value.get().split(" "))):
                self.log("\nSuccessful")
                self.value.set("")
            else:
                self.log("\nKey is not in tree")
        except ValueError:
            self.log("\nIncorrect value")

    def delete(self):
        try:
            self.log(f"Delete\tKey: {self.key.get()}")
            if self.tree.delete(int(self.key.get())):
                self.log("\nSuccessful")
                self.key.set("")
                self.update_schema()
            else:
                self.log("\nKey is not in tree")
        except ValueError:
            self.log("\nIncorrect value")

    def log(self, s):
        self.logbox.insert("0.0", s + "\n")

    def update_schema(self):
        self.schema.delete('0.0', "end")
        self.schema.insert("end", self.tree)


app = Interface()
app.mainloop()
