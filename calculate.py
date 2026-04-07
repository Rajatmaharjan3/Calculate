import tkinter

# --- Setup and Constants ---
button_values = [
    ["AC", "+/-", "%", "÷"], 
    ["7", "8", "9", "×"], 
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

row_count = len(button_values)
column_count = len(button_values[0])

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

window = tkinter.Tk() 
window.title("Calculator") 
window.configure(bg=color_black)
window.resizable(False, False)

main_container = tkinter.Frame(window, bg=color_black)
main_container.pack()

# --- CALCULATOR FRAME ---
frame = tkinter.Frame(main_container, bg=color_black)
frame.grid(row=0, column=0, padx=10, pady=10)

# History Toggle
history_visible = False
def toggle_history():
    global history_visible
    if history_visible:
        history_frame.grid_remove()
        history_visible = False
    else:
        history_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        history_visible = True

history_btn = tkinter.Button(frame, text="History 🕒", command=toggle_history, 
                             bg=color_dark_gray, fg=color_white, font=("Arial", 10), relief="flat")
history_btn.grid(row=0, column=0, sticky="nw", pady=5)

# --- SCREEN ---
full_equation_label = tkinter.Label(frame, text="", font=("Arial", 12), background=color_black,
                                   foreground=color_orange, anchor="e")
full_equation_label.grid(row=1, column=0, columnspan=column_count, sticky="se")

label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black,
                      foreground=color_white, anchor="e", width=10)
label.grid(row=2, column=0, columnspan=column_count, sticky="nsew")

# --- HISTORY ---
history_frame = tkinter.Frame(main_container, bg="#2C2C2C")
tkinter.Label(history_frame, text="History", font=("Arial", 12, "bold"), bg="#2C2C2C", fg=color_white).pack(pady=5)
history_list = tkinter.Listbox(history_frame, font=("Arial", 12), width=25, height=15, 
                               bg=color_black, fg=color_light_gray, border=0)
history_list.pack(padx=10, pady=5)

def clear_history():
    history_list.delete(0, tkinter.END)

tkinter.Button(history_frame, text="Clear", command=clear_history, bg="#FF3B30", fg=color_white).pack(pady=5)

equation_list = []

def remove_zero_decimal(num):
    if num % 1 == 0: return str(int(num))
    return str(num)

def button_clicked(value):
    global equation_list
    current_val = label["text"]

    if value in "+-×÷":
        equation_list.append(current_val)
        equation_list.append(value)
        full_equation_label["text"] = " ".join(equation_list)
        label["text"] = "0"

    elif value == "=":
        equation_list.append(current_val)
        full_str = "".join(equation_list).replace("×", "*").replace("÷", "/")
        try:
            # eval() handles the long string 8+8+8 all at once
            result = eval(full_str)
            final_res = remove_zero_decimal(result)
            
            # Save to history
            history_list.insert(0, f"{' '.join(equation_list)} = {final_res}")
            
            label["text"] = final_res
            full_equation_label["text"] = ""
            equation_list = []
        except:
            label["text"] = "Error"
            equation_list = []

    elif value == "AC":
        label["text"] = "0"
        full_equation_label["text"] = ""
        equation_list = []

    elif value == "√":
        res = float(current_val) ** 0.5
        label["text"] = remove_zero_decimal(res)
        history_list.insert(0, f"√({current_val}) = {label['text']}")

    elif value == "+/-":
        label["text"] = remove_zero_decimal(float(current_val) * -1)

    elif value == "%":
        label["text"] = remove_zero_decimal(float(current_val) / 100)

    else: # Numbers and dots
        if value == ".":
            if "." not in current_val: label["text"] += "."
        elif current_val == "0":
            label["text"] = value
        else:
            label["text"] += value

# --- BUTTONS ---
for row in range(row_count):
    for column in range(column_count):
        val = button_values[row][column] 
        btn = tkinter.Button(frame, text=val, font=("Arial", 30), width=4, height=1,
                             command=lambda v=val: button_clicked(v))
        
        if val in top_symbols:
            btn.config(fg=color_black, bg=color_light_gray)
        elif val in right_symbols:
            btn.config(fg=color_white, bg=color_orange)
        else:
            btn.config(fg=color_white, bg=color_dark_gray)
        
        btn.grid(row=row+3, column=column, sticky="nsew", padx=1, pady=1)

window.mainloop()