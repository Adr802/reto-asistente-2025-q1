import base64
import fitz  # PyMuPDF
import io
import tempfile
import PyPDF2
import ocrmypdf
import os

class ProcessPDF():
    def __init__(self):
        pass

    def get_pdf_info(self, pdf_base64):
        raw_pdf_data = self._extraer_texto_pdf_a_lista(pdf_base64)
        return self._clean_sensitive_data(raw_pdf_data)

    def _extraer_texto_pdf_a_lista(self, pdf_base64):
        """
        Extrae texto de un PDF, aplicando OCR directamente a los bytes de las imágenes
        en memoria, y devuelve una lista de textos.
        """
        try:
            print("Iniciando el proceso de extracción de texto desde el PDF...")
            
            # Decodificar el base64 a bytes
            pdf_bytes = base64.b64decode(pdf_base64)
            print(f"PDF decodificado, tamaño de bytes: {len(pdf_bytes)}")
            
            # Abrir el PDF desde los bytes
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            total_paginas = len(doc)
            print(f"Total de páginas en el documento PDF: {total_paginas}")
            
            lista_textos = []

            if total_paginas > 0:
                for i in range(1, total_paginas - 1):  # Excluyendo primera y última página
                    print(f"Procesando página {i + 1}/{total_paginas}...")
                    page = doc.load_page(i)
                    text = page.get_text("text")
                    
                    if text.strip():  # Si la página contiene texto
                        print(f"Texto encontrado en página {i + 1}: Texto", text)  # Mostrar los primeros 100 caracteres
                        lista_textos.append(text)
                    else:
                        print(f"No se encontró texto en página {i + 1}, verificando imágenes...")
                        # Si no hay texto, verificar si la página contiene imágenes
                        for img in page.get_images(full=True):
                            print(f"Imagen encontrada en página {i + 1}, procesando...")
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            
                            # Usar io.BytesIO para crear un objeto de archivo en memoria a partir de los bytes
                            imagen_buffer = io.BytesIO(image_bytes)

                            # Usar un directorio temporal personalizado para evitar problemas de permisos
                            try:
                                temp_dir = tempfile.mkdtemp()
                                temp_pdf_path = os.path.join(temp_dir, "temp.pdf")

                                print(f"Aplicando OCR a la imagen de la página {i + 1}...")
                                # Aplicar OCR directamente al buffer de la imagen en memoria y obtener el PDF como bytes
                                ocrmypdf.ocr(imagen_buffer, temp_pdf_path, output_type='pdf', input_file_is_pdf=False, image_dpi=300)

                                with open(temp_pdf_path, 'rb') as temp_pdf:
                                    pdf_bytes = temp_pdf.read()
                                print(f"OCR aplicado correctamente a la imagen de la página {i + 1}.")

                            except PermissionError as e:
                                print(f"Error de permisos al crear archivo temporal: {e}")
                                continue  # Pasar a la siguiente imagen si hay problemas de permisos

                            # Procesar el PDF en bytes y extraer el texto
                            if pdf_bytes:
                                print(f"Extrayendo texto del PDF generado por OCR...")
                                # Usar io.BytesIO para crear un objeto de archivo en memoria para el PDF
                                pdf_buffer = io.BytesIO(pdf_bytes)
                                pdf_reader = PyPDF2.PdfReader(pdf_buffer)
                                num_pages = len(pdf_reader.pages)
                                
                                for page_num in range(num_pages):
                                    page = pdf_reader.pages[page_num]
                                    text = page.extract_text()
                                    lista_textos.append(text)
                                    print(f"Texto extraído de la página {page_num + 1} después del OCR.")
            else:
                print("El documento PDF está vacío o no contiene páginas.")
            
            print("Proceso de extracción finalizado.")
            return lista_textos

        except Exception as e:
            print(f"Error al procesar el PDF: {e}")
            return []
    
    def _clean_sensitive_data(self, lista_de_textos):
        list_clean = []
        for texto_completo in lista_de_textos:
            
            # Normalizar el texto eliminando espacios adicionales
            texto_normalizado = " ".join(texto_completo.split())
            
            # Hacer el split con la cadena "DETALLE DE MOVIMIENTOS" después de la normalización
            partes = texto_normalizado.split("DETALLE DE MOVIMIENTOS")
            
            # La segunda parte de la lista `partes` contiene el texto después de la división
            texto_despues = partes[1] if len(partes) > 1 else ""
            list_clean.append(texto_despues)

        # Unir todos los fragmentos extraídos en una sola cadena
        texto_unido = "".join(list_clean)
        return texto_unido