import os
from datetime import datetime
from flask_mail import Message
from config import mail, Config


def parse_dt_maybe(dt_str):
    """
    Tenta converter uma string em datetime. 
    Retorna None se a conversão falhar.
    """
    if not dt_str:
        return None

    formatos = ["%Y-%m-%d %H:%M"]

    for fmt in formatos:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue

    return None


def enviar_campanha(campanha, lista_emails, upload_folder=None):
    """
    Envia uma campanha para uma lista de emails.
    Retorna o número de envios realizados com sucesso.
    """

    upload_dir = upload_folder or Config.UPLOAD_FOLDER
    caminho_arquivo = os.path.join(upload_dir, campanha.arquivo)

    # ----------------------------------------------------------------------
    # 1. GARANTE QUE O ARQUIVO EXISTE
    # ----------------------------------------------------------------------
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(
            f"Arquivo HTML da campanha não encontrado: {caminho_arquivo}"
        )

    # ----------------------------------------------------------------------
    # 2. LÊ O HTML DA CAMPANHA
    # ----------------------------------------------------------------------
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        raise RuntimeError(f"Não foi possível ler o arquivo HTML: {e}")

    enviados = 0

    # ----------------------------------------------------------------------
    # 3. ENVIA O EMAIL PARA CADA DESTINATÁRIO
    # ----------------------------------------------------------------------
    for email in lista_emails:
        try:
            msg = Message(
                subject=campanha.assunto,
                recipients=[email],
                html=html,
                sender=("Marketing", campanha.remetente)
            )

            mail.send(msg)
            enviados += 1

        except Exception as e:
            # Aqui podemos registrar erro sem travar outros envios
            print(f"[ERRO] Falha ao enviar email para {email}: {e}")
            continue

    return enviados
