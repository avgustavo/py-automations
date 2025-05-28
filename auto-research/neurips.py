import pyautogui as pg
import os
from find_image import find_and_click_image

# import pyautogui as pg
# pg.displayMousePosition()

def main():

    find_and_click_image("neurips_button.png", confidence=0.8, grayscale=True, message="Tentando encontrar a imagem 1")
    
    # Copiar o nome do artigo
    pg.moveTo(120,204,duration=0.5)
    pg.click(clicks=3)
    with pg.hold('ctrl'):
        pg.press('c')
    pg.sleep(1)

    # Abrir pdf do arquivo
    status = find_and_click_image("neurips2.png", confidence=0.8, grayscale=True, message="Tentando encontrar a imagem 1")
    pg.sleep(8)

    # Download do arquivo
    pg.moveTo(1870,130,duration=0.5)
    pg.click()
    pg.sleep(2)
    # RENOMEAR ARQUIVO
    with pg.hold('ctrl'):
        pg.press('v')
    pg.sleep(1)

    #Salvar arquivo
    pg.moveTo(1480,195,duration=0.5)
    pg.click()
    pg.sleep(1)

    with pg.hold('ctrl'):
        pg.press('w')
    pg.sleep(1)


if __name__ == "__main__":
    main()
    # count = 0
    # while True:
    #     main()
    #     count+=1
    #     if count%2==0:
    #         pg.alert(text=f'{count+1} artigos baixados!', title='Atenção', button='OK')
    #         if pg.confirm(text='Deseja continuar?', title='Continuar?', buttons=['Sim', 'Não']) == 'Não':
    #             break
    # pg.alert(text='Processo finalizado!', title='Finalizado', button='OK')

    