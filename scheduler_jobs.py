import os
from datetime import datetime
from flask_mail import Message
from config import db, mail, Config
from models import Campanha, Cliente
from funcoes import enviar_campanha
from colorama import Fore, Style, init

init(autoreset=True)

ultima_verificacao = None


def processar_agendamentos():
    """
    Processa todas as campanhas com status 'Agendada'
    e executa envio automático quando data/hora forem atingidos.
    """
    from app import app  # Seguro aqui porque app.py já terminou de carregar globalmente

    global ultima_verificacao
    agora = datetime.now()
    ultima_verificacao = agora.strftime("%Y-%m-%d %H:%M:%S")

    with app.app_context():

        campanhas = Campanha.query.filter_by(status="Agendada").all()

        for c in campanhas:

            try:
                # Monta datetime do envio
                data_hora_envio = datetime.strptime(
                    f"{c.data1} {c.hora1}",
                    "%Y-%m-%d %H:%M"
                )

                # Ainda não chegou o horário
                if data_hora_envio > agora:
                    continue

                if c.enviado1:
                    continue  # Já enviado

                # Busca clientes correspondentes ao grupo
                if c.grupo and c.grupo.lower() != "todos":
                    clientes = Cliente.query.filter_by(grupo=c.grupo).all()
                else:
                    clientes = Cliente.query.all()

                lista_emails = [cli.email for cli in clientes]

                if not lista_emails:
                    print(Fore.YELLOW + f"⚠ Campanha '{c.nome}' sem destinatários.")
                    c.status = "Erro ao enviar ❌"
                    db.session.commit()
                    continue

                # Envia com função oficial do sistema
                enviados = enviar_campanha(c, lista_emails, upload_folder=Config.UPLOAD_FOLDER)

                # Atualiza status
                c.enviado1 = True
                c.status = "Enviada ✅"
                db.session.commit()

                print(Fore.GREEN + f"📨 Campanha '{c.nome}' enviada ({enviados} destinatários).")

            except Exception as e:
                c.status = "Erro ao enviar ❌"
                db.session.commit()
                print(Fore.RED + f"❌ Falha ao enviar '{c.nome}': {e}")


def get_ultima_verificacao():
    """Usado pela dashboard para exibir a hora da última checagem."""
    return ultima_verificacao
