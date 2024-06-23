import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_images(pdf_path, output_folder):
    # Verificar e criar a pasta de saída, se necessário
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Abrir o documento PDF
    pdf_document = fitz.open(pdf_path)

    # Iterar por todas as páginas do PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # Criar o caminho para a imagem de saída
        output_path = f"{output_folder}/page_{page_num + 1}.png"
        
        # Salvar a imagem
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(output_path, "PNG")
        print(f"Página {page_num + 1} salva como {output_path}")

    print("Conversão concluída.")

# Caminho do PDF e pasta de saída
pdf_path = "pdf.pdf"
output_folder = "imagens"

# Converter PDF em imagens
pdf_to_images(pdf_path, output_folder)
