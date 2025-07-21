import pyautogui as pg
import os
from find_image import find_and_click_image

# import pyautogui as pg
# pg.displayMousePosition()

def main():

    # salvar no notion
    pg.moveTo(935,55,duration=0.5)
    pg.click()
    pg.moveTo(688,172,duration=0.5)
    pg.sleep(1)
    pg.click()
    
    # Copiar o nome do artigo
    # pg.moveTo(94,376,duration=0.5)
    # pg.click(clicks=3)
    # with pg.hold('ctrl'):
    #     pg.press('c')
    # pg.sleep(1)

    # Abrir pdf do arquivo
    status = find_and_click_image("ieee_button.png", confidence=0.8, grayscale=True, message="Tentando encontrar a imagem 1")
    pg.sleep(30)

    # Download do arquivo
    pg.moveTo(1316,92,duration=0.5)
    pg.click()
    pg.sleep(1)

    #Salvar arquivo
    pg.moveTo(2448,22,duration=0.5)
    pg.click()
    pg.sleep(1)

    with pg.hold('ctrl'):
        pg.press('w')
    pg.sleep(1)


if __name__ == "__main__":

    count = 0
    while True:
        main()
        count+=1
        if count%5==0:
            pg.alert(text=f'{count+1} artigos baixados!', title='Atenção', button='OK')
            if pg.confirm(text='Deseja continuar?', title='Continuar?', buttons=['Sim', 'Não']) == 'Não':
                break
    pg.alert(text='Processo finalizado!', title='Finalizado', button='OK')

    