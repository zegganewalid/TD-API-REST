import json, urllib.request, urllib.error, tkinter as tk
from tkinter import simpledialog, messagebox

API = "http://localhost:3000"

def http(method, path, body=None):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(body).encode() if body else None,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "detail": e.read().decode()}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Cliente"); self.geometry("500x400")
        self.output = tk.Text(self, height=15, width=60); self.output.pack(pady=10)
        bf = tk.Frame(self); bf.pack()
        for i, (label, cmd) in enumerate([
            ("Read", self.read_data), ("Add", self.add_value),
            ("Update", self.update_value), ("Delete", self.delete_value),
        ]):
            tk.Button(bf, text=label, command=cmd).grid(row=0, column=i, padx=5)
        self.read_data()

    def show(self, d):
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", json.dumps(d, indent=2, ensure_ascii=False))

    def read_data(self):
        self.show(http("GET", "/patients"))

    def add_value(self):
        nom = simpledialog.askstring("Add", "Nom :")
        prenom = simpledialog.askstring("Add", "Prénom :")
        ssn = simpledialog.askstring("Add", "SSN :")
        if nom and prenom and ssn:
            r = http("POST", "/patients", {"nom": nom, "prenom": prenom, "ssn": ssn})
            messagebox.showinfo("Add", str(r)); self.read_data()

    def update_value(self):
        ssn = simpledialog.askstring("Update", "SSN à modifier :")
        if not ssn: return
        nom = simpledialog.askstring("Update", "Nouveau nom :")
        prenom = simpledialog.askstring("Update", "Nouveau prénom :")
        new_ssn = simpledialog.askstring("Update", "Nouveau SSN :", initialvalue=ssn)
        if nom and prenom and new_ssn:
            r = http("PUT", f"/patients/{ssn}",
                     {"nom": nom, "prenom": prenom, "ssn": new_ssn})
            messagebox.showinfo("Update", str(r)); self.read_data()

    def delete_value(self):
        ssn = simpledialog.askstring("Delete", "SSN :")
        if ssn:
            r = http("DELETE", f"/patients/{ssn}")
            messagebox.showinfo("Delete", str(r)); self.read_data()

if __name__ == "__main__":
    Application().mainloop()