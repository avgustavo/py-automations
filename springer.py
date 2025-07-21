import pyautogui as pg
import os
from find_image import find_and_click_image

# import pyautogui as pg
# pg.displayMousePosition()

def main():

    # Download do arquivo
    status = find_and_click_image("download_button.png", confidence=0.8, grayscale=True, message="Tentando encontrar a imagem 1")
    pg.sleep(3)
    if(status == True):
        # Voltar para a aba
        pg.moveTo(27,152,duration=0.5)
        pg.click()

        pg.sleep(1)
        # salvar no notion
        pg.moveTo(935,55,duration=2)
        pg.click()
        pg.moveTo(688,172,duration=0.5)
        pg.sleep(1)
        pg.click()

        # Copiar o nome do artigo
        pg.moveTo(95,298,duration=0.5)
        pg.click(clicks=3)

        with pg.hold('ctrl'):
            pg.press('c')
        pg.sleep(1)
        # Abrir a pasta de downloads
        pg.moveTo(620,745,duration=0.5)
        pg.sleep(0.5)
        pg.click()
        # Clique no arquivo
        pg.moveTo(252,149,duration=0.5)
        pg.click()

        # Renomear o arquivo
        pg.press('f2')

        with pg.hold('ctrl'):
            pg.press('v')
        pg.sleep(1)

        pg.moveTo(328,340,duration=0.5)
        pg.click()

        # Minimizar a janela
        pg.moveTo(1265,57,duration=0.5)
        pg.click()

        # Fechar as duas abas do navegador
        pg.moveTo(11,140,duration=0.5)
        pg.click()
        pg.sleep(1)
        pg.click()
    else:
        # Fechar as duas abas do navegador
        pg.moveTo(11,140,duration=0.5)
        pg.click()


if __name__ == "__main__":

    while True:
        main()
        if pg.confirm(text='Deseja continuar?', title='Continuar?', buttons=['Sim', 'Não']) == 'Não':
            break
    pg.alert(text='Processo finalizado!', title='Finalizado', button='OK')

    