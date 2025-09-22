from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db 
from models import User, Produto


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dona_bela.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]= "troque_esta_chave" 

db.init_app(app)

def usuario_logado():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)

@app.route("/")
def index():
    produtos = Produto.query.limit(5).all()
    return render_template("index.html", produtos=produtos, user=usuario_logado())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return redirect(url_for('register'))

        u = User(nome=nome, email=email)
        u.set_password(senha)
        db.session.add(u)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', user=usuario_logado())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=email).first()
    
        if user and user.check_password(senha):
            session['user_id'] = user.id
            flash(f'Bem-vindo(a), {user.nome}!', 'success')
            return redirect(url_for('index'))

        else:
            flash('E-mail ou senha inválidos.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', user=usuario_logado())

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('index'))

@app.route('/produtos')
def produtos():
    lista = Produto.query.all()
    return render_template('produtos.html', produtos=lista, user=usuario_logado())

@app.route('/produtos/novo', methods=['GET', 'POST'])
def produto_novo():
    if not usuario_logado():
        flash('Faça login para gerenciar produtos.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'].replace(',', '.'))
        descricao = request.form.get('descricao', '')
        categoria = request.form.get('categoria', '')
        p = Produto(nome=nome, preco=preco, descricao=descricao, categoria=categoria)
        db.session.add(p)
        db.session.commit()

        flash('Produto adicionado!', 'success')
        return redirect(url_for('produtos'))
    return render_template('produto_form.html', produto=None, user=usuario_logado())

@app.route('/produtos/<int:id>/editar', methods=['GET', 'POST'])
def produto_editar(id):
    p = Produto.query.get_or_404(id)

    if request.method == 'POST':
        p.nome = request.form['nome']
        p.preco = float(request.form['preco'].replace(',', '.'))
        p.descricao = request.form.get('descricao', '')
        p.categoria = request.form.get('categoria', '')

        db.session.commit()
        flash('Produto atualizado!', 'success')
        return redirect(url_for('produtos'))

    return render_template('produto_form.html', produto=p, user=usuario_logado())

@app.route('/produtos/<int:id>/excluir', methods=['POST'])
def produto_excluir(id):
    p = Produto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Produto excluído!', 'info')
    return redirect(url_for('produtos'))
