import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_images(pdf_path, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    

    pdf_document = fitz.open(pdf_path)


    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        output_path = f"{output_folder}/page_{page_num + 1}.png"
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(output_path, "PNG")
        print(f"Página {page_num + 1} salva como {output_path}")

    print("Conversão concluída.")

pdf_path = "pdf.pdf"
output_folder = "imagens"

pdf_to_images(pdf_path, output_folder)
