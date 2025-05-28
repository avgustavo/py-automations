import pyautogui as pg
import os

def find_and_click_image(image_path, confidence=0.8, grayscale=True, message=""):
    """Encontra uma imagem na tela e clica nela."""
    try:
        location = pg.locateCenterOnScreen(image_path, confidence=confidence, grayscale=grayscale)
        if location:
            print(f"Imagem '{os.path.basename(image_path)}' encontrada em {location}. {message}")
            pg.moveTo(location, duration=0.2)
            pg.click()
            pg.sleep(1)
            return True
        else:
            print(f"Imagem '{os.path.basename(image_path)}' não encontrada na tela. {message}")
            return False
    except Exception as e:
        print(f"Erro ao tentar encontrar/clicar na imagem '{os.path.basename(image_path)}': {e}")
        if grayscale: # Tentar novamente sem grayscale se a primeira tentativa falhou
            try:
                print("Tentando novamente sem grayscale...")
                location = pg.locateCenterOnScreen(image_path, confidence=confidence, grayscale=False)
                if location:
                    print(f"Imagem '{os.path.basename(image_path)}' encontrada (sem grayscale) em {location}. {message}")
                    pg.moveTo(location, duration=0.2)
                    pg.click()
                    pg.sleep(1)
                    return True
            except Exception as e2:
                 print(f"Nova falha ao tentar encontrar/clicar na imagem '{os.path.basename(image_path)}': {e2}")
        return False