import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def zoom_in(image, coordinates, zoom_factor=2):
    x, y = coordinates
    box_size = 100  # Tamanho da área a ser ampliada
    x1, y1 = max(0, x - box_size), max(0, y - box_size)
    x2, y2 = min(image.width, x + box_size), min(image.height, y + box_size)

    cropped_area = image.crop((x1, y1, x2, y2))
    zoomed_area = cropped_area.resize(
        (cropped_area.width * zoom_factor, cropped_area.height * zoom_factor), Image.LANCZOS)

    zoomed_image = Image.new('RGB', image.size)
    center_x, center_y = x, y
    offset_x, offset_y = center_x - \
        (zoomed_area.width // 2), center_y - (zoomed_area.height // 2)

    zoomed_image.paste(image, (0, 0))
    zoomed_image.paste(zoomed_area, (offset_x, offset_y))

    return zoomed_image


def open_image():
    global img, tk_img, original_img
    file_path = filedialog.askopenfilename()
    if file_path:
        original_img = Image.open(file_path)
        img = original_img.copy()
        tk_img = ImageTk.PhotoImage(img)
        canvas.config(width=img.width, height=img.height)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        frame_coords.pack(side=tk.LEFT, padx=10, pady=10)


def apply_zoom():
    global img, tk_img, original_img
    x = int(entry_x.get())
    y = int(entry_y.get())
    img = zoom_in(original_img, (x, y))
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)


root = tk.Tk()
root.title("Zoom na Imagem")

frame_main = tk.Frame(root)
frame_main.pack()

canvas = tk.Canvas(frame_main)
canvas.pack(side=tk.LEFT)

frame_coords = tk.Frame(frame_main)
frame_coords.pack_forget()  # Inicialmente escondido

btn_open = tk.Button(root, text="Abrir Imagem", command=open_image)
btn_open.pack(pady=5)

tk.Label(frame_coords, text="X:").grid(row=0, column=0, padx=5, pady=5)
entry_x = tk.Entry(frame_coords)
entry_x.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_coords, text="Y:").grid(row=1, column=0, padx=5, pady=5)
entry_y = tk.Entry(frame_coords)
entry_y.grid(row=1, column=1, padx=5, pady=5)

btn_zoom = tk.Button(frame_coords, text="Aplicar Zoom", command=apply_zoom)
btn_zoom.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
