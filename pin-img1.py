import tkinter as tk
from PIL import Image, ImageTk, ImageDraw


class ZoomPanImage:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Clique na imagem para obter as coordenadas")

        self.image = Image.open(image_path)
        self.original_image = self.image.copy()
        self.width, self.height = self.image.size
        self.zoom_factor = 1.0
        self.click_count = 0
        self.coordinates = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(
            self.frame, width=self.width, height=self.height)
        self.canvas.pack()

        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.tk_image)

        self.coord_frame = tk.Frame(self.root)
        self.coord_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.coord_listbox = tk.Listbox(self.coord_frame, width=30)
        self.coord_listbox.pack(fill=tk.Y)

        self.radius = 5 

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        self.canvas.bind("<ButtonPress-2>", self.on_pan_start)
        self.canvas.bind("<B2-Motion>", self.on_pan_move)

        self.canvas.bind("<ButtonPress-3>", self.on_pan_start)
        self.canvas.bind("<B3-Motion>", self.on_pan_move)

        self.pan_start_x = 0
        self.pan_start_y = 0
        self.canvas_x = 0
        self.canvas_y = 0

        self.root.mainloop()

    def on_click(self, event):
        x = self.canvas.canvasx(event.x) / self.zoom_factor
        y = self.canvas.canvasy(event.y) / self.zoom_factor
        self.click_count += 1
        coordinate_info = f'Click {self.click_count} - Coordenadas: ({x:.2f}, {y:.2f})'
        print(coordinate_info)
        self.coordinates.append(coordinate_info)
        self.coord_listbox.insert(tk.END, coordinate_info)
        draw = ImageDraw.Draw(self.original_image)
        draw.ellipse((x - self.radius / self.zoom_factor, y - self.radius / self.zoom_factor,
                      x + self.radius / self.zoom_factor, y + self.radius / self.zoom_factor), fill='red', outline='black')
        self.update_image()

        
        self.canvas.create_text(
            event.x, event.y, text=f'({x:.2f}, {y:.2f})', fill='red', anchor=tk.NW)

    def on_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.zoom_factor *= factor
        self.image = self.original_image.resize(
            (int(self.width * self.zoom_factor), int(self.height * self.zoom_factor)), Image.LANCZOS)
        self.update_image()

    def on_pan_start(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_pan_move(self, event):
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.canvas.move(self.image_id, dx, dy)
        self.canvas_x += dx
        self.canvas_y += dy
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def update_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.itemconfig(self.image_id, image=self.tk_image)
        self.canvas.coords(self.image_id, self.canvas_x, self.canvas_y)


# imagem
image_path = "imagens/page_1.png"

zoom_pan_image = ZoomPanImage(image_path)
print('Coordenadas obtidas:')
for coordinate in zoom_pan_image.coordinates:
    print(coordinate)
