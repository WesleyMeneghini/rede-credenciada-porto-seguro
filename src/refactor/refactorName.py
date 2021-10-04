def refactorEspecialidade(especialidade: str) -> str:
    return especialidade


def refactorTipoServico(tipoSevico: str) -> str:
    tipoSevico = tipoSevico.upper()
    if tipoSevico == "CONSULTÓRIOS MÉDICOS E CLÍNICAS ESPECIALIZADAS":
        tipoSevico = "CONSULTORIO / CLINICAS"
    return tipoSevico
