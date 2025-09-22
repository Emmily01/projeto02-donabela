from database import db
from models import User, Produto
from app import app

with app.app_context():
    db.drop_all() 
    db.create_all()

    
    if not User.query.filter_by(email="admin@donabela.com").first():
        u = User(nome="Admin Dona Bela", email="admin@donabela.com")
        u.set_password("admin123")
        db.session.add(u)

    
    if not Produto.query.first():
        exemplos = [
            Produto(nome="Bolo de Chocolate", preco=25.00, descricao="Bolo caseiro com cobertura", categoria="bolo"),
            Produto(nome="Coxinha", preco=4.50, descricao="Salgado tradicional", categoria="salgado"),
            Produto(nome="Brigadeiro", preco=2.50, descricao="Docinho de chocolate", categoria="doce"),
            Produto(nome="Cappuccino", preco=6.00, descricao="Bebida cremosa", categoria="bebida"),
        ]
        db.session.bulk_save_objects(exemplos)

    db.session.commit()
    print("Banco de dados inicializado com sucesso!")