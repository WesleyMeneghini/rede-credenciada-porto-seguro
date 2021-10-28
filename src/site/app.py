import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.db.conexao import myConexao
from src.refactor.refactorName import refactorEspecialidade, refactorTipoServico
from src.site.redeCredenciada import redeCredenciada

conn = myConexao()
cursor = conn.cursor()

salvarRedeCredenciada = True


def navegacao(driver: webdriver.Chrome):

    driver.get("https://wwws.portoseguro.com.br/gerenciadorinterfaceweb/saude_rede_referenciada.do")

    idEstado = 0
    idCidade = 0
    idRede = 0
    idTipoServico = 0

    cidadeValueId = 0
    planoValueId = 0
    tipoServicoValueId = 0

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
            nomeUf = estadoElement.text.upper()
            print(f"UF: {nomeUf}")

            selectUf = f"select * from tbl_estado where uf like '{nomeUf}'"
            cursor.execute(selectUf)
            idEstado = cursor.fetchone()[0]

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
            nomeCidade = cidadeElement.text.upper()
            print(f"Cidade: {nomeCidade}")

            selectCidade = f"select * from tbl_cidade where nome like '{nomeCidade}'"
            cursor.execute(selectCidade)
            idCidade = cursor.fetchone()[0]


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

        nomeTipoPlano = planoElement.text
        print(f"Nome Plano: {nomeTipoPlano}")

        selectRede = f"select * from tbl_rede where nome like '{nomeTipoPlano}' and id_operadora = 11;"
        print(selectRede)
        cursor.execute(selectRede)

        if cursor.rowcount == 1:
            planoValueId = planoElement.get_attribute('value')
            planoElement.click()

            idRede = cursor.fetchone()[0]

            print("Selecionando: Tipo de Serviço!")
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.ID, 'comboServicos'))
                )
            finally:
                pass
            tipoServicos = driver.find_element_by_id('comboServicos').find_elements_by_tag_name('option')
            del [tipoServicos[0]]
            for tipoServicoElement in tipoServicos:

                nomeTipoServico = refactorTipoServico(tipoServicoElement.text)
                print(f"\nTipo Serviço: {nomeTipoServico}\n")

                sql = f"select * from tbl_tipo_servico where nome like '{nomeTipoServico}';"

                cursor.execute(sql)

                if cursor.rowcount == 1:
                    tipoServicoValueId = tipoServicoElement.get_attribute('value')
                    tipoServicoElement.click()

                    idTipoServico = cursor.fetchone()[0]

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

                            nomeEspecialidade = refactorEspecialidade(especialidadeElement.text)
                            print(f"Especialidade: {nomeEspecialidade}")

                            selectEspecialidade = f"select * from tbl_especialidade where nome like '{nomeEspecialidade}';"
                            cursor.execute(selectEspecialidade)
                            if cursor.rowcount == 0:
                                insertEspecialidade = f"INSERT INTO tbl_especialidade(nome) VALUES ('{nomeEspecialidade}');"
                                cursor.execute(insertEspecialidade)
                                idEspecialidade = conn.insert_id()
                                conn.commit()
                            else:
                                idEspecialidade = cursor.fetchone()[0]

                            if idEspecialidade is not None:
                                payload = f"""
                                <soap:Envelope
                                    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                                    xmlns:tem="http://tempuri.org/">
                                    <soap:Header/>
                                    <soap:Body>
                                        <tem:ListarPrestadoresGIW>
                                            <tem:rede>1</tem:rede>
                                            <tem:cidadeID>{cidadeValueId}</tem:cidadeID>
                                            <tem:planoID>{planoValueId}</tem:planoID>
                                            <tem:tipoServicoID>{tipoServicoValueId}</tem:tipoServicoID>
                                            <tem:especialidadeID>{especialidadeValueId}</tem:especialidadeID>
                                            <tem:tipoBusca>1</tem:tipoBusca>
                                            <tem:situacao>1</tem:situacao>
                                        </tem:ListarPrestadoresGIW>
                                    </soap:Body>
                                </soap:Envelope>
                                """

                                url = "https://wwws.portoseguro.com.br/gerenciadorinterfaceweb/mapas_Acd.content"
                                querystring = {"tipo": "redeReferenciada"}
                                print(payload)
                                response = requests.request("POST", url, data=payload, params=querystring)

                                # Obs: Os Campos abaixo com valores dos Ids, ja sao em relaçao ao banco de dados do sistema
                                if salvarRedeCredenciada:
                                    redeCredenciada(
                                        xml=response.text,
                                        idEstado=idEstado,
                                        idCidade=idCidade,
                                        idRede=idRede,
                                        idTipoServico=idTipoServico,
                                        idEspecialidade=idEspecialidade
                                    )

                else:
                    print(f"Nao achou o tipo de serviço: {nomeTipoServico}")

        elif cursor.rowcount == 0:
            print(f"Inserir plano/rede: {nomeTipoPlano}")
            # cursor.execute(f"insert into tbl_rede (nome, id_operadora) values ('{nomeTipoPlano}', 11)")
            # conn.commit()
