from typing import List, Any, Optional

from pydantic import BaseModel, Field, validator


class VirtualPeriodClasses(BaseModel):
    """
    Turmas virtuais por periodo
    """

    id: str
    sigla: str
    descricao: str
    observacao: Any
    locais_de_aula: List[str]
    horarios_de_aula: str


class VirtualPeriodClassesModel(BaseModel):
    __root__: List[VirtualPeriodClasses]


class Professores(BaseModel):
    matricula: str
    foto: str
    email: str
    nome: str


class Participante(BaseModel):
    matricula: str
    foto: str
    email: str
    nome: str


class Aula(BaseModel):
    etapa: int
    professor: str
    data: str
    quantidade: int
    conteudo: str


class MateriaisDeAulaItem(BaseModel):
    url: str
    data_vinculacao: str
    descricao: str


class VirtualClassModel(BaseModel):
    """
    Turma virtual a partir do ID
    """

    id: int
    ano_letivo: str
    periodo_letivo: int
    componente_curricular: str
    professores: List[Professores]
    locais_de_aula: List
    data_inicio: str
    data_fim: str
    participantes: List[Participante]
    aulas: List[Aula]
    materiais_de_aula: List[MateriaisDeAulaItem]


class Period(BaseModel):
    """
    Periodos
    """

    ano_letivo: Optional[int]
    periodo_letivo: Optional[int]


class PeriodModel(BaseModel):
    __root__: List[Period]


class Vinculo(BaseModel):
    matricula: str
    nome: str
    curso: str
    campus: str
    situacao: str
    cota_sistec: str
    cota_mec: str
    situacao_sistemica: str


class UserDataModel(BaseModel):
    """
    Dados do usuário
    """

    id: int
    matricula: str
    nome_usual: str
    email: str
    url_foto_75x100: str
    tipo_vinculo: str
    vinculo: Vinculo


class Nota(BaseModel):
    nota: Optional[str]
    faltas: Optional[int]


class ReportCard(BaseModel):
    """
    Boletim do usuário
    """

    codigo_diario: str
    disciplina: str
    segundo_semestre: bool
    carga_horaria: int
    carga_horaria_cumprida: int
    numero_faltas: int
    percentual_carga_horaria_frequentada: int
    situacao: str
    quantidade_avaliacoes: int
    nota_etapa_1: Nota
    nota_etapa_2: Nota
    nota_etapa_3: Nota
    nota_etapa_4: Nota
    media_disciplina: Optional[float]
    nota_avaliacao_final: Nota
    media_final_disciplina: Optional[float]

    @validator("media_final_disciplina")
    def set_media_final_disciplina(cls, media_final):
        return media_final or 0.0


class ReportCardModel(BaseModel):
    __root__: List[ReportCard]
