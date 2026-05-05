import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Окно приложения
root = tk.Tk()
root.title("Training Planner")
root.geometry("600x500")

# Переменная для хранения данных
trainings = []

# Загрузка данных из JSON
def load_data():
    try:
        with open("trainings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Сохранение данных в JSON
def save_data():
    with open("trainings.json", "w") as f:
        json.dump(trainings, f)

# Проверка даты
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

# Добавление тренировки
def add_training():
    date = date_entry.get()
    training_type = type_combo.get()
    duration = duration_entry.get()

    # Проверка ввода
    if not is_valid_date(date):
        messagebox.showerror("Ошибка", "Неверный формат даты (ДД.ММ.ГГГГ)")
        return
    if not duration.isdigit() or int(duration) <= 0:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return
    if not training_type:
        messagebox.showerror("Ошибка", "Выберите тип тренировки")
        return

    # Добавляем запись
    trainings.append({
        "date": date,
        "type": training_type,
        "duration": int(duration)
    })
    save_data()
    update_table()
    clear_inputs()

# Очистка полей ввода
def clear_inputs():
    date_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    type_combo.set("")

# Обновление таблицы
def update_table():
    for item in tree.get_children():
        tree.delete(item)
    filtered = filter_trainings()
    for t in filtered:
        tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))

# Фильтрация тренировок
def filter_trainings():
    selected_type = filter_type.get()
    selected_date = filter_date.get()

    result = trainings
    if selected_type != "Все":
        result = [t for t in result if t["type"] == selected_type]
    if selected_date:
        result = [t for t in result if selected_date in t["date"]]
    return result

# Интерфейс

# Поля ввода
tk.Label(root, text="Дата (ДД.ММ.ГГГГ)").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Тип тренировки").grid(row=1, column=0, padx=5, pady=5)
type_combo = ttk.Combobox(root, values=["Бег", "Плавание", "Йога", "Силовая"])
type_combo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Длительность (мин)").grid(row=2, column=0, padx=5, pady=5)
duration_entry = tk.Entry(root)
duration_entry.grid(row=2, column=1, padx=5, pady=5)

# Кнопка добавления
add_btn = tk.Button(root, text="Добавить тренировку", command=add_training)
add_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Фильтры
tk.Label(root, text="Фильтр по типу:").grid(row=4, column=0, padx=5, pady=5)
filter_type = ttk.Combobox(root, values=["Все", "Бег", "Плавание", "Йога", "Силовая"])
filter_type.set("Все")
filter_type.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по дате:").grid(row=5, column=0, padx=5, pady=5)
filter_date = tk.Entry(root)
filter_date.grid(row=5, column=1, padx=5, pady=5)

filter_btn = tk.Button(root, text="Применить фильтры", command=update_table)
filter_btn.grid(row=6, column=0, columnspan=2, pady=5)

# Таблица
tree = ttk.Treeview(root, columns=("Date", "Type", "Duration"), show="headings")
tree.heading("Date", text="Дата")
tree.heading("Type", text="Тип")
tree.heading("Duration", text="Длительность (мин)")
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Загрузка данных при запуске
trainings = load_data()
update_table()

root.mainloop()