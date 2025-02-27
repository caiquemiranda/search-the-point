import flet as ft
import fitz  # PyMuPDF
import base64
import cv2
import numpy as np
from PIL import Image as PILImage
import io

class PDFViewer:
    def __init__(self):
        self.pdf_document = None
        self.coordinates = []

    def main(self, page: ft.Page):
        page.title = "PDF Viewer"
        page.window_width = 1200
        page.window_height = 900
        page.padding = 20

        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files and e.files[0].path.lower().endswith('.pdf'):
                file_path = e.files[0].path
                load_pdf(file_path)

        def load_pdf(file_path):
            try:
                self.pdf_document = fitz.open(file_path)
                display_current_page()
            except Exception as e:
                print(f"Erro ao carregar PDF: {e}")

        def display_current_page():
            try:
                if self.pdf_document:
                    page_content = self.pdf_document[0]
                    zoom = 2
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page_content.get_pixmap(matrix=mat)
                    
                    img_data = pix.tobytes("png")
                    img = PILImage.open(io.BytesIO(img_data))
                    img_np = np.array(img)

                    # Usar OpenCV para exibir a imagem e capturar cliques
                    cv2.imshow("PDF Image", img_np)
                    cv2.setMouseCallback("PDF Image", on_mouse_click)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            except Exception as e:
                print(f"Erro ao exibir página: {e}")

        def on_mouse_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.coordinates.append((x, y))
                update_coordinates_display()

        def update_coordinates_display():
            coordinates_list.controls = [
                ft.Text(f"X: {coord[0]}, Y: {coord[1]}") for coord in self.coordinates
            ]
            page.update()

        pick_files_dialog = ft.FilePicker(on_result=pick_file_result)

        coordinates_list = ft.Column()

        page.overlay.append(pick_files_dialog)
        page.add(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Abrir PDF",
                        on_click=lambda _: pick_files_dialog.pick_files()
                    ),
                    coordinates_list
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )

if __name__ == '__main__':
    pdf_viewer = PDFViewer()
    ft.app(target=pdf_viewer.main)