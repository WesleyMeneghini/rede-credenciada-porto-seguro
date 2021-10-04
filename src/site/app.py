import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def navegacao(driver: webdriver.Chrome):

    driver.get("https://wwws.portoseguro.com.br/gerenciadorinterfaceweb/saude_rede_referenciada.do")

    estadoValueId = 0
    cidadeValueId = 0
    planoValueId = 0
    tipoServicoValueId = 0
    especialidadeValueId = 0

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'selecione_rede'))
        )
    finally:
        pass

    driver.find_element_by_id('selecione_rede').find_elements_by_tag_name('option')[1].click()
    driver.find_element_by_id('selecione_documento').find_elements_by_tag_name('option')[3].click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'comboUF'))
        )
    finally:
        pass

    print("Selecionando estados!")
    estados = driver.find_element_by_id('comboUF').find_elements_by_tag_name('option')
    del[estados[0]]
    for estadoElement in estados:
        if estadoElement.text == "SP":
            estadoValueId = estadoElement.get_attribute('value')
            estadoElement.click()
            print(f"UF: {estadoElement.text}")

    print("Selecionando cidades!")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'comboCidade'))
        )
    finally:
        pass
    cidades = driver.find_element_by_id('comboCidade').find_elements_by_tag_name('option')
    del [cidades[0]]
    for cidadeElement in cidades:
        if cidadeElement.text == "SAO PAULO":
            cidadeValueId = cidadeElement.get_attribute('value')
            cidadeElement.click()
            print(f"Cidade: {cidadeElement.text}")

    print("Selecionando: Tipo Plano!")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'comboPlanos'))
        )
    finally:
        pass
    planos = driver.find_element_by_id('comboPlanos').find_elements_by_tag_name('option')
    del[planos[0]]
    for planoElement in planos:
        if planoElement.text == "BRONZE I":
            planoValueId = planoElement.get_attribute('value')
            planoElement.click()
            print(f"Nome Plano: {planoElement.text}")

    print("Selecionando: Tipo de Serviço!")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'comboServicos'))
        )
    finally:
        pass
    tipoServicos = driver.find_element_by_id('comboServicos').find_elements_by_tag_name('option')
    del [tipoServicos[0]]
    for tipoServicoElement in tipoServicos:
        if tipoServicoElement.text == "CONSULTÓRIOS MÉDICOS E CLÍNICAS ESPECIALIZADAS":
            tipoServicoValueId = tipoServicoElement.get_attribute('value')
            tipoServicoElement.click()
            print(f"Tipo Serviço: {tipoServicoElement.text}")

    print("Selecionando: Especialidade!")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'comboEspecialidades'))
        )
    finally:
        pass
    especialidades = driver.find_element_by_id('comboEspecialidades').find_elements_by_tag_name('option')
    del [especialidades[0]]
    for especialidadeElement in especialidades:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, 'comboEspecialidades'))
            )
        finally:
            pass
        if especialidadeElement.text != "":
            especialidadeValueId = especialidadeElement.get_attribute('value')
            especialidadeElement.click()
            print(f"Especialidade: {especialidadeElement.text}")




            # print("Buscando Rede...")
            # time.sleep(0.5)
            # driver.find_element_by_id('consultarRedeCredenciada').click()
            #
            # # Frame com os resultados
            # # time.sleep(1)
            #
            # linkIframe = driver.find_element_by_id('frameListaRedeCredenciada').get_attribute('src')
            # print(linkIframe)
            # breakpoint()
            # driver.switch_to.frame(driver.find_element_by_id('frameListaRedeCredenciada'))
            #
            # try:
            #     WebDriverWait(driver, 15).until(
            #         EC.presence_of_element_located(
            #             (By.CLASS_NAME, 'ps-map-list__item'))
            #     )
            # finally:
            #     time.sleep(1)
            #     listaPrestadoresLi = driver.find_elements_by_class_name('ps-map-list__item')
            #
            #     print(len(listaPrestadoresLi))
                # for p, prestador in enumerate(listaPrestadoresLi):
                #
                #     if p > 0:
                #         driver.switch_to.frame(driver.find_element_by_id('frameListaRedeCredenciada'))
                #         time.sleep(0.5)
                #
                #     try:
                #         WebDriverWait(driver, 15).until(
                #             EC.presence_of_element_located(
                #                 (By.CLASS_NAME, 'ps-map-list__item'))
                #         )
                #     finally:
                #         while len(driver.find_elements_by_class_name('ps-map-list__item')) == 0:
                #             ...
                #     driver.find_elements_by_class_name('ps-map-list__item')[p+1].find_element_by_tag_name('a').click()
                #
                #     driver.switch_to.default_content()
                #     time.sleep(1)
                #     try:
                #         WebDriverWait(driver, 15).until(
                #             EC.presence_of_element_located(
                #                 (By.XPATH, '//*[@id="incluirConteudo"]/iframe'))
                #         )
                #     finally:
                #         pass
                #         time.sleep(2)
                #     driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="incluirConteudo"]/iframe'))
                #     try:
                #         WebDriverWait(driver, 15).until(
                #             EC.presence_of_element_located(
                #                 (By.CLASS_NAME, 'ps-text-light'))
                #         )
                #     finally:
                #         pass
                #     time.sleep(1)
                #     res = driver.find_elements_by_class_name("ps-text-light")
                #     print("\n-------------------")
                #     print(res[0].text)
                #     print(res[1].text)
                #     print(res[2].text)
                #     print(res[3].text)
                #
                #     driver.switch_to.default_content()
                #     time.sleep(1)
                #     driver.execute_script("document.getElementsByClassName('ps-modal-close ps-modal-close-default')[0].click()")
                #     time.sleep(1)


                # print("Voltando a tela de pesquisa!")
                # driver.execute_script("javascript:clickButtonVoltarRede();")

