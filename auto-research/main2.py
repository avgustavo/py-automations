import pyautogui
import pyperclip
import time
import os
import shutil # Para mover e renomear arquivos

# --- Configurações Iniciais ---
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads") # Ajuste se sua pasta de downloads for outra
TARGET_PDF_FOLDER = "tcc" # Pasta onde os PDFs renomeados serão salvos
OUTPUT_TEXT_FILE = "artigos_coletados.txt" # Nome do arquivo de texto para salvar os dados

if not os.path.exists(TARGET_PDF_FOLDER):
    os.makedirs(TARGET_PDF_FOLDER)

# --- Funções Auxiliares ---

def append_to_text_file(filepath, title, link):
    """Adiciona o título e o link a um arquivo de texto."""
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"Título: {title}\n")
            f.write(f"Link: {link}\n")
            f.write("-" * 30 + "\n") # Separador
        print(f"'{title}' adicionado ao arquivo '{filepath}'.")
    except Exception as e:
        print(f"Erro ao escrever no arquivo de texto '{filepath}': {e}")

def get_active_window_title():
    """Pega o título da janela ativa (pode ajudar a confirmar o foco)."""
    try:
        active_window = pyautogui.getActiveWindow()
        if active_window:
            return active_window.title
        return "Nenhuma janela ativa"
    except Exception as e:
        print(f"Erro ao pegar título da janela: {e}")
        return "Erro"

def click_at_location(x, y, message=""):
    """Clica em uma coordenada específica."""
    print(f"Clicando em ({x}, {y}). {message}")
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()
    time.sleep(1) # Pequena pausa após o clique

def find_and_click_image(image_path, confidence=0.8, grayscale=True, message=""):
    """Encontra uma imagem na tela e clica nela."""
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=grayscale)
        if location:
            print(f"Imagem '{os.path.basename(image_path)}' encontrada em {location}. {message}")
            pyautogui.moveTo(location, duration=0.2)
            pyautogui.click()
            time.sleep(1)
            return True
        else:
            print(f"Imagem '{os.path.basename(image_path)}' não encontrada na tela. {message}")
            return False
    except Exception as e:
        print(f"Erro ao tentar encontrar/clicar na imagem '{os.path.basename(image_path)}': {e}")
        if grayscale: # Tentar novamente sem grayscale se a primeira tentativa falhou
            try:
                print("Tentando novamente sem grayscale...")
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=False)
                if location:
                    print(f"Imagem '{os.path.basename(image_path)}' encontrada (sem grayscale) em {location}. {message}")
                    pyautogui.moveTo(location, duration=0.2)
                    pyautogui.click()
                    time.sleep(1)
                    return True
            except Exception as e2:
                 print(f"Nova falha ao tentar encontrar/clicar na imagem '{os.path.basename(image_path)}': {e2}")
        return False

def get_latest_downloaded_file(download_path, initial_files):
    """Retorna o nome do arquivo mais recente baixado."""
    # Espera um pouco para o download começar e aparecer no sistema de arquivos
    time.sleep(5) # Ajuste este tempo conforme a velocidade do seu download
    current_files = set(os.listdir(download_path))
    new_files = current_files - initial_files
    if new_files:
        # Pega o arquivo mais recente baseado no tempo de modificação
        latest_file = max([os.path.join(download_path, f) for f in new_files], key=os.path.getmtime)
        return latest_file
    return None

# --- Script Principal ---
def main():
    print("Preparando para automatizar...")
    print(f"As informações dos artigos serão salvas em '{OUTPUT_TEXT_FILE}'.")
    print(f"Os PDFs baixados serão salvos em '{TARGET_PDF_FOLDER}'.")
    print("Por favor, certifique-se de que a janela do navegador com a aba do artigo está ativa.")
    print("O script começará em 5 segundos...")
    time.sleep(5)

    num_artigos = int(input("Quantos artigos (abas) você vai processar? "))

    for i in range(num_artigos):
        print(f"\n--- Processando Artigo {i+1} de {num_artigos} ---")
        print(">>> POR FAVOR, MUDE PARA A ABA DO ARTIGO E COLOQUE O FOCO NA JANELA DO NAVEGADOR <<<")
        input("Pressione Enter quando estiver pronto para o artigo atual...")

        print(f"Janela ativa: {get_active_window_title()}")
        time.sleep(1) # Dá tempo para você soltar a tecla Enter e o foco se estabelecer

        article_title = "Nao_Identificado" # Valor padrão
        article_link = "Nao_Identificado" # Valor padrão

        # 1. Copiar o Título do Artigo
        print("Tentando copiar o título...")
        input(">>> Selecione o título do artigo na página e pressione Enter... <<<")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        pyperclip_content = pyperclip.paste()
        if pyperclip_content: # Verifica se algo foi copiado
            article_title = pyperclip_content.strip()
        else:
            article_title = f"Artigo_Sem_Titulo_{time.strftime('%Y%m%d_%H%M%S')}"
        print(f"Título copiado/definido: {article_title}")


        # 2. Copiar o Link (URL)
        print("Tentando copiar o link da URL...")
        pyautogui.hotkey('alt', 'd') # Atalho comum para focar na barra de endereço (Windows/Linux)
                                     # No macOS, pode ser 'command', 'l'
        # pyautogui.click(x=600, y=60) # Alternativa: AJUSTE Coordenada da barra de endereço
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c') # No macOS, seria 'command', 'c'
        time.sleep(0.5)
        article_link = pyperclip.paste()
        print(f"Link copiado: {article_link}")

        # 3. Salvar no arquivo de texto local
        append_to_text_file(OUTPUT_TEXT_FILE, article_title, article_link)

        # 4. Encontrar o botão de Download do PDF e Baixar
        print("Tentando encontrar e clicar no botão de download do PDF...")
        button_images = ['download_button.png', 'pdf_icon.png', 'download_pdf.png', 'baixar_pdf.png'] # Adicione mais nomes de imagens se necessário
        download_clicked = False
        for img_name in button_images:
            if os.path.exists(img_name):
                if find_and_click_image(img_name, confidence=0.7, message=f"Procurando por '{img_name}'"):
                    download_clicked = True
                    break
            else:
                print(f"Arquivo de imagem de referência '{img_name}' não encontrado. Pulando esta imagem.")

        if not download_clicked:
            print("Não foi possível clicar no botão de download automaticamente usando as imagens fornecidas.")
            print(">>> Você precisará clicar manualmente no botão de download do PDF. <<<")
            input("Clique manualmente no botão de download e pressione Enter após o início do download...")
            time.sleep(5) # Dá um tempo para o download começar

        # 5. Renomear o PDF
        print("Aguardando o download do PDF...")
        initial_files_in_download = set()
        if os.path.exists(DOWNLOADS_FOLDER): # Verifica se a pasta de downloads existe
            initial_files_in_download = set(os.listdir(DOWNLOADS_FOLDER))
        else:
            print(f"AVISO: A pasta de downloads '{DOWNLOADS_FOLDER}' não foi encontrada. Não será possível monitorar downloads.")


        downloaded_pdf_path = None
        # Tenta por um tempo encontrar o novo arquivo
        # Aumentar o tempo de espera total se os downloads forem grandes/lentos
        for attempt in range(12): # Tenta por até 120 segundos (12 * 10s)
            if not os.path.exists(DOWNLOADS_FOLDER): break # Para de tentar se a pasta não existe
            downloaded_pdf_path = get_latest_downloaded_file(DOWNLOADS_FOLDER, initial_files_in_download)
            if downloaded_pdf_path and downloaded_pdf_path.lower().endswith(".pdf"):
                print(f"PDF encontrado: {downloaded_pdf_path}")
                break
            if attempt < 11 : # Evita imprimir na última tentativa se não encontrar
                print(f"Ainda procurando pelo PDF baixado (tentativa {attempt+1}/12)...")
            time.sleep(10) # Intervalo entre as verificações

        if downloaded_pdf_path and downloaded_pdf_path.lower().endswith(".pdf"):
            safe_title = "".join([c for c in article_title if c.isalnum() or c in (' ', '.', '_', '-')]).rstrip()
            safe_title = safe_title.replace(' ', '_')
            if not safe_title:
                safe_title = f"Artigo_baixado_{time.strftime('%Y%m%d_%H%M%S')}"
            if len(safe_title) > 150: # Limita o tamanho do nome do arquivo
                safe_title = safe_title[:150]

            new_pdf_name = f"{safe_title}.pdf"
            new_pdf_path = os.path.join(TARGET_PDF_FOLDER, new_pdf_name)

            try:
                print(f"Movendo '{downloaded_pdf_path}' para '{new_pdf_path}'")
                shutil.move(downloaded_pdf_path, new_pdf_path)
                print(f"PDF baixado e renomeado para: {new_pdf_path}")
            except Exception as e:
                print(f"Erro ao mover/renomear o PDF: {e}")
                print(f"O PDF pode estar em: {downloaded_pdf_path}")
        else:
            print(f"Não foi possível encontrar o PDF baixado na pasta '{DOWNLOADS_FOLDER}' ou o arquivo não é um PDF.")
            print("Verifique sua pasta de Downloads. O arquivo pode precisar ser renomeado manualmente.")

        if i < num_artigos - 1:
             print("Prepare-se para o próximo artigo...")
             time.sleep(2)

    print(f"\n--- Processamento Concluído ---")
    print(f"Os dados dos artigos foram salvos em: {os.path.abspath(OUTPUT_TEXT_FILE)}")
    print(f"Os PDFs foram salvos em: {os.path.abspath(TARGET_PDF_FOLDER)}")

if __name__ == '__main__':
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5

    screenWidth, screenHeight = pyautogui.size()
    print(f"Resolução da tela: {screenWidth}x{screenHeight}")
    print("Para encontrar coordenadas (se necessário), use no console Python:")
    print("import pyautogui")
    print("pyautogui.displayMousePosition()")
    print("(Mova o mouse para a posição desejada e veja as coordenadas no console)")
    print("-" * 50)

    main()