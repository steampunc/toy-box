#!/usr/bin/python
import Tkinter as tk
from mrhelper import *

mrhelper = MrHelper()

main = tk.Tk()
main.geometry("500x400")
upper_frame = tk.Frame(main)
lower_frame = tk.Frame(main)

scrollbar = tk.Scrollbar(upper_frame)
prompt = tk.Text(upper_frame, yscrollcommand = scrollbar.set, wrap=tk.WORD)
scrollbar.pack(side = tk.RIGHT, fill=tk.Y)

prompt.tag_configure("mrhelper", foreground="blue")



def on_click(event=None):
    prompt.insert(tk.END, "\nUser: " + user_response.get())
    sanitized_user_input = user_response.get().lower().lstrip().rstrip()

    helper_response = mrhelper.RespondToInput(user_response.get())

    prompt.insert(tk.END, "\nMr. Helper: " + helper_response, "mrhelper")
    prompt.see(tk.END)

    user_input.delete(0, tk.END)

    prompt.pack(side = tk.LEFT, fill = tk.BOTH, expand= tk.YES)
    scrollbar.config( command = prompt.yview )

    upper_frame.pack()
    input_button.pack(side = tk.LEFT)
    user_input.pack(side = tk.RIGHT)
    lower_frame.pack(side = tk.BOTTOM)


input_button = tk.Button(lower_frame, text="Response", command=on_click)
user_response = tk.StringVar()
user_input = tk.Entry(lower_frame, bd=1, textvariable = user_response)
main.bind('<Return>', on_click)

prompt.insert(tk.END, "Hello, I'm Mr. Helper, here to help you with managing your things and time! Type help for assistance!", "mrhelper")
prompt.pack( side = tk.LEFT, fill = tk.BOTH )
scrollbar.config( command = prompt.yview )

upper_frame.pack(fill = tk.BOTH, expand=tk.YES)

input_button.pack(side = tk.LEFT)


user_input.pack(side = tk.RIGHT, fill = tk.X, expand=tk.YES)

lower_frame.pack(side = tk.BOTTOM, fill = tk.X, expand=tk.YES)

while True:
    main.update_idletasks()
    main.update()
