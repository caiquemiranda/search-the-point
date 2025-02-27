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
        self.current_image = None
        self.markers = []
        self.pdf_stack = ft.Stack(
            width=800,
            height=700,
        )

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
                try:
                    page_content = self.pdf_document[self.current_page]
                    zoom = 2
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page_content.get_pixmap(matrix=mat)
                    
                    # Converter para PNG
                    png_data = pix.tobytes("png")
                    img_base64 = base64.b64encode(png_data).decode()
                    
                    # Atualizar imagem
                    self.current_image = ft.Image(
                        src=f"data:image/png;base64,{img_base64}",
                        width=800,
                        height=700,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=10,
                    )
                    
                    # Atualizar stack
                    self.pdf_stack.controls = [self.current_image]
                    self.pdf_stack.controls.extend(self.markers)
                    page.update()
                except Exception as e:
                    print(f"Erro ao exibir página: {e}")

        def on_pdf_click(e: ft.TapEvent):
            try:
                # Ajustar coordenadas
                x = e.global_x - pdf_container.get_offset_x()
                y = e.global_y - pdf_container.get_offset_y()
                
                # Salvar coordenadas
                self.coordinates.append({
                    'page': self.current_page,
                    'x': x,
                    'y': y
                })
                
                # Criar marcador
                marker = ft.Container(
                    width=10,
                    height=10,
                    bgcolor=ft.Colors.RED,
                    border_radius=5,
                    left=x - 5,
                    top=y - 5,
                )
                
                # Adicionar à lista de marcadores
                self.markers.append(marker)
                self.pdf_stack.controls.append(marker)
                page.update()
            except Exception as e:
                print(f"Erro ao adicionar marcador: {e}")

        pick_files_dialog = ft.FilePicker(
            on_result=pick_file_result
        )

        # Container do PDF com borda
        pdf_stack_container = ft.Container(
            content=self.pdf_stack,
            border=ft.border.all(2, ft.Colors.BLUE_GREY_400),
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            margin=ft.margin.only(bottom=50),
        )

        # Container principal centralizado
        pdf_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.GestureDetector(
                            content=pdf_stack_container,
                            on_tap=on_pdf_click,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=20, bottom=20),
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            alignment=ft.alignment.center,
            expand=True,
            margin=ft.margin.all(30),
        )

        # Container para o botão com padding
        button_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Abrir PDF",
                        on_click=lambda _: pick_files_dialog.pick_files()
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=20, bottom=20),
        )

        page.overlay.append(pick_files_dialog)
        page.add(
            button_container,
            pdf_container
        )

        # Atualizar a página principal
        page.bgcolor = ft.Colors.BLUE_GREY_50
        page.padding = 20

if __name__ == '__main__':
    pdf_viewer = PDFViewer()
    ft.app(target=pdf_viewer.main) 