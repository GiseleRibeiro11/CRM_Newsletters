import os
import atexit

from flask import Flask, redirect, url_for, render_template
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

from config import Config, db
from routes.campanhas import campanhas_routes
from routes.dashboard import dashboard_routes
from routes.login import login_routes


# =====================================================
#  FLASK APP
# =====================================================
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)


# =====================================================
#  REGISTRO DAS ROTAS
# =====================================================
login_routes(app)
dashboard_routes(app)
campanhas_routes(app)


# =====================================================
#  CRIA DIRETÓRIO DE UPLOADS (SE NÃO EXISTIR)
# =====================================================
os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

with app.app_context():
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if uri.startswith("sqlite"):
        db.create_all()


# =====================================================
#  ROTA HOME (REDIRECIONA PARA LOGIN)
# =====================================================
@app.route("/")
def home():
    return redirect(url_for("login_page"))


# =====================================================
#  PÁGINA OOPS – ERROR HANDLERS
# =====================================================
@app.errorhandler(404)
def page_not_found(error):
    return render_template("oops.html", code=404), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("oops.html", code=500), 500


# =====================================================
#  SCHEDULER (Só inicia quando executado como app principal)
# =====================================================
def iniciar_scheduler():
    from scheduler_jobs import processar_agendamentos

    scheduler = BackgroundScheduler()
    scheduler.add_job(processar_agendamentos, "interval", seconds=30)
    scheduler.start()

    print("[Scheduler] ✅ Ativo. Verificando agendamentos a cada 30s.")

    atexit.register(lambda: scheduler.shutdown(wait=False))


# =====================================================
#  START DA APLICAÇÃO
# =====================================================
if __name__ == "__main__":
    iniciar_scheduler()
    # Para ver a página OOPS de erro 500, use debug=False
    app.run(debug=False, use_reloader=False)
    # se quiser desenvolver com debug=True, tudo bem,
    # só lembra que o handler 500 só aparece com debug=False
