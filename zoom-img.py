import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

zoom_factor = 2 


def zoom_in(image, coordinates, zoom_factor):
    x, y = coordinates
    width, height = image.size
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)


    zoomed_image = image.resize((new_width, new_height), Image.LANCZOS)

   
    new_x = x * zoom_factor
    new_y = y * zoom_factor

    return zoomed_image, new_x, new_y


def open_image():
    global img, tk_img, original_img, zoomed_img, canvas_img, current_zoom
    file_path = filedialog.askopenfilename()
    if file_path:
        original_img = Image.open(file_path)
        zoomed_img = original_img.copy()
        img = zoomed_img
        current_zoom = 1  # Zoom inicial
        tk_img = ImageTk.PhotoImage(img)
        canvas.config(scrollregion=(0, 0, img.width, img.height))
        canvas_img = canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        canvas.config(width=img.width, height=img.height)


def apply_zoom():
    global img, tk_img, zoomed_img, canvas_img, current_zoom
    x = float(entry_x.get())
    y = float(entry_y.get())
    current_zoom = zoom_factor
    zoomed_img, new_x, new_y = zoom_in(original_img, (x, y), current_zoom)
    img = zoomed_img
    tk_img = ImageTk.PhotoImage(img)
    canvas.delete(canvas_img)
    canvas_img = canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
    canvas.config(scrollregion=(0, 0, img.width, img.height))
    canvas.config(width=img.width, height=img.height)
    canvas.xview_moveto(new_x / img.width)
    canvas.yview_moveto(new_y / img.height)
    lbl_coordinates.config(text=f"Coordenadas: ({x}, {y})")
    lbl_scale.config(text=f"Escala: {current_zoom}")


def zoom(event):
    global img, tk_img, zoomed_img, canvas_img, current_zoom
    scale = 1.1 if event.delta > 0 else 0.9
    current_zoom *= scale
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    zoomed_img, new_x, new_y = zoom_in(original_img, (x, y), current_zoom)
    img = zoomed_img
    tk_img = ImageTk.PhotoImage(img)
    canvas.delete(canvas_img)
    canvas_img = canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
    canvas.config(scrollregion=(0, 0, img.width, img.height))
    canvas.config(width=img.width, height=img.height)
    canvas.xview_moveto(new_x / img.width)
    canvas.yview_moveto(new_y / img.height)
    lbl_scale.config(text=f"Escala: {current_zoom:.2f}")


def move_canvas(event):
    global last_x, last_y
    canvas.scan_dragto(event.x - last_x, event.y - last_y, gain=1)
    last_x, last_y = event.x, event.y


def scroll_start(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y


root = tk.Tk()
root.title("Zoom Dinâmico na Imagem")

frame_main = tk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

canvas_frame = tk.Frame(frame_main)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(canvas_frame, bg='gray')
canvas.pack(fill=tk.BOTH, expand=True)

frame_controls = tk.Frame(frame_main)
frame_controls.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

btn_open = tk.Button(frame_controls, text="Abrir Imagem", command=open_image)
btn_open.pack(pady=5)

lbl_x = tk.Label(frame_controls, text="X:")
lbl_x.pack(pady=5)
entry_x = tk.Entry(frame_controls)
entry_x.pack(pady=5)

lbl_y = tk.Label(frame_controls, text="Y:")
lbl_y.pack(pady=5)
entry_y = tk.Entry(frame_controls)
entry_y.pack(pady=5)

btn_zoom = tk.Button(frame_controls, text="Aplicar Zoom", command=apply_zoom)
btn_zoom.pack(pady=5)

lbl_coordinates = tk.Label(frame_controls, text="Coordenadas: ")
lbl_coordinates.pack(pady=5)

lbl_scale = tk.Label(frame_controls, text="Escala: 1")
lbl_scale.pack(pady=5)

canvas.bind("<ButtonPress-1>", scroll_start)
canvas.bind("<B1-Motion>", move_canvas)
canvas.bind("<MouseWheel>", zoom)

root.mainloop()
