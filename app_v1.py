import warnings
warnings.filterwarnings('ignore')

import flet as ft
import fitz  # PyMuPDF
import cv2
import numpy as np
import base64
import io
import csv
from datetime import datetime

def main(page: ft.Page):
    page.title = "PDF Coordinate Picker"
    page.window_width = 1200
    page.window_height = 800

    # Variáveis de estado
    coordinates = []
    current_pdf_name = ""  # Para usar no nome do arquivo exportado

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("X")),
            ft.DataColumn(ft.Text("Y")),
        ],
        width=300,
    )

    def update_table():
        data_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(i + 1))),
                    ft.DataCell(ft.Text(str(x))),
                    ft.DataCell(ft.Text(str(y)))
                ]
            ) for i, (x, y) in enumerate(coordinates)
        ]
        page.update()

    def export_coordinates():
        if not coordinates:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Não há coordenadas para exportar")))
            return

        try:
            # Criar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coordenadas_{current_pdf_name}_{timestamp}.csv"
            
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'X', 'Y'])  # Cabeçalho
                for i, (x, y) in enumerate(coordinates, 1):
                    writer.writerow([i, x, y])
            
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Coordenadas exportadas para {filename}")))
        except Exception as e:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Erro ao exportar: {str(e)}")))

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coordinates.append((x, y))
            update_table()

    def convert_pdf_to_image(e: ft.FilePickerResultEvent):
        if not e.files:
            return
            
        try:
            pdf_path = e.files[0].path
            global current_pdf_name
            current_pdf_name = e.files[0].name.split('.')[0]  # Nome do PDF sem extensão
            
            pdf_document = fitz.open(pdf_path)
            
            # Converter primeira página para imagem
            page_content = pdf_document[0]
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            pix = page_content.get_pixmap(matrix=mat)
            
            # Converter para formato OpenCV
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
            
            # Criar janela OpenCV
            cv2.namedWindow("PDF Image")
            cv2.setMouseCallback("PDF Image", mouse_callback)
            
            while True:
                # Mostrar imagem com pontos marcados
                img_display = img_array.copy()
                for i, (cx, cy) in enumerate(coordinates):
                    cv2.circle(img_display, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(img_display, str(i+1), (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                cv2.imshow("PDF Image", img_display)
                
                # Sair com ESC
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
            
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"Erro ao converter PDF: {e}")

    # Componente para upload de arquivo
    file_picker = ft.FilePicker(
        on_result=convert_pdf_to_image
    )
    page.overlay.append(file_picker)

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Carregar PDF",
                            on_click=lambda _: file_picker.pick_files()
                        ),
                        ft.ElevatedButton(
                            "Exportar Coordenadas",
                            on_click=lambda _: export_coordinates()
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Container(
                    content=ft.Column(
                        [data_table],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    bgcolor="#D3D3D3",
                    padding=10,
                    border_radius=5,
                    height=700,  # Altura fixa do container
                    width=300,   # Largura fixa do container
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)