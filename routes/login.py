from flask import render_template, request, redirect, url_for, flash, session

def login_routes(app):
    if 'login_page' in app.view_functions:
        return

    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            senha = request.form.get('senha', '').strip()

            # LOGIN FIXO (PODE SER ALTERADO DEPOIS)
            if email == "admin@qnova.com" and senha == "1234":
                session['usuario'] = email
                flash("Login efetuado com sucesso!", "success")
                return redirect(url_for('dashboard'))

            # CREDENCIAIS INCORRETAS
            flash("E-mail ou senha incorretos!", "error")
            return redirect(url_for('login_page'))

        # Ativa o modo auth_page no template (tema dark futurista)
        return render_template('login.html', auth_page=True)

    @app.route('/logout')
    def logout():
        session.pop('usuario', None)
        flash("Sessão encerrada.", "success")
        return redirect(url_for('login_page'))
