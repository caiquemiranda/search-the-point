import flet as ft
import fitz  # PyMuPDF
import os
import io
import base64

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
            if e.files and e.files[0].path.lower().endswith('.pdf'):
                file_path = e.files[0].path
                load_pdf(file_path)
            else:
                # Opcional: mostrar mensagem de erro
                page.show_snack_bar(ft.SnackBar(content=ft.Text("Por favor, selecione um arquivo PDF")))

        def load_pdf(file_path):
            self.pdf_document = fitz.open(file_path)
            self.current_page = 0
            self.coordinates = []
            display_current_page()

        def display_current_page():
            if self.pdf_document:
                # Converter página do PDF para imagem
                page_content = self.pdf_document[self.current_page]
                # Aumentamos a escala para melhor qualidade
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page_content.get_pixmap(matrix=mat)
                
                # Converter diretamente para PNG
                png_data = pix.tobytes("png")
                
                # Atualizar a imagem usando base64
                pdf_image.src_base64 = base64.b64encode(png_data).decode()
                
                # Limpar marcadores ao mudar de página
                pdf_stack.controls = [pdf_image]
                page.update()

        def on_pdf_click(e: ft.TapEvent):
            # Corrigindo para usar as coordenadas corretas do evento
            coordinates = (e.global_x, e.global_y)
            
            # Ajustar coordenadas relativas ao container
            container_left = pdf_container.get_offset_x()
            container_top = pdf_container.get_offset_y()
            
            x = coordinates[0] - container_left
            y = coordinates[1] - container_top
            
            self.coordinates.append({
                'page': self.current_page,
                'x': x,
                'y': y
            })
            
            # Adicionar marcador visual
            marker = ft.Container(
                width=10,
                height=10,
                bgcolor=ft.colors.RED,
                border_radius=5,
                left=x - 5,
                top=y - 5,
            )
            pdf_stack.controls.append(marker)
            page.update()

        pick_files_dialog = ft.FilePicker(
            on_result=pick_file_result
        )

        pdf_image = ft.Image(
            width=900,
            height=800,
            fit=ft.ImageFit.CONTAIN,
            border_radius=10
        )

        pdf_stack = ft.Stack(
            controls=[pdf_image],
            width=900,
            height=800,
        )

        # Criando um container centralizado para o PDF
        pdf_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.GestureDetector(
                            content=pdf_stack,
                            on_tap=on_pdf_click,
                        ),
                        alignment=ft.alignment.center
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            expand=True
        )

        page.overlay.append(pick_files_dialog)
        page.add(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Abrir PDF",
                        on_click=lambda _: pick_files_dialog.pick_files()
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            pdf_container
        )

if __name__ == '__main__':
    pdf_viewer = PDFViewer()
    ft.app(target=pdf_viewer.main) 