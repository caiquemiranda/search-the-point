import flet as ft
import fitz  # PyMuPDF
import os
from PIL import Image
import io

class PDFViewer:
    def __init__(self):
        self.current_page = 0
        self.pdf_document = None
        self.coordinates = []
        self.current_scale = 1.0

    def main(self, page: ft.Page):
        page.title = "PDF Marker"
        page.window_width = 1000
        page.window_height = 800
        page.padding = 20

        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                load_pdf(file_path)

        def load_pdf(file_path):
            self.pdf_document = fitz.open(file_path)
            self.current_page = 0
            self.coordinates = []
            display_current_page()

        def display_current_page():
            if self.pdf_document:
                # Converter página do PDF para imagem
                page_content = self.pdf_document[self.current_page]
                pix = page_content.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes()
                
                # Converter para formato que o Flet pode exibir
                img = Image.frombytes("RGB", [pix.width, pix.height], img_bytes)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                pdf_image.src_base64 = img_byte_arr
                page.update()

        def on_pdf_click(e: ft.TapEvent):
            # Salvar coordenadas do clique
            coordinates = (e.local_x, e.local_y)
            self.coordinates.append({
                'page': self.current_page,
                'x': coordinates[0],
                'y': coordinates[1]
            })
            
            # Adicionar marcador visual
            marker = ft.Container(
                width=10,
                height=10,
                bgcolor=ft.colors.RED,
                border_radius=5,
                left=coordinates[0] - 5,
                top=coordinates[1] - 5,
            )
            pdf_stack.controls.append(marker)
            page.update()

        pick_files_dialog = ft.FilePicker(
            on_result=pick_file_result,
            allow_multiple=False,
            accept="application/pdf"
        )

        pdf_image = ft.Image(
            width=800,
            height=600,
            fit=ft.ImageFit.CONTAIN,
        )

        pdf_stack = ft.Stack(
            controls=[pdf_image],
            width=800,
            height=600,
        )

        pdf_container = ft.GestureDetector(
            content=pdf_stack,
            on_tap=on_pdf_click,
        )

        page.overlay.append(pick_files_dialog)
        page.add(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Abrir PDF",
                        on_click=lambda _: pick_files_dialog.pick_files()
                    )
                ]
            ),
            pdf_container
        )

if __name__ == '__main__':
    pdf_viewer = PDFViewer()
    ft.app(target=pdf_viewer.main) 