import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Instâncias globais

db = SQLAlchemy()
mail = Mail()

class Config:
    # ------------------------------------------------------
    #  SEGURANÇA
    # ------------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # ------------------------------------------------------
    #  BANCO DE DADOS
    # ------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///campanhas.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ------------------------------------------------------
    #  E-MAIL (FLASK-MAIL)
    # ------------------------------------------------------
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "emailremetente@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "sua_senha_aqui")

    # Remetente padrão (opcional)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # ------------------------------------------------------
    #  FUSO HORÁRIO
    # ------------------------------------------------------
    APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Europe/Lisbon")

    # ------------------------------------------------------
    #  UPLOADS
    # ------------------------------------------------------
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB