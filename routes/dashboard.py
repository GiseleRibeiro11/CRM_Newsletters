from flask import render_template
from utils.auth import login_required
from datetime import datetime
from config import db
from models import Campanha

def dashboard_routes(app):

    @app.route("/dashboard")
    @login_required
    def dashboard():
        """
        Exibe métricas, campanhas e o próximo envio.
        """

        # Buscar todas campanhas
        campanhas = Campanha.query.order_by(Campanha.data1.asc()).all()

        # Apenas campanhas ainda não enviadas
        campanhas_pendentes = [
            c for c in campanhas
            if c.status in ("Agendada", "Pendente")
        ]

        proximas = []

        for c in campanhas_pendentes:
            try:
                data_hora_envio = datetime.strptime(
                    f"{c.data1} {c.hora1}", "%Y-%m-%d %H:%M"
                )
                proximas.append({
                    "id": c.id,
                    "nome": c.nome,
                    "assunto": c.assunto,
                    "grupo": c.grupo,
                    "data1": c.data1,
                    "hora1": c.hora1,
                    "status": c.status,
                    "data_hora": data_hora_envio
                })
            except Exception:
                continue

        # Ordena do envio mais próximo → mais distante
        proximas = sorted(proximas, key=lambda x: x["data_hora"])

        total_clientes = 0    # Ajustar depois se houver tabela de clientes
        taxa_media = "—"      # Ajustável com estatísticas reais
        
        ultima_verificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return render_template(
            "dashboard.html",
            campanhas=campanhas,
            proximas=proximas,
            total_clientes=total_clientes,
            taxa_media=taxa_media,
            ultima_verificacao=ultima_verificacao,
            active_page="dashboard"
        )
