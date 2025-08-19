import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import string
import time

# Password Cracking Algorithms
def brute_force(password, charset=string.ascii_lowercase + string.digits):
    attempts = 0
    start_time = time.time()
    for length in range(1, len(password) + 1):
        for guess in itertools.product(charset, repeat=length):
            if stop_flag:
                # this.stop_flag = False
                break
            attempts += 1
            guess = ''.join(guess)
            yield guess, attempts, time.time() - start_time
            if guess == password:
                return

def dictionary_attack(password, dictionary):
    attempts = 0
    start_time = time.time()
    for word in dictionary:
        if stop_flag:
            # stop_flag = False
            break
        attempts += 1
        yield word, attempts, time.time() - start_time
        if word == password:
            return

# GUI

# نخزن الباسوردات اللي اتفكت قبل كده
cracked_passwords = []

def start_attack():
    global stop_flag
    stop_flag = False
    print(stop_flag)
    password = entry_password.get()
    attack_type = attack_choice.get()

    if not password:
        messagebox.showwarning("Error", "Enter a password first!")
        return

    progress_bar["value"] = 0
    log_box.delete(1.0, tk.END)
    window.update()

    #
    dictionary = ["123456", "password", "letmein", "qwerty", "admin", "hello", "welcome"] + cracked_passwords

    if attack_type == "Brute Force":
        generator = brute_force(password)
    else:
        generator = dictionary_attack(password, dictionary)

    for guess, attempts, elapsed in generator:
        log_box.insert(tk.END, f"Trying: {guess} | Attempts: {attempts} | Time: {elapsed:.2f}s\n")
        log_box.see(tk.END)

        progress_bar["value"] = min(100, (attempts / 1000) * 100)
        window.update()

        if guess == password:
            messagebox.showinfo("Success!", f"Password found: {guess}\nAttempts: {attempts}\nTime: {elapsed:.2f}s")
            # ييخزن الباسورد اللي فكيناه ب الBrute Force
            if attack_type == "Brute Force" and guess not in cracked_passwords:
                cracked_passwords.append(guess)

            return

    messagebox.showerror("Failed", "Password not found in Dictionary!")

stop_flag = False
def stop_attack():
    global stop_flag
    stop_flag = True

    
# Main Window

window = tk.Tk()
window.title(" Password Cracker Simulator")
window.geometry("600x400")

label_title = tk.Label(window, text="Cybersecurity Password Cracker Simulator", font=("Arial", 14, "bold"))
label_title.pack(pady=10)

frame_input = tk.Frame(window)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Enter Password:").grid(row=0, column=0, padx=5)
# entry_password = tk.Entry(frame_input, width=30)
entry_password = tk.Entry(frame_input, show="*", width=30)

entry_password.grid(row=0, column=1)

attack_choice = tk.StringVar(value="Brute Force")

tk.Radiobutton(window, text="Brute Force", variable=attack_choice, value="Brute Force").pack()
tk.Radiobutton(window, text="Dictionary Attack", variable=attack_choice, value="Dictionary").pack()

btn_start = tk.Button(window, text="Start Attack", command=start_attack, bg="green", fg="white")
btn_start.pack(pady=10)

btn_stop = tk.Button(window, text="stop Attack", command=stop_attack, bg="red", fg="white")
btn_stop.pack(pady=10)

progress_bar = ttk.Progressbar(window, length=500, mode="determinate")
progress_bar.pack(pady=10)

log_box = tk.Text(window, height=10, width=70)
log_box.pack(pady=10)

window.mainloop()
