import tkinter as tk
from tkinter import messagebox
import random


user_data = {}
user_login = {}
history_pembayaran = []

list_nama_mahasiswa = [
    "ifah", "dipa", "huri", "pani",
    "bila", "helda",
]

def get_nominal_random():
    return random.choice([2400000, 2500000, 2600000, 2750000, 2800000, 3000000, 3200000])

def generate_tagihan_for(nim):
    if nim not in user_data:
        nominal = get_nominal_random()
        kode_va = "88" + str(random.randint(100000000, 999999999))
        nama = random.choice(list_nama_mahasiswa)
        user_data[nim] = {
            "nominal": f"Rp {nominal:,}".replace(",", "."),
            "kode_va": kode_va,
            "nama": nama
        }
    return user_data[nim]["nominal"], user_data[nim]["kode_va"], user_data[nim]["nama"]

def login_edlink():
    nim = nim_entry.get()
    pw = password_entry.get()

    if not nim or not pw:
        messagebox.showwarning("Login Gagal", "NIM dan Password tidak boleh kosong.")
        return

    nominal, kode_va, nama = generate_tagihan_for(nim)
    user_login["nim"] = nim
    user_login["password"] = pw
    user_login["nominal"] = nominal
    user_login["kode_va"] = kode_va
    user_login["nama"] = nama

    messagebox.showinfo("Login Berhasil", f"Selamat datang, {nama}!\nNIM: {nim}")
    show_menu()

def show_menu():
    login_frame.pack_forget()
    history_frame.pack_forget()
    metode_frame.pack_forget()
    tagihan_frame.pack_forget()
    menu_frame.pack(pady=20)

def tampilkan_tagihan():
    nominal_label.config(text=f"Nominal Tagihan: {user_login['nominal']}")
    kode_va_label.config(text=f"Kode VA: {user_login['kode_va']}")
    tagihan_frame.pack(pady=10)

def buka_metode_pembayaran():
    metode_frame.pack(pady=10)

def proses_pembayaran():
    metode = var_metode.get()
    if metode == "":
        messagebox.showwarning("Metode Belum Dipilih", "Pilih metode pembayaran terlebih dahulu.")
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi",
        f"Bayar UKT sebesar {user_login['nominal']} melalui {metode}?"
    )
    if konfirmasi:
        history_pembayaran.append(
            f"NIM: {user_login['nim']}, Nama: {user_login['nama']}, VA: {user_login['kode_va']}, Nominal: {user_login['nominal']}, Metode: {metode}"
        )
        messagebox.showinfo("Pembayaran Berhasil", f"Pembayaran berhasil melalui {metode}.\nTerima kasih!")
        
        tampilkan_history()

def tampilkan_history():
    login_frame.pack_forget()
    menu_frame.pack_forget()
    metode_frame.pack_forget()
    tagihan_frame.pack_forget()
    history_text.delete("1.0", tk.END)
    if not history_pembayaran:
        history_text.insert(tk.END, "Belum ada pembayaran yang tercatat.")
    else:
        for entry in history_pembayaran:
            history_text.insert(tk.END, f"{entry}\n")
    history_frame.pack(pady=10)

def kembali_ke_menu():
    history_frame.pack_forget()
    menu_frame.pack(pady=20)

def reset_form():
    nim_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    nominal_label.config(text="Nominal Tagihan: -")
    kode_va_label.config(text="Kode VA: -")
    var_metode.set("")
    metode_frame.pack_forget()
    tagihan_frame.pack_forget()
    menu_frame.pack_forget()
    history_frame.pack_forget()
    login_frame.pack(pady=20)
    user_login.clear()

root = tk.Tk()
root.title("Simulasi Pembayaran UKT")
root.geometry("480x700")

tk.Label(
    root,
    text="Simulasi Pembayaran UKT via Edlink & m-Banking",
    font=("Helvetica", 14, "bold"),
    wraplength=420,
    justify="center"
).pack(pady=20)

login_frame = tk.Frame(root)
tk.Label(login_frame, text="Login ke Edlink", font=("Helvetica", 12, "bold")).pack()
tk.Label(login_frame, text="NIM").pack()
nim_entry = tk.Entry(login_frame, width=30)
nim_entry.pack()
tk.Label(login_frame, text="Password").pack()
password_entry = tk.Entry(login_frame, width=30, show="*")
password_entry.pack()
tk.Button(login_frame, text="Login", width=15, command=login_edlink).pack(pady=10)
login_frame.pack(pady=20)

menu_frame = tk.Frame(root)
tk.Label(menu_frame, text="Menu Utama", font=("Helvetica", 12, "bold")).pack(pady=5)
tk.Button(menu_frame, text="Lihat Tagihan", width=25, command=tampilkan_tagihan).pack(pady=5)
tk.Button(menu_frame, text="Pilih Metode Pembayaran", width=25, command=buka_metode_pembayaran).pack(pady=5)
tk.Button(menu_frame, text="Lihat History Pembayaran", width=25, command=tampilkan_history).pack(pady=5)
tk.Button(menu_frame, text="Keluar / Reset", width=25, command=reset_form).pack(pady=5)

tagihan_frame = tk.Frame(root)
nominal_label = tk.Label(tagihan_frame, text="Nominal Tagihan: -", font=("Helvetica", 10))
nominal_label.pack()
kode_va_label = tk.Label(tagihan_frame, text="Kode VA: -", font=("Helvetica", 10))
kode_va_label.pack()

metode_frame = tk.Frame(root)
tk.Label(metode_frame, text="Pilih Metode Pembayaran", font=("Helvetica", 12)).pack(pady=5)
var_metode = tk.StringVar()
tk.Radiobutton(metode_frame, text="Bank BSI", variable=var_metode, value="Bank BSI").pack(anchor="w")
tk.Radiobutton(metode_frame, text="Bank Aceh", variable=var_metode, value="Bank Aceh").pack(anchor="w")
tk.Button(metode_frame, text="Bayar Sekarang", command=proses_pembayaran).pack(pady=10)

history_frame = tk.Frame(root)
tk.Label(history_frame, text="History Pembayaran", font=("Helvetica", 12, "bold")).pack()
history_text = tk.Text(history_frame, height=10, width=60)
history_text.pack()
tk.Button(history_frame, text="Kembali ke Menu", command=kembali_ke_menu).pack(pady=5)

root.mainloop()

