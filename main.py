# libs
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import XMLparser as prs
import difflib


class NegException(Exception):
    def __init__(self, text):
        self.text = text


def getActivated():
    if not activate.get():
        valute_list_from.config(state=DISABLED)
        valute_list_to.config(state=DISABLED)
        style.theme_use('disabled')
        for button in range(len(curr_list)):
            curr_list[button].config(state=NORMAL)
            curr_list_to[button].config(state=NORMAL)
        curr_frame_add.config(bg='#2c2c2c')
        label_hint_upper.config(bg='#2c2c2c', fg='#b0b0b0')
        label_hint_lower.config(bg='#2c2c2c', fg='#b0b0b0')
    else:
        valute_list_from.config(state='readonly')
        valute_list_to.config(state='readonly')
        style.theme_use('active')
        for button in range(len(curr_list)):
            curr_list[button].config(state=DISABLED)
            curr_list_to[button].config(state=DISABLED)
        curr_var_from.set('None')
        curr_var_to.set('None')
        curr_frame_add.config(bg=bg_color.get())
        label_hint_upper.config(bg=bg_color.get(), fg=fg_color.get())
        label_hint_lower.config(bg=bg_color.get(), fg=fg_color.get())


def calculate():
    if not activate.get():
        if curr_var_from.get() == 'None' and curr_var_to.get() == 'None':
            mb.showwarning("Ошибка", "Выберите валюту")
        curr_result.delete(0, END)
        try:
            if float(user_input.get()) < 0:
                raise NegException("Можно вводить только положительные числа!")
            elif curr_var_from.get() == curr_var_to.get():
                final_res = float(user_input.get())
            elif curr_var_from.get() == "RUB":
                final_res = float(user_input.get()) / valute_list[curr_var_to.get()]
            elif curr_var_to.get() == "RUB":
                final_res = float(user_input.get()) * valute_list[curr_var_from.get()]
            else:
                final_res = float(user_input.get()) * valute_list[curr_var_from.get()] / valute_list[curr_var_to.get()]
            curr_result.insert(END, round(final_res, 2))
        except NegException as error:
            mb.showerror("Ошибка", error)
            user_input.delete(0, END)
        except ValueError:
            mb.showerror("Ошибка", "Строка не должна быть пустой! Можно вводить только числа!")
            user_input.delete(0, END)
    else:
        result_from = getSimilar(comboValute_from.get(), addit_valute_names.items())
        result_to = getSimilar(comboValute_to.get(), addit_valute_names.items())
        curr_result.delete(0, END)
        try:
            if float(user_input.get()) < 0:
                raise NegException("Можно вводить только положительные числа!")
            elif result_from == result_to:
                final_res = float(user_input.get())
            elif result_from == "RUB":
                final_res = float(user_input.get()) / valute_list[result_to]
            elif result_to == "RUB":
                final_res = float(user_input.get()) * valute_list[result_from]
            else:
                final_res = float(user_input.get()) * valute_list[result_from] / valute_list[result_to]
            curr_result.insert(END, round(final_res, 2))
        except NegException as error:
            mb.showerror("Ошибка", error)
            user_input.delete(0, END)
        except ValueError:
            mb.showerror("Ошибка", "Строка не должна быть пустой! Можно вводить только числа!")
            user_input.delete(0, END)


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


def getSimilar(obj_1, obj_2):
    similarityDict = {}
    for key, value in obj_2:
        similarityDict[key] = similarity(obj_1, value)
    max_value = max(list(similarityDict.values()))
    for key, value in similarityDict.items():
        if value == max_value:
            return key


if __name__ == "__main__":
    root = Tk()

bg_color = StringVar()
fg_color = StringVar()
bg_color.set('#3f3f3f')
fg_color.set('#ffffff')
root.title('Конвертер валют')
root.geometry('400x600')
root.minsize(400, 600)
root.maxsize(400, 600)
root.config(bg=bg_color.get())
root.iconbitmap('dollar_sign.ico')
url = r'http://www.cbr.ru/scripts/XML_daily.asp'
url_to_get_names = r'http://www.cbr.ru/scripts/XML_val.asp'
valute_names = prs.getNames(url_to_get_names)
addit_valute_names = prs.getCourse(url, 1)
addit_valute_names = addit_valute_names.copy()
valute_list = prs.getCourse(url)
style = ttk.Style()

# Upper widgets frame
upper_frame = Frame(root)
upper_frame.place(relx=0.5, rely=0.1, width='380', height='90', anchor='center')
upper_frame.config(bg=bg_color.get(), highlightcolor='white', highlightthickness=1)

# User's input
user_input = Entry(upper_frame, highlightthickness=1)
user_input.place(relx=0.2, rely=0.65, anchor='center', width=130, height=30)
user_input.insert(END, '100')
user_input.config(bg=bg_color.get(), fg=fg_color.get(), highlightbackground='white',
                  highlightcolor='white', insertbackground=fg_color.get(), font=("Arial", 12), justify='center')
label_right = Label(upper_frame, text="У меня есть:", font=("Arial", 14), bg=bg_color.get(), fg=fg_color.get())
label_right.place(relx=0.2, rely=0.3, anchor='center')

# Result widget
curr_result = Entry(upper_frame, highlightthickness=1)
curr_result.place(relx=0.8, rely=0.65, anchor='center', width=130, height=30)
curr_result.config(bg=bg_color.get(), fg=fg_color.get(), highlightbackground='white',
                   highlightcolor='white', insertbackground=fg_color.get(), font=("Arial", 12), justify='center')
curr_result.bind("<Key>", lambda a: "break")
label_left = Label(upper_frame, text="Я получу:", font=("Arial", 14), bg=bg_color.get(), fg=fg_color.get())
label_left.place(relx=0.8, rely=0.3, anchor='center')

# Label "Часто используемые валюты"
curr_freq_label = Label(root, text='Часто используемые валюты', bg=bg_color.get(),
                        fg=fg_color.get(), font=("Arial", 11)).pack(anchor='center', pady=115)

# RB frame
curr_frame = Frame(root)
curr_frame.place(relx=0.5, rely=0.45, anchor='center', relwidth=0.95, height=240)
curr_frame.config(bg=bg_color.get(), highlightcolor='white', highlightthickness=1)

# RB for original currency
curr_var_from = StringVar()
curr_var_from.set('USD')
curr_names_list = ['USD', 'RUB', 'EUR', 'CNY']
curr_list = ['USD_rb', 'RUB_rb', 'EUR_rb', 'CNY_rb']
for currency in range(len(curr_list)):
    curr_list[currency] = Radiobutton(curr_frame, text=curr_names_list[currency],
                                      value=curr_names_list[currency], variable=curr_var_from, bg=bg_color.get(),
                                      fg=fg_color.get(), selectcolor='#00919b', activebackground=bg_color.get(),
                                      activeforeground='white', indicator=0, width=14, font=("Arial", 12),
                                      cursor='exchange')
for each in range(len(curr_list)):
    if each == 0 or each == 2:
        curr_list[each].grid(row=each, column=0, pady=25, padx=10)
    curr_list[each].grid(row=each, column=0)

# Hints labels
label_hint_right = Label(curr_frame, text='Перевести из:', bg=bg_color.get(),
                         fg=fg_color.get(), font=("Arial", 8))
label_hint_right.place(relx=0.1, rely=0.01)

label_hint_left = Label(curr_frame, text='Перевести в:', bg=bg_color.get(),
                        fg=fg_color.get(), font=("Arial", 8))
label_hint_left.place(relx=0.7, rely=0.01)

# RB for target currency
curr_var_to = StringVar()
curr_var_to.set('RUB')
curr_list_to = ['USD_rb_to', 'RUB_rb_to', 'EUR_rb_to', 'CNY_rb_to']
for currency in range(len(curr_list_to)):
    curr_list_to[currency] = Radiobutton(curr_frame, text=curr_names_list[currency],
                                         value=curr_names_list[currency], variable=curr_var_to, bg=bg_color.get(),
                                         fg=fg_color.get(), selectcolor='#00919b', activebackground=bg_color.get(),
                                         activeforeground='white', indicator=0, width=14, font=("Arial", 12),
                                         cursor='exchange')
for each in range(len(curr_list_to)):
    if each == 0:
        curr_list_to[each].grid(row=each, column=1, padx=75)
    curr_list_to[each].grid(row=each, column=1)

# Label "Дополнительные валюты"
curr_freq_label = Label(root, text='Активировать список дополнительных валют', bg=bg_color.get(),
                        fg=fg_color.get(), font=("Arial", 11)).place(relx=0.45, rely=0.69, anchor='center')

# Additional currencies frame
curr_frame_add = Frame(root)
curr_frame_add.place(relx=0.5, rely=0.82, anchor='center', relwidth=0.95, height=110)
curr_frame_add.config(bg='#2c2c2c', highlightbackground='white', highlightthickness=1)

# Additional currencies checkbox widget
activate = BooleanVar()
activate.set(0)
activeCheck = Checkbutton(root, variable=activate, onvalue=1, offvalue=0, bg=bg_color.get(),
                          activebackground=bg_color.get(), selectcolor=bg_color.get(), activeforeground='white',
                          fg=fg_color.get(), command=getActivated)
activeCheck.place(relx=0.95, rely=0.69, anchor='e')

# Hints labels & Additional currencies combobox widget
label_hint_upper = Label(curr_frame_add, text='Перевести из:', bg='#2c2c2c',
                         fg='#b0b0b0', font=("Arial", 8))
label_hint_upper.place(rely=0.15, relx=0.5, anchor='center')
label_hint_lower = Label(curr_frame_add, text='Перевести в:', bg='#2c2c2c',
                         fg='#b0b0b0', font=("Arial", 8))
label_hint_lower.place(rely=0.55, relx=0.5, anchor='center')

comboValute_from = StringVar()
comboValute_to = StringVar()
valute_list_from = ttk.Combobox(curr_frame_add, state=DISABLED, width=49, values=list(valute_names.values()),
                                font=("Arial", 10), textvariable=comboValute_from, justify='center')
style.theme_create('active', parent='alt',
                   settings={'TCombobox':
                                 {'configure':
                                      {'selectbackground': bg_color.get(),
                                       'fieldbackground': bg_color.get(),
                                       'background': bg_color.get(),
                                       'foreground': fg_color.get(),
                                       'bordercolor': 'white'
                                       }}}
                   )
style.theme_create('disabled', parent='alt',
                   settings={'TCombobox':
                                 {'configure':
                                      {'selectbackground': '#2c2c2c',
                                       'fieldbackground': '#2c2c2c',
                                       'background': '#2c2c2c',
                                       'foreground': '#2c2c2c',
                                       'bordercolor': 'black'
                                       }}}
                   )
style.theme_use("disabled")
valute_list_from.place(relx=0.02, rely=0.35, anchor='w')
valute_list_to = ttk.Combobox(curr_frame_add, state=DISABLED, width=49, values=list(valute_names.values()),
                              font=("Arial", 10), textvariable=comboValute_to, justify='center')
valute_list_to.place(relx=0.02, rely=0.75, anchor='w')

# Calculate button
calculate_btn = Button(root, text="Посчитать", width=15, bg=bg_color.get(), fg=fg_color.get(), font=("Arial", 12),
activebackground='#00919b', activeforeground='white')
calculate_btn.config(command=calculate)
calculate_btn.place(relx=0.5, rely=0.96, anchor="center")
root.mainloop()
