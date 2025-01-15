import os
import zipfile
import tarfile
import rarfile
import tkinter as tk
from tkinter import filedialog, scrolledtext
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

MAX_FILES = 10  # Максимальное количество файлов одного типа в каждой папке

def print_directory_structure(directory, output, indent=""):
    try:
        items = os.listdir(directory)
        file_types_count = defaultdict(int)
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                output.insert(tk.END, f"{indent}📁 {item}/\n")
                print_directory_structure(item_path, output, indent + "    ")
            else:
                file_ext = os.path.splitext(item)[1]
                if file_types_count[file_ext] < MAX_FILES:
                    output.insert(tk.END, f"{indent}📄 {item}\n")
                    file_types_count[file_ext] += 1
                elif file_types_count[file_ext] == MAX_FILES:
                    output.insert(tk.END, f"{indent}... (больше файлов .{file_ext[1:]})\n")
                    file_types_count[file_ext] += 1
    except PermissionError:
        output.insert(tk.END, f"{indent}Доступ запрещен\n")

def print_zip_structure(zip_path, output):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        dir_seen = set()
        file_types_count_per_dir = defaultdict(lambda: defaultdict(int))
        for zip_info in zip_ref.infolist():
            file = zip_info.filename
            parts = file.strip('/').split('/')
            for j in range(len(parts) - 1):
                directory = '/'.join(parts[:j+1])
                if directory not in dir_seen:
                    output.insert(tk.END, "    " * j + f"📁 {parts[j]}/\n")
                    dir_seen.add(directory)
            directory = '/'.join(parts[:-1])
            if zip_info.is_dir():
                continue  # Пропускаем директории
            file_ext = os.path.splitext(parts[-1])[1]
            if file_types_count_per_dir[directory][file_ext] < MAX_FILES:
                output.insert(tk.END, "    " * (len(parts) - 1) + f"📄 {parts[-1]}\n")
                file_types_count_per_dir[directory][file_ext] += 1
            elif file_types_count_per_dir[directory][file_ext] == MAX_FILES:
                output.insert(tk.END, "    " * (len(parts) - 1) + f"... (больше файлов .{file_ext[1:]})\n")
                file_types_count_per_dir[directory][file_ext] += 1

def print_rar_structure(rar_path, output):
    with rarfile.RarFile(rar_path, 'r') as rar_ref:
        dir_seen = set()
        file_types_count_per_dir = defaultdict(lambda: defaultdict(int))
        for rar_info in rar_ref.infolist():
            file = rar_info.filename
            parts = file.strip('/').split('/')
            for j in range(len(parts) - 1):
                directory = '/'.join(parts[:j+1])
                if directory not in dir_seen:
                    output.insert(tk.END, "    " * j + f"📁 {parts[j]}/\n")
                    dir_seen.add(directory)
            directory = '/'.join(parts[:-1])
            if rar_info.isdir():
                continue  # Пропускаем директории
            file_ext = os.path.splitext(parts[-1])[1]
            if file_types_count_per_dir[directory][file_ext] < MAX_FILES:
                output.insert(tk.END, "    " * (len(parts) - 1) + f"📄 {parts[-1]}\n")
                file_types_count_per_dir[directory][file_ext] += 1
            elif file_types_count_per_dir[directory][file_ext] == MAX_FILES:
                output.insert(tk.END, "    " * (len(parts) - 1) + f"... (больше файлов .{file_ext[1:]})\n")
                file_types_count_per_dir[directory][file_ext] += 1

def print_tar_structure(tar_path, output):
    with tarfile.open(tar_path, 'r') as tar_ref:
        dir_seen = set()
        file_types_count_per_dir = defaultdict(lambda: defaultdict(int))
        for member in tar_ref:
            file = member.name
            parts = file.strip('/').split('/')
            for j in range(len(parts) - 1):
                directory = '/'.join(parts[:j+1])
                if directory not in dir_seen:
                    output.insert(tk.END, "    " * j + f"📁 {parts[j]}/\n")
                    dir_seen.add(directory)
            directory = '/'.join(parts[:-1])
            if member.isdir():
                continue  # Пропускаем директории
            file_ext = os.path.splitext(parts[-1])[1]
            if file_types_count_per_dir[directory][file_ext] < MAX_FILES:
                output.insert(tk.END, "    " * (len(parts) - 1) + f"📄 {parts[-1]}\n")
                file_types_count_per_dir[directory][file_ext] += 1
            elif file_types_count_per_dir[directory][file_ext] == MAX_FILES:
                output.insert(tk.END, "    " * (len(parts) - 1) + f"... (больше файлов .{file_ext[1:]})\n")
                file_types_count_per_dir[directory][file_ext] += 1

def browse_file():
    file_path = filedialog.askopenfilename()
    output.delete(1.0, tk.END)
    if file_path.endswith('.zip'):
        output.insert(tk.END, f"Архив: {file_path}\n")
        print_zip_structure(file_path, output)
    elif file_path.endswith('.rar'):
        output.insert(tk.END, f"Архив: {file_path}\n")
        print_rar_structure(file_path, output)
    elif file_path.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
        output.insert(tk.END, f"Архив: {file_path}\n")
        print_tar_structure(file_path, output)
    elif os.path.isdir(file_path):
        output.insert(tk.END, f"Директория: {file_path}\n")
        print_directory_structure(file_path, output)
    else:
        output.insert(tk.END, f"Файл: {file_path}\n")

def save_to_txt():
    text = output.get(1.0, tk.END)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(script_dir, "output.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    tk.messagebox.showinfo("Сохранение завершено", f"Файл сохранен как {txt_path}")

def save_as_image():
    text = output.get(1.0, tk.END)
    lines = text.splitlines()
    padding = 10
    font = ImageFont.load_default()

    # Вычисление ширины и высоты текста
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = font.getbbox(line)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])

    max_line_width = max(line_widths) if line_widths else 0
    line_height = max(line_heights) if line_heights else 0

    width = max_line_width + padding * 2
    height = padding * 2 + len(lines) * (line_height + 5)

    image = Image.new('RGB', (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Рисование текста
    y_text = padding
    for line in lines:
        draw.text((padding, y_text), line, font=font, fill="black")
        y_text += line_height + 5

    # Сохранение изображения
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "output.png")
    image.save(image_path)
    tk.messagebox.showinfo("Сохранение завершено", f"Изображение сохранено как {image_path}")

# Настройка GUI
root = tk.Tk()
root.title("Просмотр структуры файлов")
root.geometry("600x400")

browse_button = tk.Button(root, text="Выбрать файл/директорию", command=browse_file)
browse_button.pack(pady=10)

save_txt_button = tk.Button(root, text="Сохранить в TXT", command=save_to_txt)
save_txt_button.pack(pady=10)

save_button = tk.Button(root, text="Сохранить как изображение", command=save_as_image)
save_button.pack(pady=10)

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
output.pack()

root.mainloop()
