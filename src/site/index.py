import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def navegacao(driver: webdriver.Chrome):
    driver.get("https://wwws.portoseguro.com.br/gerenciadorinterfaceweb/saude_rede_referenciada.do")

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
    for estado in estados:
        if estado.text == "SP":
            estado.click()

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
    for cidade in cidades:
        if cidade.text == "SAO PAULO":
            cidade.click()

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
    for plano in planos:
        if plano.text == "BRONZE I":
            plano.click()

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
    for tipoServico in tipoServicos:
        if tipoServico.text == "CONSULTÓRIOS MÉDICOS E CLÍNICAS ESPECIALIZADAS":
            tipoServico.click()

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
    for especialidade in especialidades:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, 'comboEspecialidades'))
            )
        finally:
            pass
        if especialidade.text != "":
            especialidade.click()

            print("Buscando Rede...")
            time.sleep(0.5)
            driver.find_element_by_id('consultarRedeCredenciada').click()

            # Frame com os resultados
            # time.sleep(1)
            driver.switch_to.frame(driver.find_element_by_id('frameListaRedeCredenciada'))

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'ps-map-list__item'))
                )
            finally:
                time.sleep(1)
                listaPrestadoresLi = driver.find_elements_by_class_name('ps-map-list__item')

                print(len(listaPrestadoresLi))

                print("Voltando a tela de pesquisa!")
                driver.switch_to.default_content()
                driver.execute_script("javascript:clickButtonVoltarRede();")

