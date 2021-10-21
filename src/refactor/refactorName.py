def refactorEspecialidade(especialidade: str) -> str:
    return especialidade


def refactorTipoServico(tipoSevico: str) -> str:
    tipoSevico = tipoSevico.upper().strip()
    if tipoSevico == "CONSULTÓRIOS MÉDICOS E CLÍNICAS ESPECIALIZADAS":
        tipoSevico = "CONSULTORIO / CLINICAS"
    elif tipoSevico == "PRONTOS SOCORROS (URGÊNCIA/EMERGÊNCIA)":
        tipoSevico = "PRONTO-SOCORRO 24H (URGENCIA E EMERGENCIA)"
    return tipoSevico
