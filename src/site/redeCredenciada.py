from xml.dom.minidom import parseString

from src.db.conexao import myConexao
from src.services.viaCep import getViaCep

conn = myConexao()
cursor = conn.cursor()

inserirDados = True


def redeCredenciada(xml: str, idEstado: int, idCidade: int, idRede: int, idTipoServico: int, idEspecialidade: int):

    dom = parseString(xml)
    prestadores = dom.getElementsByTagName('PrestadorVO')

    for prestador in prestadores:

        print("----------------------------------------------")

        tipoDocumento = prestador.getElementsByTagName('TipoPessoa')[0].firstChild.data
        documento = prestador.getElementsByTagName('CNPJCPFFormatado')[0].firstChild.data
        razaoSocial = prestador.getElementsByTagName('RazaoSocial')[0].firstChild.data
        nomeFantasia = prestador.getElementsByTagName('Nome')[0].firstChild.data
        enderecos = prestador.getElementsByTagName('EnderecoVO')

        if tipoDocumento.upper() == "F":
            idTipoDucumento = 1
        elif tipoDocumento.upper() == "J":
            idTipoDucumento = 2
        else:
            idTipoDucumento = None

        print(f"Razao Social: {razaoSocial}")

        sqlEstabelecimento = f"SELECT * FROM estabelecimento where documento like '{documento}';"
        cursor.execute(sqlEstabelecimento)
        idEstabelecimento = None
        if cursor.rowcount == 0:
            insertEstabelecimento = """
            INSERT INTO estabelecimento
                (id_tipo_estabelecimento, documento, razao_social, nome_fantasia)
            values (%s, %s, %s, %s)
            """
            # print(insertEstabelecimento)
            valuesEstabelecimento = (idTipoDucumento, documento, razaoSocial, nomeFantasia)

            if inserirDados:
                cursor.execute(insertEstabelecimento, valuesEstabelecimento)
                idEstabelecimento = conn.insert_id()
                conn.commit()
        elif cursor.rowcount == 1:
            idEstabelecimento = cursor.fetchone()[0]
        else:
            print(f"Erro no estabelecimento: {sqlEstabelecimento}")

        print(f"idEstabelecimento: {idEstabelecimento}")

        if idEstabelecimento is not None:
            for endereco in enderecos:
                cepString = endereco.getElementsByTagName('CepString')[0].firstChild.data
                cepComplementoString = endereco.getElementsByTagName('CepComplementoString')[0].firstChild.data
                try:
                    complemento = endereco.getElementsByTagName('Complemento')[0].firstChild.data
                except:
                    complemento = None
                finally:
                    pass
                numero = endereco.getElementsByTagName('Numero')[0].firstChild.data
                telefones = prestador.getElementsByTagName('TelefoneVO')

                cep = f"{cepString}-{cepComplementoString}"

                selectEnderecoEstabelecimento = f"SELECT * from tbl_estabelecimento_endereco where cep like '{cep}' and id_estabelecimento = {idEstabelecimento};"
                cursor.execute(selectEnderecoEstabelecimento)

                if cursor.rowcount == 0:

                    telefone1 = None
                    telefone2 = None
                    for t, tel in enumerate(telefones):
                        DDD = tel.getElementsByTagName('DDD')[0].firstChild.data
                        numero = tel.getElementsByTagName('Numero')[0].firstChild.data
                        telefone = f"{DDD}{numero}"

                        if t == 0:
                            telefone1 = telefone
                        elif t == 1:
                            telefone2 = telefone

                    resCep = getViaCep(cep)
                    if resCep.status_code == 200:
                        dados = resCep.json()
                        logradouroRes = dados['logradouro']
                        bairroRes = dados['bairro'].upper()

                        sqlBairro = f"SELECT * from tbl_bairro where nome like '{bairroRes}' and id_cidade = {idCidade};"
                        # print(sqlBairro)
                        cursor.execute(sqlBairro)

                        idBairro = None
                        if cursor.rowcount == 0:
                            insert = f"insert into tbl_bairro(nome, id_cidade) values('{bairroRes.upper()}', {idCidade}) "

                            if inserirDados:
                                cursor.execute(insert)
                                idBairro = conn.insert_id()
                                conn.commit()

                        elif cursor.rowcount == 1:
                            idBairro = cursor.fetchone()[0]
                        else:
                            print(cursor.fetchall())

                        insertEnderecoEstabelecimento = """
                        INSERT INTO tbl_estabelecimento_endereco 
                        (id_estabelecimento, cep, complemento, logradouro, numero, id_bairro, id_cidade, id_estado, telefone1, telefone2) VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        valuesEndereco = (idEstabelecimento, cep, complemento, logradouroRes, numero, idBairro, idBairro, idEstado, telefone1, telefone2)

                        cursor.execute(insertEnderecoEstabelecimento, valuesEndereco)
                        conn.commit()
                    else:
                        print("Erro na consulta ViaCep: ", resCep)

            # Inserir Rede Credenciada
            selectRedeCredenciada = f"""
            SELECT * from rede_credenciada where 
            id_rede = {idRede} and id_estabelecimento = {idEstabelecimento} and id_tipo_servico = {idTipoServico} and id_especialidade = {idEspecialidade};
            """

            cursor.execute(selectRedeCredenciada)
            if cursor.rowcount == 0:
                insertRede = """
                INSERT INTO rede_credenciada 
                (id_rede, id_estabelecimento, id_tipo_servico, id_especialidade) VALUES 
                (%s, %s, %s, %s)
                """
                valuesRede = (idRede, idEstabelecimento, idTipoServico, idEspecialidade)

                if inserirDados:
                    cursor.execute(insertRede, valuesRede)
                    conn.commit()

