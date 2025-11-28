from config import db
from datetime import datetime

# ======================================================
#  TABELA DE RELAÇÃO N:N ENTRE CAMPANHA E CLIENTE
# ======================================================
campanha_cliente = db.Table(
    "campanha_cliente",
    db.Column("campanha_id", db.Integer, db.ForeignKey("campanha.id"), primary_key=True),
    db.Column("cliente_id", db.Integer, db.ForeignKey("cliente.id"), primary_key=True)
)


# ======================================================
#  CLIENTE
# ======================================================
class Cliente(db.Model):
    __tablename__ = "cliente"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    # Grupo opcional, pode ser usado como tag/categoria
    grupo = db.Column(db.String(100), nullable=True)

    # Relação N:N com campanhas
    campanhas = db.relationship(
        "Campanha",
        secondary=campanha_cliente,
        back_populates="clientes"
    )

    def __repr__(self):
        return f"<Cliente {self.nome} ({self.email})>"


# ======================================================
#  CAMPANHA
# ======================================================
class Campanha(db.Model):
    __tablename__ = "campanha"

    id = db.Column(db.Integer, primary_key=True)

    # Infomações principais da campanha
    nome = db.Column(db.String(255), nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    remetente = db.Column(db.String(255), nullable=False)

    grupo = db.Column(db.String(100), nullable=True)            # Agrupamento opcional
    frequencia = db.Column(db.String(50), nullable=True)        # Ex: semanal, mensal

    arquivo = db.Column(db.String(255), nullable=False)         # Caminho do HTML salvo

    # Mantendo compatibilidade — estão como string no fluxo atual
    data1 = db.Column(db.String(50), nullable=False)            # “2025-02-10”
    hora1 = db.Column(db.String(10), nullable=False)            # “14:30”

    status = db.Column(db.String(50), nullable=True)            # Enviada, Pendente, Erro
    enviado1 = db.Column(db.Boolean, default=False)             # Flag útil no scheduler

    fingerprint = db.Column(db.String(255), unique=True)        # Hash SHA-256 (agora comporta 64 chars)

    # Relação com clientes
    clientes = db.relationship(
        "Cliente",
        secondary=campanha_cliente,
        back_populates="campanhas"
    )

    # Timestamp opcional (ótimo para relatórios)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Campanha {self.nome}>"
