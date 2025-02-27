import flet as ft
import fitz  # PyMuPDF
import base64
import cv2
import numpy as np
import io

class PDFViewer:
    def __init__(self):
        self.pdf_document = None
        self.current_page = 0
        self.zoom_level = 2.0
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
                    page_content = self.pdf_document[self.current_page]
                    mat = fitz.Matrix(self.zoom_level, self.zoom_level)
                    pix = page_content.get_pixmap(matrix=mat)
                    
                    img_data = pix.tobytes("png")
                    img_np = np.frombuffer(img_data, np.uint8)
                    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                    # Exibir imagem e capturar cliques
                    cv2.imshow("PDF Image", img)
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
            coordinates_table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(i + 1))),
                        ft.DataCell(ft.Text(f"X: {coord[0]}")),
                        ft.DataCell(ft.Text(f"Y: {coord[1]}")),
                    ]
                )
                for i, coord in enumerate(self.coordinates)
            ]
            page.update()

        pick_files_dialog = ft.FilePicker(on_result=pick_file_result)

        coordinates_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("X")),
                ft.DataColumn(ft.Text("Y")),
            ],
            rows=[],
        )

        page.overlay.append(pick_files_dialog)
        page.add(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Abrir PDF",
                        on_click=lambda _: pick_files_dialog.pick_files()
                    ),
                    coordinates_table
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )

if __name__ == '__main__':
    pdf_viewer = PDFViewer()
    ft.app(target=pdf_viewer.main)