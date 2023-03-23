import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Registro(Base):
    __tablename__ = 'registros'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    sobrenome = Column(String)
    departamento = Column(String)
    codigo = Column(String)
    usuario = Column(String)
    senha = Column(String)


class Formulario(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Definindo campos do formulário
        self.nome = TextInput(hint_text='Nome')
        self.sobrenome = TextInput(hint_text='Sobrenome')
        self.departamento = TextInput(hint_text='Departamento')
        self.codigo = TextInput(hint_text='Código')
        self.usuario = TextInput(hint_text='Usuário')
        self.senha = TextInput(hint_text='Senha', password=True)

        # Adicionando campos ao layout
        self.add_widget(self.nome)
        self.add_widget(self.sobrenome)
        self.add_widget(self.departamento)
        self.add_widget(self.codigo)
        self.add_widget(self.usuario)
        self.add_widget(self.senha)

        # Botão de salvar
        btn_salvar = Button(text='Salvar', size_hint=(1, 0.3))
        btn_salvar.bind(on_press=lambda _: self.salvar())  # <--- Linha adicionada
        self.add_widget(btn_salvar)
        
    def salvar(self):
        # Criando objeto de conexão com o banco de dados
        engine = create_engine('sqlite:///cadastro.db', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Criando objeto de registro
        registro = Registro(
            nome=self.nome.text,
            sobrenome=self.sobrenome.text,
            departamento=self.departamento.text,
            codigo=self.codigo.text,
            usuario=self.usuario.text,
            senha=self.senha.text
        )

        # Adicionando registro ao banco de dados
        session.add(registro)
        session.commit()

        # Limpando campos do formulário
        self.nome.text = ''
        self.sobrenome.text = ''
        self.departamento.text = ''
        self.codigo.text = ''
        self.usuario.text = ''
        self.senha.text = ''


class CadastroApp(App):

    def build(self):
        return Formulario()
    
if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '600')
    CadastroApp().run()
