from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path
import pygame
import pyautogui
import base64
from dotenv import load_dotenv
import threading
from tab_manager import tab_manager_function


os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), "chromium")

# Obtém o diretório atual onde o arquivo "Notificar.py" está localizado
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define o caminho para a pasta com os áudios
audio_folder_path = os.path.join(current_directory, 'static')


def main():

    pygame.mixer.init()

    # Obtém o local do audio para Requisições para Equipe Técnica
    audioAreaTecnica = os.path.join('static', 'Nova requisicao para area tecnica.mp3')
    audio_pathAreaTecnica = Path(audioAreaTecnica).resolve().as_posix()

    # Obtém o local do audio para Requisições para Equipe de Logística
    audioLogistica = os.path.join('static', 'Nova requisicao para logistica.mp3')
    audio_pathLogistica = Path(audioLogistica).resolve().as_posix()

    # Obtém o local do audio para Requisições da Unimed Lar
    audioUnimedLar = os.path.join('static', 'Nova requisicao na base da Unimed Lar.mp3')
    audio_pathUnimedLar = Path(audioUnimedLar).resolve().as_posix()

    # Obtém o local do audio para Requisições das Clínicas
    audioClinicas = os.path.join('static', 'Nova requisicao na base das Clinicas.mp3')
    audio_pathClinicas = Path(audioClinicas).resolve().as_posix()

    # Obtém o local do audio para Requisições dos Laboratórios
    audioLaboratorios = os.path.join('static', 'Nova requisicao na base dos laboratorios.mp3')
    audio_pathLaboratorios = Path(audioLaboratorios).resolve().as_posix()

    # Obtém o local do audio para Requisições da Unimed Urgente
    audioUnimedUrgente = os.path.join('static','Nova requisicao na base da Unimed Urgente.mp3')
    audio_pathUnimedUrgente = Path(audioUnimedUrgente).resolve().as_posix()

    # Obtém o local do audio para Requisições da Medicina Preventiva
    audioMedPrev = os.path.join('static', 'Nova requisicao na base da medicina preventiva.mp3')
    audio_pathMedPrev = Path(audioMedPrev).resolve().as_posix()

    # Obtém o local do audio para avisar que a requisição ainda não foi atendida
    audioAviso5Minutos = os.path.join('static', 'Requisicao_5_minutos.mp3')
    audio_path_5_minutes = Path(audioAviso5Minutos).resolve().as_posix()

    # Obtém o local do audio para avisar que a meta foi atingida
    audioMetaAtingida = os.path.join('static', 'MetaAtingida.mp3')
    audio_path_metaAtingida = Path(audioMetaAtingida).resolve().as_posix()


    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    def decrypt_password(encrypted_password):
        # Decodifica a senha usando base64
        decrypted_password = base64.b64decode(encrypted_password.encode()).decode()
        return decrypted_password

    # Lê a senha criptografada do arquivo .env
    s_criptografada = os.getenv("S_CRIPTOGRAFADA")

    # Decodifica a senha para uso
    s = decrypt_password(s_criptografada) 

    # Declaração da variável context fora do bloco with
    context = None    

    #Inicia a quantidade de requisição como none
    requisicao = None

    # Variáveis adicionais para controlar a reprodução do áudio
    reproduzir_audio = False
    ultimo_valor_reproduzido = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Abre a página
        page = context.new_page()
        page.set_viewport_size({"width": 0, "height": 0})
        # Pressiona a tecla F11 para entrar em modo de tela cheia
        pyautogui.press('F11')
        page.goto("https://unimedfortaleza.neovero.com/login")
        time.sleep(3)

        # Preenche as credenciais de login
        page.fill('input[type="text"]', "painel.ec")
        time.sleep(3)
        page.fill('input[type="password"]', s)
        time.sleep(2)
        page.click('button[type="submit"]')
        time.sleep(3)

        # Aguarda a página carregar
        page.wait_for_load_state("load")

        page.wait_for_selector('[data-empresaid="1"]', state="visible")
        page.click('[data-empresaid="1"]')

        # Aguarda a página carregar
        page.wait_for_load_state("load")
        time.sleep(85)

        # Abrir uma nova aba com o dashboard Geral
        pageDashboard1 = context.new_page()
        pageDashboard1.set_viewport_size({"width": 0, "height": 0})
        pyautogui.press('F11')
        pageDashboard1.goto("https://unimedfortaleza.neovero.com/dashboards?id=15&fullscreen=S&mobile=N")
        time.sleep(3)

        # Abrir uma nova aba com o dashboard Preventivas do mês
        pageDashboard2 = context.new_page()
        pageDashboard2.set_viewport_size({"width": 0, "height": 0})
        pyautogui.press('F11')
        pageDashboard2.goto("https://unimedfortaleza.neovero.com/dashboards?id=15&fullscreen=S&mobile=N")
        time.sleep(20)

        # Clica no elemento "Preventivas do Mês" usando o texto do elemento da aba
        pageDashboard2.wait_for_selector('div.dx-item-content:has-text("Preventivas do Mês")', state="visible")
        pageDashboard2.click('div.dx-item-content:has-text("Preventivas do Mês")')
        
        time.sleep(20)


        meta_element = pageDashboard2.wait_for_selector('//*[@id="Dashboard"]/div/div[5]/div/dashboard-viewer/dx-layout-item/div/div/div/dx-layout-item/div/div/div/dx-layout-item/div/dx-dashboard-layout-tab-container/div/div/div/dx-layout-item/div/div/div[1]/dx-layout-item/div/div[1]/div/dx-layout-item[2]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/div')
        meta_element_text = meta_element.inner_text() if meta_element else "Não foi possível encontrar o elemento da meta."
        print("Meta:", meta_element_text)


        feitas_por_dia_element = pageDashboard2.query_selector('td[class^="dx-grandtotal dx-row-total"]:last-child > span')
        feitas_por_dia_text = feitas_por_dia_element.inner_text() if feitas_por_dia_element else "Não foi possível encontrar a quantidade feita por dia."
        print("Quantidade feita por dia:", feitas_por_dia_text)



        # Abrir uma nova aba com o dashboard Gráfico de pizza
        pageDashboard3 = context.new_page()
        pageDashboard3.set_viewport_size({"width": 0, "height": 0})
        pyautogui.press('F11')
        pageDashboard3.goto("https://unimedfortaleza.neovero.com/dashboards?id=15&fullscreen=S&mobile=N")
        time.sleep(20)

        # Clica no elemento "Status das Preventivas" usando o texto do elemento da aba
        pageDashboard3.wait_for_selector('div.dx-item-content:has-text("Status das Preventivas")', state="visible")
        pageDashboard3.click('div.dx-item-content:has-text("Status das Preventivas")')

        time.sleep(20)


        #Clica em Ordem de Serviço
        page.wait_for_selector('a[role="button"]:has-text("Ordens de Serviço")', state="visible")
        time.sleep(5)
        page.click('a[role="button"]:has-text("Ordens de Serviço")')
        time.sleep(1)

        # Clica em Monitor de Atendimento Neo
        page.wait_for_selector('//*[@id="nvNavBar"]/nav[2]/div[1]/ul/li[3]/div/ul/li[8]/a[2]', state="visible")
        page.click('//*[@id="nvNavBar"]/nav[2]/div[1]/ul/li[3]/div/ul/li[8]/a[2]')

        
        #Espera o botão Monitor Corporativo aparecer na tela
        page.wait_for_selector('.item-monitor-corporativo', state='visible', timeout=None)

        #Clica no botão Monitor Corporativo
        page.click('.item-monitor-corporativo')

        page.click('//*[@id="winid_1"]/div[1]/div[1]/div[3]/a[1]')

        # Inicia uma nova thread para a função tab_manager_function
        tab_thread = threading.Thread(target=tab_manager_function, args=(context,), daemon=True)
        tab_thread.start()
        
        while True:

            try:
                # Logs
                print("Aguardando a aparição da linha de requisição.")
                
                # Aguarda a aparição do elemento da Linha de requisição
                linhaRequisicao = '.cdk-row.ng-star-inserted:nth-child(1)'
                page.wait_for_selector(linhaRequisicao, state='visible', timeout=None)

                # Apenas o Número da linha de requisição
                numeroReq = page.inner_text(f'{linhaRequisicao} .cdk-column-numero')

                tipoReq = page.inner_text(f'{linhaRequisicao} .cdk-column-tipoManutencao')

                # Apenas a Empresa
                empresaReq = page.inner_text(f'{linhaRequisicao} .cdk-column-empresaid') 

                # Lógica do loop para reproduzir o áudio da notificação
                if page.is_visible('text=Requisições de serviço pendente de análise') and int(numeroReq) != requisicao:
                    requisicao = numeroReq
                        
                    if numeroReq != None and page.is_visible(f'{linhaRequisicao} .cdk-column-numero'):
                        if ultimo_valor_reproduzido is None or int(numeroReq) > int(ultimo_valor_reproduzido):
                            reproduzir_audio = True
                        else:
                            reproduzir_audio = False
                    else:
                        reproduzir_audio = False


                    # Verificar a empresa e executar um áudio específico para cada empresa 
                    if empresaReq == 'HOSPITAL UNIMED FORTALEZA':

                        
                        # Clica na linha de requisição para expandir e encontrar a oficina
                        if (reproduzir_audio):
                            page.click(linhaRequisicao)
                        else:
                            continue
                        # Aguarda a aparição do elemento da Oficina
                        oficina_element_xpath = '//*[@id="winid_1"]/div[1]/div[2]/nv-monitor-atendimento/div/nv-requisicao-servico/div/div[2]/div/div[4]/div[1]/div[2]/label'
                        page.wait_for_selector(oficina_element_xpath, state='visible', timeout=None)

                        # Obtém o texto do elemento da Oficina
                        oficina_text = page.inner_text(oficina_element_xpath)

                        if "CENTRAL DE EQUIPAMENTOS" in oficina_text:
                            if reproduzir_audio:
                                # Reproduzir o áudio usando o mixer do pygame
                                pygame.mixer.music.load(audio_pathLogistica)
                                pygame.mixer.music.play()
                                ultimo_valor_reproduzido = numeroReq

                                # Clica no botão depois de tocar o áudio
                                button_xpath = '//*[@id="winid_1"]/div[1]/div[2]/nv-monitor-atendimento/div/nv-requisicao-servico/div/div[1]/a'
                                page.click(button_xpath)

                        else: 
                            if reproduzir_audio:
                                # Reproduzir o áudio usando o mixer do pygame
                                pygame.mixer.music.load(audio_pathAreaTecnica)
                                pygame.mixer.music.play()
                                ultimo_valor_reproduzido = numeroReq

                                # Clica no botão depois de tocar o áudio
                                button_xpath = '//*[@id="winid_1"]/div[1]/div[2]/nv-monitor-atendimento/div/nv-requisicao-servico/div/div[1]/a'
                                page.click(button_xpath)

                    elif empresaReq == 'UNIMED LAR':
                        if reproduzir_audio:
                            # Reproduzir o áudio usando o mixer do pygame
                            pygame.mixer.music.load(audio_pathUnimedLar)
                            pygame.mixer.music.play()
                            ultimo_valor_reproduzido = numeroReq

                    elif empresaReq == 'CLÍNICAS UNIMED':
                        if reproduzir_audio:
                            # Reproduzir o áudio usando o mixer do pygame
                            pygame.mixer.music.load(audio_pathClinicas)
                            pygame.mixer.music.play()
                            ultimo_valor_reproduzido = numeroReq

                    elif empresaReq == 'LABORATÓRIOS UNIMED':
                        if reproduzir_audio:
                            # Reproduzir o áudio usando o mixer do pygame
                            pygame.mixer.music.load(audio_pathLaboratorios)
                            pygame.mixer.music.play()
                            ultimo_valor_reproduzido = numeroReq

                    elif empresaReq == 'UNIMED URGENTE':
                        if reproduzir_audio:
                            # Reproduzir o áudio usando o mixer do pygame
                            pygame.mixer.music.load(audio_pathUnimedUrgente)
                            pygame.mixer.music.play()
                            ultimo_valor_reproduzido = numeroReq

                    elif empresaReq == 'MEDICINA PREVENTIVA UNIMED FORTALEZA':
                        if reproduzir_audio:
                            # Reproduzir o áudio usando o mixer do pygame
                            pygame.mixer.music.load(audio_pathMedPrev)
                            pygame.mixer.music.play()
                            ultimo_valor_reproduzido = numeroReq  

                    elif empresaReq == 'CENTRO ONCOLÓGICO UNIMED FORTALEZA':
                        print("Nova requisição do CENTRO ONCOLÓGICO UNIMED FORTALEZA")

                    else:
                        print("Nova requisição do HOSPITAL UNIMED SUL")

            except Exception as e:
                print(f"Ocorreu um erro: {e}")
            
          
if __name__ == "__main__":
    main()
