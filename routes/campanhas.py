from flask import render_template, request, redirect, url_for, flash, jsonify
from utils.auth import login_required
import os, hashlib, time
from werkzeug.utils import secure_filename
from config import db
from models import Campanha

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')


def _safe_save(fileobj):
    fname = secure_filename(fileobj.filename)
    base, ext = os.path.splitext(fname)
    unique = f"{int(time.time() * 1000)}_{base}{ext}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, unique)
    fileobj.save(path)
    return unique


def _make_fingerprint(**fields):
    key = "|".join(str(fields.get(k, "") or "") for k in [
        "nome", "remetente", "assunto", "frequencia", "data1", "arquivo", "grupo"
    ])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def campanhas_routes(app):

    # =====================================================
    #  AGENDAR CAMPANHA
    # =====================================================
    @app.route('/agendar', methods=['GET', 'POST'])
    @login_required
    def agendar():
        if request.method == 'POST':

            nome = (request.form.get('nome') or '').strip()
            assunto = (request.form.get('assunto') or '').strip()
            remetente = (request.form.get('remetente') or '').strip()
            grupo = (request.form.get('grupo') or '').strip()
            frequencia = (request.form.get('frequencia') or '').strip() or None
            data1 = (request.form.get('data1') or '').strip()
            hora1 = (request.form.get('hora1') or '').strip()
            arquivo = request.files.get('arquivo')

            # Campos obrigatórios
            if not all([nome, assunto, remetente, grupo, data1, hora1]) or not (arquivo and arquivo.filename.strip()):
                flash("Preencha todos os campos obrigatórios.", "error")
                return redirect(url_for('agendar'))

            # Campanha duplicada
            existente = Campanha.query.filter_by(
                nome=nome,
                assunto=assunto,
                data1=data1,
                grupo=grupo
            ).first()

            if existente:
                flash("Essa campanha já foi agendada.", "warning")
                return redirect(url_for('dashboard'))

            # Salvar arquivo
            nome_arquivo = _safe_save(arquivo)

            fingerprint = _make_fingerprint(
                nome=nome,
                remetente=remetente,
                assunto=assunto,
                frequencia=frequencia,
                data1=data1,
                arquivo=nome_arquivo,
                grupo=grupo
            )

            nova = Campanha(
                nome=nome,
                assunto=assunto,
                remetente=remetente,
                grupo=grupo,
                frequencia=frequencia,
                arquivo=nome_arquivo,
                data1=data1,
                hora1=hora1,
                status="Agendada",
                fingerprint=fingerprint
            )

            db.session.add(nova)
            db.session.commit()

            flash(f"Campanha '{nome}' agendada com sucesso!", "success")
            return redirect(url_for('dashboard'))

        return render_template('agendar.html', active_page='agendar')

    # =====================================================
    #  ENVIAR AGORA (AJAX)
    # =====================================================
    @app.route('/enviar/<int:id>', methods=['POST'])
    @login_required
    def enviar(id):
        campanha = Campanha.query.get_or_404(id)
        campanha.status = "Enviada ✅"
        db.session.commit()

        # Retorno para SweetAlert (AJAX)
        return jsonify({
            "status": "success",
            "message": f"Campanha '{campanha.nome}' marcada como enviada."
        })

    # =====================================================
    #  EXCLUIR CAMPANHA (AJAX)
    # =====================================================
    @app.route('/excluir/<int:id>', methods=['POST'])
    @login_required
    def excluir(id):
        campanha = Campanha.query.get_or_404(id)
        db.session.delete(campanha)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Campanha '{campanha.nome}' foi excluída com sucesso!"
        })
