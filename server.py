from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import g
import psycopg2
from datetime import datetime

app = Flask(__name__)

#Informações banco de dados
db_host = 'localhost'
db_port = '5432'
db_name = 'tg3.0'
db_user = 'postgres'
db_password = '1234'
global sessao
global usuarioid2
global clienteID

@app.route('/telaadm')
def index():
   
    return render_template('index.html')

@app.route('/usuarios')
def usuarios():

    connection = psycopg2.connect(
        host=db_host, port=db_port, database=db_name,
        user=db_user, password=db_password
    )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (us_id) FROM tb_user')

    us_id = cursor.fetchone()[0]

    if us_id is not None:
        us_id = us_id + 1
    else:
        us_id = 1  

    selectSetor = getSelectSetor()
    
    return render_template('usuarios.html', us_id=us_id, selectSetor = selectSetor)  

@app.route('/telausuario')
def telausuario():
    return render_template('telausuario.html')

@app.route('/telaGestor')
def telaGestor():
    return render_template('telaGestor.html')

@app.route('/telausercliente')
def telausercliente():
    return render_template('telausuarioCliente.html')

@app.route('/telausergestor')
def telausergestor():
    return render_template('telaGestorCliente.html')

@app.route('/')
def logar1():
    return render_template('login.html')

@app.route('/dadosinseridos')
def sucesso():
    return render_template('dadosinseridos.html')

@app.route('/loginerror')
def loginerror():
    return render_template('loginError.html')



@app.route('/inserir_assunto')
def inserir_assunto():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(as_id) FROM tb_assunto')

    as_id = cursor.fetchone()[0]

    if as_id is not None:
        as_id = as_id + 1
    else:
        as_id = 1
    


    return render_template('insertAssunto.html', as_id=as_id)

@app.route('/inserirEquipamento')
def inserirEquipamento():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(eq_id) FROM tb_equipamento')

    eq_id = cursor.fetchone()[0]

    if eq_id is not None:
        eq_id = eq_id + 1
    else:
        eq_id = 1
    

    return render_template('inserirEquipamento.html', eq_id=eq_id)

@app.route('/inserirEquipamentoCliente')
def inserirEquipamentoCliente():
    global clienteID
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(eq_id) FROM tb_equipamento')

    eq_id = cursor.fetchone()[0]

    if eq_id is not None:
        eq_id = eq_id + 1
    else:
        eq_id = 1
    
    cli_id = clienteID

    return render_template('inserirEquipamentoCliente.html', eq_id=eq_id, cli_id=cli_id)

@app.route('/selecionar_cliente')
def selecionar_cliente():
    return render_template('selecionarCliente.html')


@app.route('/inserirPJ')
def inserirPJ():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (cli_id) FROM tb_cliente')


    cli_id = cursor.fetchone()[0]

    if cli_id is not None:
        cli_id = cli_id + 1
    else:
        cli_id = 1

    return render_template('inserirPJ.html', cli_id=cli_id)

@app.route('/inserirPF')
def inserirPF():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (cli_id) FROM tb_cliente')

    cli_id = cursor.fetchone()[0]

    if cli_id is not None:
        cli_id = cli_id + 1
    else:
        cli_id = 1   


    return render_template('inserirPF.html', cli_id=cli_id)

@app.route('/inserirUserCliente')
def inserirUserCliente():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (us_id) FROM tb_user')

    us_id = cursor.fetchone()[0]

    if us_id is not None:
        us_id = us_id + 1
    else:
        us_id = 1  
       
    return render_template('inserirUserCliente.html', us_id=us_id)

@app.route('/inserirUserFuncionario')
def inserirUserFuncionario():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (us_id) FROM tb_user')

    us_id = cursor.fetchone()[0]

    if us_id is not None:
        us_id = us_id + 1
    else:
        us_id = 1  
       
    
    return render_template('inserirUserFuncionario.html', us_id=us_id)

@app.route('/inserirevento', methods=['POST'])
def inserirevento():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (eve_id) FROM tb_evento')

   
    eve_id = cursor.fetchone()[0]

    if eve_id is not None:
        eve_id = eve_id + 1
    else:
        eve_id = 1
    
    selectStatus = getSelectStatus()
    selectSetor = getSelectSetor()
    cha_id = request.form['cha_id']
    
    return render_template('eventoChamado.html', selectStatus = selectStatus, selectSetor = selectSetor, cha_id = cha_id, eve_id = eve_id)

def getSelectStatus():

    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cur = connection.cursor()
    cur.execute("SELECT sta_id, sta_nome FROM tb_status")
    selectStatus = []

    for row in cur:
        selectStatus.append({"sta_id": row[0],"sta_nome": row[1]})

    connection.close()

    return selectStatus


def getSelectSetor():

    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cur = connection.cursor()
    cur.execute("SELECT set_id, set_nome FROM tb_setor")
    selectSetor = []

    for row in cur:
        selectSetor.append({"set_id": row[0],"set_nome": row[1]})

    connection.close()

    return selectSetor

@app.route('/inserirChamado')
def inserirChamado():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(cha_id) FROM tb_chamado')

    cha_id = cursor.fetchone()[0]

    if cha_id is not None:
        cha_id = cha_id + 1
    else:
        cha_id = 1
    
    selectAssunto = getSelectAssunto()

    return render_template('novoChamado.html', cha_id=cha_id, selectAssunto=selectAssunto)

@app.route('/inserirChamadoCliente')
def inserirChamadoCliente():
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(cha_id) FROM tb_chamado')

    cha_id = cursor.fetchone()[0]

    if cha_id is not None:
        cha_id = cha_id + 1
    else:
        cha_id = 1
    
    selectEquipamento = getSelectEquipamento()
    selectAssunto = getSelectAssunto()
    return render_template('novoChamadoCliente.html', cha_id=cha_id, selectEquipamento=selectEquipamento, selectAssunto=selectAssunto)


#Comando para inserção dos dados no banco 
@app.route('/enviar_dados', methods=['POST'])
def enviar_dados():
    # Recebe os dados do formulário HTML
    id = request.form['id']
    nome = request.form['nome']

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_assunto (as_id, as_nome) VALUES (%s, %s);", (id, nome))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"


#Inserir PJ
@app.route('/inserir_PJ', methods=['POST'])
def inserir_PJ():
    # Recebe os dados do formulário HTML
    cli_id = request.form['cli_id']
    pj_razaosocial = request.form['pj_razaosocial']
    pj_nomefantasia = request.form['pj_nomefantasia']
    pj_cnpj = request.form['pj_cnpj']
    cli_cep = request.form['cli_cep']
    cli_telefone = request.form['cli_telefone']
    cli_celular = request.form['cli_celular']
    cli_email = request.form['cli_email']

    numero = request.form ['numero']
    rua = request.form['rua']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form.get('list_estado')
    
    
    cli_endereco = numero + ", " + rua + ", " + bairro + ", " + cidade + "-" + estado
    

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_cliente (cli_id, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email) VALUES (%s, %s, %s, %s, %s, %s);", (cli_id, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email))
        connection.commit()
        cursor.execute("INSERT INTO tb_pj (cli_id, pj_razaosocial, pj_nomefantasia, pj_cnpj) VALUES (%s, %s, %s, %s);", (cli_id, pj_razaosocial, pj_nomefantasia, pj_cnpj))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"

#Inserir PF
@app.route('/inserir_PF', methods=['post'])
def inserir_PF():
    # Recebe os dados do formulário HTML
    numero = request.form ['numero']
    rua = request.form['rua']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form.get('list_estado')
    cli_id = request.form['cli_id']
    pf_nome = request.form['pf_nome']
    pf_nomesocial = request.form['pf_nomesocial']
    pf_cpf = request.form['pf_cpf']
    cli_endereco = numero + ", " + rua + ", " + bairro + ", " + cidade + "-" + estado
    cli_cep = request.form['cli_cep']
    cli_telefone = request.form['cli_telefone']
    cli_celular = request.form['cli_celular']
    cli_email = request.form['cli_email']

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_cliente (cli_id, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email) VALUES (%s, %s, %s, %s, %s, %s);", (cli_id, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email))
        connection.commit()
        cursor.execute("INSERT INTO tb_pf (cli_id, pf_nome, pf_nomesocial, pf_cpf) VALUES (%s, %s, %s, %s);", (cli_id, pf_nome, pf_nomesocial, pf_cpf))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"
    
#Consultar cliente
def search_cliente(nome):
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Consulta na tabela tb_pf
        cur.execute("SELECT tb_pf.cli_id, pf_cpf, pf_nome, pf_nomesocial, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email FROM tb_cliente, tb_pf WHERE tb_cliente.cli_id = tb_pf.cli_id AND LOWER(pf_nome) ilike %s;", ("%"+nome+"%",))
        resultado_pf = cur.fetchall()

        # Consulta na tabela tb_pj
        cur.execute("SELECT tb_pj.cli_id, pj_cnpj, pj_razaosocial, pj_nomefantasia, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email FROM tb_cliente, tb_pj WHERE tb_cliente.cli_id = tb_pj.cli_id AND LOWER(pj_nomefantasia) ilike %s;", ("%"+nome+"%",))
        resultado_pj = cur.fetchall()

        cur.close()
        connection.close()

        return resultado_pf, resultado_pj
    except Exception as e:
        return None

@app.route('/consulta_cliente', methods=['POST'])
def consulta_cliente():
    nome = request.form.get('nome')
    
    results_pf, results_pj = search_cliente(nome)
    return render_template('resultsCliente.html', results_pf=results_pf, results_pj=results_pj)

#Consultar usuario
def search_usuario(us_nome):
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Consulta na tabela cliente
        cur.execute("SELECT * from tb_user_cliente where LOWER(us_nome) ilike %s;", ("%"+us_nome+"%",))
        results_cli = cur.fetchall()

        # Consulta na tabela funcionario
        cur.execute("SELECT * from tb_user_funcionario where LOWER(fun_nome) ilike %s;", ("%"+us_nome+"%",))
        results_fun = cur.fetchall()

        cur.close()
        connection.close()

        return results_cli, results_fun
    except Exception as e:
        return None

def search_usuario_cliid(us_nome,cli_id):
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Consulta na tabela cliente
        cur.execute("SELECT * from tb_user_cliente where cli_id = %s and LOWER(us_nome) ilike %s;", (cli_id, "%"+us_nome+"%",))
        results_cli = cur.fetchall()

        cur.close()
        connection.close()

        return results_cli
    except Exception as e:
        return None
    
@app.route('/consulta_usuarios', methods=['POST'])
def consulta_usuarios():

    global clienteID
    cli_id = clienteID
    us_nome = request.form.get('us_nome')

    if cli_id is None:
        results_fun, results_cli = search_usuario(us_nome)
        return render_template('resultsUsuarios.html', results_cli=results_cli, results_fun=results_fun) 
    else:
        results_cli = search_usuario_cliid(us_nome, cli_id)
        return render_template('resultsUsuarios.html', results_cli=results_cli)           


#Inserir equipamentos 
@app.route('/inserir_equipamento', methods=['POST'])
def inserir_equipamento():
    # Recebe os dados do formulário HTML
    eq_id = request.form['eq_id']
    eq_tipo = request.form['eq_tipo']
    eq_marca = request.form['eq_marca']
    eq_modelo = request.form['eq_modelo']
    eq_serial = request.form['eq_serial']
    cli_id = request.form['cli_id']


    # Insere o equipamento no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_equipamento (eq_id, eq_tipo, eq_marca, eq_modelo, eq_serial, cli_id) VALUES (%s, %s, %s, %s, %s, %s);", (eq_id, eq_tipo, eq_marca, eq_modelo, eq_serial, cli_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"


def get_detalhes_cliente_pf(cliente_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("SELECT tb_pf.cli_id, pf_cpf, pf_nome, pf_nomesocial, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email FROM tb_cliente, tb_pf WHERE tb_cliente.cli_id = tb_pf.cli_id AND tb_pf.cli_id = %s;", (cliente_id,))
        detalhes_cliente = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_cliente:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["cli_id", "pf_cpf", "pf_nome", "pf_nomesocial", "cli_endereco", "cli_cep", "cli_telefone", "cli_celular", "cli_email"]
            detalhes_cliente = dict(zip(keys, detalhes_cliente))

        return detalhes_cliente

    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None

def get_detalhes_cliente_pj(cliente_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("SELECT tb_pj.cli_id, pj_cnpj, pj_razaosocial, pj_nomefantasia, cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email FROM tb_cliente, tb_pj WHERE tb_cliente.cli_id = tb_pj.cli_id AND tb_pj.cli_id = %s;", (cliente_id,))
        detalhes_cliente = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_cliente:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["cli_id", "pj_cnpj", "pj_razaosocial", "pj_nomefantasia", "cli_endereco", "cli_cep", "cli_telefone", "cli_celular", "cli_email"]
            detalhes_cliente = dict(zip(keys, detalhes_cliente))

        return detalhes_cliente

    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None
    

@app.route('/editarPF/<string:cliente_id>')
def editar_clientePF(cliente_id):
    detalhes_cliente = get_detalhes_cliente_pf(cliente_id)

    if detalhes_cliente is not None:
        cli_id = detalhes_cliente.get('cli_id')
        pf_cpf = detalhes_cliente.get('pf_cpf')
        pf_nome = detalhes_cliente.get('pf_nome')
        pf_nomesocial = detalhes_cliente.get('pf_nomesocial')
        cli_endereco = detalhes_cliente.get('cli_endereco')
        cli_cep = detalhes_cliente.get('cli_cep')
        cli_telefone = detalhes_cliente.get('cli_telefone')
        cli_celular = detalhes_cliente.get('cli_celular')    
        cli_email = detalhes_cliente.get('cli_email')
        return render_template('editarPF.html', cli_id=cli_id, pf_cpf=pf_cpf, pf_nome=pf_nome, pf_nomesocial=pf_nomesocial, cli_endereco=cli_endereco, cli_cep=cli_cep, cli_telefone=cli_telefone, cli_celular=cli_celular, cli_email=cli_email)

@app.route('/editarPJ/<string:cliente_id>')
def editar_cliente(cliente_id):
    detalhes_cliente = get_detalhes_cliente_pj(cliente_id)

    if detalhes_cliente is not None:
        cli_id = detalhes_cliente.get('cli_id')
        pj_cnpj = detalhes_cliente.get('pj_cnpj')
        pj_razaosocial = detalhes_cliente.get('pj_razaosocial')
        pj_nomefantasia = detalhes_cliente.get('pj_nomefantasia')
        cli_endereco = detalhes_cliente.get('cli_endereco')
        cli_cep = detalhes_cliente.get('cli_cep')
        cli_telefone = detalhes_cliente.get('cli_telefone')
        cli_celular = detalhes_cliente.get('cli_celular')    
        cli_email = detalhes_cliente.get('cli_email')
        return render_template('editarPJ.html', cli_id=cli_id, pj_cnpj=pj_cnpj, pj_razaosocial=pj_razaosocial, pj_nomefantasia=pj_nomefantasia, cli_endereco=cli_endereco, cli_cep=cli_cep, cli_telefone=cli_telefone, cli_celular=cli_celular, cli_email=cli_email)            

@app.route('/editar_PJ', methods=['POST'])
def editar_PJ():
    # Recebe os dados do formulário HTML
    cli_id = request.form['cli_id']
    pj_razaosocial = request.form['pj_razaosocial']
    pj_nomefantasia = request.form['pj_nomefantasia']
    pj_cnpj = request.form['pj_cnpj']
    cli_cep = request.form['cli_cep']
    cli_telefone = request.form['cli_telefone']
    cli_celular = request.form['cli_celular']
    cli_email = request.form['cli_email']
    cli_endereco = request.form['cli_endereco']

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE tb_cliente SET cli_endereco = %s, cli_cep = %s, cli_telefone = %s, cli_celular = %s, cli_email = %s WHERE cli_id = %s;", (cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email, cli_id))
        connection.commit()
        cursor.execute("UPDATE tb_pj SET pj_razaosocial = %s, pj_nomefantasia = %s, pj_cnpj = %s WHERE cli_id = %s;", (pj_razaosocial, pj_nomefantasia, pj_cnpj, cli_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"

@app.route('/editar_PF', methods=['POST'])
def editar_PF():
    # Recebe os dados do formulário HTML
    
    cli_id = request.form['cli_id']
    pf_nome = request.form['pf_nome']
    pf_nomesocial = request.form['pf_nomesocial']
    pf_cpf = request.form['pf_cpf']
    cli_cep = request.form['cli_cep']
    cli_telefone = request.form['cli_telefone']
    cli_celular = request.form['cli_celular']
    cli_email = request.form['cli_email']
    cli_endereco = request.form['cli_endereco']

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE tb_cliente SET cli_endereco = %s, cli_cep = %s, cli_telefone = %s, cli_celular = %s, cli_email = %s WHERE cli_id = %s;", (cli_endereco, cli_cep, cli_telefone, cli_celular, cli_email, cli_id))
        connection.commit()
        cursor.execute("UPDATE tb_pf SET pf_nome = %s, pf_nomesocial = %s, pf_cpf = %s WHERE cli_id = %s;", (pf_nome, pf_nomesocial, pf_cpf, cli_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"

#Inserir user cliente
@app.route('/inserir_user_cliente', methods=['POST'])
def inserir_user_cliente():
    # Recebe os dados do formulário HTML
    us_id = request.form['us_id']
    
    numero = request.form.get('list_box')
    tu_id = numero
    
    us_nome = request.form['us_nome']
    us_celular = request.form['us_celular']
    us_email = request.form['us_email']
    us_login = request.form['us_login']
    us_senha = request.form['us_senha']
    cli_id = request.form['cli_id']
    
    # Insere o usuario cliente no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_user (us_id, tu_id) VALUES (%s, %s);", (us_id, tu_id))
        connection.commit()
        cursor.execute("INSERT INTO tb_user_cliente (us_id, us_nome, us_celular, us_email, us_login, us_senha, cli_id) VALUES (%s, %s, %s, %s, %s, %s, %s);", (us_id, us_nome, us_celular, us_email, us_login, us_senha, cli_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"

#Inserir user funcionario 
@app.route('/inserir_user_funcionario', methods=['POST'])
def inserir_user_funcioanrio():
    # Recebe os dados do formulário HTML
    us_id = request.form['us_id']
    
    numero = request.form.get('list_funcionario')
    
    tu_id = numero
    set_id = request.form.get('selectSetor')

    fun_nome = request.form['fun_nome']
    fun_cpf = request.form['fun_cpf']
    fun_celular = request.form['fun_celular']
    fun_endereco = request.form['fun_endereco']
    fun_login = request.form['fun_login']
    fun_senha = request.form['fun_senha']
        
    # Insere o usuario cliente no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_user (us_id, tu_id) VALUES (%s, %s);", (us_id, tu_id))
        connection.commit()
        cursor.execute("INSERT INTO tb_user_funcionario (us_id, fun_nome, fun_cpf, fun_celular, fun_endereco, fun_login, fun_senha) VALUES (%s, %s, %s, %s, %s, %s, %s);", (us_id, fun_nome, fun_cpf, fun_celular, fun_endereco, fun_login, fun_senha))
        connection.commit()
        cursor.execute("INSERT INTO tb_sf (set_id, us_id) VALUES (%s, %s);", (set_id, us_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"

#Inserir chamado
@app.route('/inserir_chamado', methods=['POST'])

def inserir_chamado():
    global usuarioid2

    # Recebe os dados do formulário HTML
    cha_id = request.form['cha_id']
    numero = request.form.get('ass_option')
    cha_texto = request.form['cha_texto']
    eq_id = request.form['eq_id']
    cha_hora = datetime.now()
    us_id = int (usuarioid2)

    as_id = request.form.get('selectAssunto')
    out_assunto = request.form['out_assunto']
    

    if out_assunto: 
        try:
            connection = psycopg2.connect(
                host=db_host, port=db_port, database=db_name,
                user=db_user, password=db_password
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tb_chamado (cha_id, cha_texto, eq_id, cha_hora, us_id) VALUES (%s, %s, %s, %s, %s);", (cha_id, cha_texto, eq_id, cha_hora, us_id))           
            connection.commit()
            cursor.execute("INSERT INTO tb_outros (cha_id, out_assunto) VALUES (%s, %s);", (cha_id, out_assunto))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('sucesso'))
        except Exception as e:
            return f"Erro ao inserir os dados no banco de dados: {e}" 
    else:
        try:
            connection = psycopg2.connect(
                host=db_host, port=db_port, database=db_name,
                user=db_user, password=db_password
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tb_chamado (cha_id, cha_texto, cha_hora, as_id, eq_id, us_id) VALUES (%s, %s, %s, %s, %s, %s);", (cha_id, cha_texto, cha_hora, as_id, eq_id, us_id))    
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('sucesso'))
        except Exception as e:
            return f"Erro ao inserir os dados no banco de dados: {e}"  


#Inserir evento 
@app.route('/inserir_evento', methods=['POST'])
def inserir_evento():
    global usuarioid2

    # Recebe os dados do formulário HTML
    eve_id = request.form['eve_id']
    aco_id = request.form.get('aco_resultado')
    us_id = usuarioid2
    set_id = request.form.get('selectSetor')
    sta_id = request.form.get('selectStatus')
    cha_id = request.form['cha_id']
    eve_nota = request.form['eve_nota']
    eve_tempo = request.form['eve_tempo']
    eve_data = datetime.now()


    # Insere o evento no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_evento (eve_id, aco_id, us_id, set_id, sta_id, cha_id, eve_nota, eve_tempo, eve_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (eve_id, aco_id, us_id, set_id, sta_id, cha_id, eve_nota, eve_tempo, eve_data))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"


def login(us_login, us_senha):
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
    )
    global clienteID
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute(f"SELECT * FROM tb_user_cliente, tb_user WHERE tb_user_cliente.us_id = tb_user.us_id AND us_login = %s AND us_senha = %s AND tu_id = '2';", (us_login, us_senha))
    cur2.execute(f"SELECT cli_id FROM tb_user_cliente WHERE us_login = %s AND us_senha = %s", (us_login, us_senha))
    idcliente1 = cur2.fetchone()
    user_cliente_usuario = cur.fetchone()

    cur = connection.cursor()
    cur.execute(f"SELECT * FROM tb_user_cliente, tb_user WHERE tb_user_cliente.us_id = tb_user.us_id AND us_login = %s AND us_senha = %s AND tu_id = '3';", (us_login, us_senha))
    cur2.execute(f"SELECT cli_id FROM tb_user_cliente WHERE us_login = %s AND us_senha = %s", (us_login, us_senha))
    idcliente2 = cur2.fetchone()
    user_cliente_gestor = cur.fetchone()    
    
    cur.execute(f"SELECT * FROM tb_user_funcionario, tb_user WHERE tb_user_funcionario.us_id = tb_user.us_id AND fun_login = %s AND fun_senha = %s AND tu_id = '1';", (us_login, us_senha))
    user_funcionario_adm = cur.fetchone()

    cur.execute(f"SELECT * FROM tb_user_funcionario, tb_user WHERE tb_user_funcionario.us_id = tb_user.us_id AND fun_login = %s AND fun_senha = %s AND tu_id = '2';", (us_login, us_senha))
    user_funcionario_usuario = cur.fetchone()

    cur.execute(f"SELECT * FROM tb_user_funcionario, tb_user WHERE tb_user_funcionario.us_id = tb_user.us_id AND fun_login = %s AND fun_senha = %s AND tu_id = '3';", (us_login, us_senha))
    user_funcionario_gestor = cur.fetchone()  



    if user_cliente_usuario is not None:
        clienteID = idcliente1[0]
        
        return "cliente_usuario"
    elif user_cliente_gestor is not None:
        clienteID = idcliente2[0]
        return "cliente_gestor"    
    elif user_funcionario_adm is not None:
        clienteID = None
        return "funcionario_adm"
    elif user_funcionario_usuario is not None:
        clienteID = None  
        return "funcionario_usuario"
    elif user_funcionario_gestor is not None:
        clienteID = None
        return "funcionario_gestor"    
    else:
        return None
    
@app.route("/login", methods=["POST"])
def logar():
    # Pega a informação do formulário para fazer a autenticação com o usuário
    us_login = request.form["us_login"]
    us_senha = request.form["us_senha"]
    
    tipo_usuario = login(us_login, us_senha)
    global sessao
    global usuarioid2
    usuarioid = None
    sessao = None
    sessao = tipo_usuario

    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
    )
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT us_id FROM tb_user_funcionario WHERE fun_login = %s", (us_login,))
    cur2.execute("SELECT us_id FROM tb_user_cliente WHERE us_login = %s", (us_login,))
    usuarioid = cur.fetchone()

    if usuarioid:
        usuarioid2 = usuarioid[0]
    else:
        usuarioid = cur2.fetchone()
        usuarioid2 = usuarioid[0]
        
    if tipo_usuario == "cliente_usuario":
        return redirect("/telausercliente")
    
    elif tipo_usuario == "cliente_gestor":
        return redirect("/telausergestor")    
    
    elif tipo_usuario == "funcionario_adm":
        return redirect("/telaadm")
    
    elif tipo_usuario == "funcionario_usuario":
        return redirect("/telausuario")
    
    elif tipo_usuario == "funcionario_gestor":
        return redirect("/telaGestor")
        
    else:
        return redirect("/loginerror")

@app.route("/url_voltar", methods=["GET"])
def voltar():
    
    global sessao
    usuario_tipo = sessao

    if usuario_tipo == "cliente_usuario":
        return redirect("/telausercliente")
    
    elif usuario_tipo == "cliente_gestor":
        return redirect("/telausergestor")    
    
    elif usuario_tipo == "funcionario_adm":
        return redirect("/telaadm")
    
    elif usuario_tipo == "funcionario_usuario":
        return redirect("/telausuario")
    
    elif usuario_tipo == "funcionario_gestor":
        return redirect("/telaGestor")
        
    else:
        return redirect("/loginerror")
      
def get_detalhes_us_cli(us_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("SELECT tb_user_cliente.us_id, us_nome, us_celular, us_email, us_login, tu_id, cli_id FROM tb_user_cliente,tb_user WHERE tb_user_cliente.us_id = tb_user.us_id and tb_user_cliente.us_id = %s;", (us_id,))
        detalhes_us_cli = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_us_cli:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["us_id", "us_nome", "us_celular", "us_email", "us_login", "tu_id", "cli_id"]
            detalhes_us_cli = dict(zip(keys, detalhes_us_cli))

        return detalhes_us_cli

    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None

@app.route('/editarUserCliente/<string:us_id>')
def editar_userCliente(us_id):
    us_id = str(us_id)
    print (us_id)
    detalhes_us_cli = get_detalhes_us_cli(us_id)


    us_id = detalhes_us_cli.get('us_id')
    us_nome = detalhes_us_cli.get('us_nome')
    us_celular = detalhes_us_cli.get('us_celular')
    us_email = detalhes_us_cli.get('us_email')
    us_login = detalhes_us_cli.get('us_login')
    tu_id = detalhes_us_cli.get('tu_id')
    cli_id = detalhes_us_cli.get('cli_id')
    
    return render_template('editarUserCliente.html', us_id = us_id, us_nome = us_nome, us_celular = us_celular, us_email = us_email, us_login = us_login, tu_id = tu_id, cli_id = cli_id)   

@app.route('/editar_user_cliente', methods=['POST'])
def editar_user_cliente():
    # Recebe os dados do formulário HTML
    us_id = request.form['us_id']
    us_nome = request.form['us_nome']
    us_celular = request.form['us_celular']
    us_email = request.form['us_email']
    us_login = request.form['us_login']
    cli_id = request.form['cli_id']

    numero = request.form.get('list_box')
    tu_id = numero

    us_senha = request.form['us_senha']



    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE tb_user_cliente SET us_nome = %s, us_celular = %s, us_email = %s, us_login = %s, cli_id = %s WHERE us_id = %s;", (us_nome, us_celular, us_email, us_login, cli_id, us_id))
        connection.commit()
        if us_senha:
            cursor.execute("UPDATE tb_user_cliente SET us_senha = %s WHERE us_id = %s;", (us_senha, us_id))
            connection.commit()
        
        cursor.execute("UPDATE tb_user SET tu_id = %s WHERE us_id = %s;", (tu_id, us_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"
            

def get_detalhes_us_fun(us_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("SELECT tb_user_funcionario.us_id, fun_nome, fun_CPF, fun_celular, fun_endereco, fun_login, tu_id, set_id FROM tb_user_funcionario,tb_user, tb_sf WHERE tb_user_funcionario.us_id = tb_sf.us_id and tb_user_funcionario.us_id = tb_user.us_id and tb_user_funcionario.us_id = %s;", (us_id,))
        detalhes_us_fun = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_us_fun:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["us_id", "fun_nome", "fun_CPF", "fun_celular", "fun_endereco", "fun_login", "tu_id", "set_id"]
            detalhes_us_fun = dict(zip(keys, detalhes_us_fun))

        return detalhes_us_fun

    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None

@app.route('/editarUserFuncionario/<string:us_id>')
def editar_userFuncionario(us_id):
    us_id = str(us_id)
    detalhes_us_fun = get_detalhes_us_fun(us_id)


    us_id = detalhes_us_fun.get('us_id')
    fun_nome = detalhes_us_fun.get('fun_nome')
    fun_CPF = detalhes_us_fun.get('fun_CPF')
    fun_celular = detalhes_us_fun.get('fun_celular')
    fun_endereco = detalhes_us_fun.get('fun_endereco')
    fun_login = detalhes_us_fun.get('fun_login')
    tu_id = detalhes_us_fun.get('tu_id')
    set_id = detalhes_us_fun.get('set_id')

    selectSetor = getSelectSetor()

    
    return render_template('editarUserFuncionario.html', us_id = us_id, fun_nome = fun_nome, fun_CPF = fun_CPF, fun_celular = fun_celular, fun_endereco = fun_endereco, fun_login = fun_login, tu_id = tu_id, set_id = set_id, selectSetor = selectSetor)         

@app.route('/editar_user_funcionario', methods=['POST'])
def editar_user_funcionario():
    # Recebe os dados do formulário HTML
    us_id = request.form['us_id']
    fun_nome = request.form['fun_nome']
    fun_cpf = request.form['fun_CPF']
    fun_celular = request.form['fun_celular']
    fun_endereco = request.form['fun_endereco']
    fun_login = request.form['fun_login']
    fun_senha = request.form['fun_senha']
    fun_senha = str(fun_senha)

    numero = request.form.get('list_box')
    tu_id = numero

    set_id = request.form.get('selectSetor')

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE tb_user_funcionario SET fun_nome = %s, fun_cpf = %s, fun_celular = %s, fun_endereco = %s, fun_login = %s WHERE us_id = %s;", (fun_nome, fun_cpf, fun_celular, fun_endereco, fun_login, us_id))
        connection.commit()

        if fun_senha:
            cursor.execute("UPDATE tb_user_funcionario SET fun_senha = %s WHERE us_id = %s;", (fun_senha, us_id))
            connection.commit()
      
        cursor.execute("UPDATE tb_user SET tu_id = %s WHERE us_id = %s", (tu_id, us_id))
        connection.commit()

        cursor.execute("UPDATE tb_sf SET set_id = %s WHERE us_id = %s", (set_id, us_id))
        connection.commit()

        
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"
    
#Consultar assunto
def search_assunto(as_nome):
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Consulta na tabela tb_assunto
        cur.execute("SELECT * FROM tb_assunto WHERE LOWER(as_nome) ilike %s;", ("%"+as_nome+"%",))
        resultados = cur.fetchall()

        cur.close()
        connection.close()
        return resultados
    except Exception as e:
        return None

@app.route('/consulta_assunto', methods=['POST'])
def consulta_assunto():
    as_nome = request.form.get('as_nome')
    
    results_assuntos = search_assunto(as_nome)
    return render_template('resultsAssunto.html', results_assuntos=results_assuntos)    

def get_detalhes_as_id(as_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("SELECT * FROM tb_assunto WHERE as_id = %s;", (as_id,))
        detalhes_assunto = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_assunto:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["as_id", "as_nome"]
            detalhes_assunto = dict(zip(keys, detalhes_assunto))

        return detalhes_assunto

    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None

@app.route('/editarAssunto/<string:as_id>')
def editar_editarAssunto(as_id):
    as_id = str(as_id)
    detalhes_assunto = get_detalhes_as_id(as_id)


    as_id = detalhes_assunto.get('as_id')
    as_nome = detalhes_assunto.get('as_nome')


    
    return render_template('editarAssunto.html', as_id = as_id, as_nome = as_nome)

@app.route('/editar_assunto', methods=['POST'])
def editar_assunto():
    # Recebe os dados do formulário HTML
    as_id = request.form['as_id']
    as_nome = request.form['as_nome']

    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE tb_assunto SET as_nome = %s WHERE as_id = %s;", (as_nome, as_id))
        connection.commit()

        
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"

#Consultar equipamento
def search_equipamento(eq_tipo):
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Consulta na tabela tb_equipamento_pj
        cur.execute("select eq_id, eq_tipo, eq_marca, eq_modelo, eq_serial, pj_nomefantasia, tb_equipamento.cli_id from tb_equipamento, tb_pj, tb_cliente WHERE tb_equipamento.cli_id = tb_cliente.cli_id and tb_pj.cli_id = tb_cliente.cli_id and lower(eq_tipo) ilike %s;", ("%"+eq_tipo+"%",))
        resultados_eq_pj = cur.fetchall()

        # Consulta na tabela tb_equipamento_pf
        cur.execute("select eq_id, eq_tipo, eq_marca, eq_modelo, eq_serial, pf_nomesocial, tb_equipamento.cli_id from tb_equipamento, tb_pf, tb_cliente WHERE tb_equipamento.cli_id = tb_cliente.cli_id and tb_pf.cli_id = tb_cliente.cli_id and lower(eq_tipo) ilike %s;", ("%"+eq_tipo+"%",))
        resultados_eq_pf = cur.fetchall()

        cur.close()
        connection.close()
        return resultados_eq_pf, resultados_eq_pj
    except Exception as e:
        return None
    
def search_equipamento_clidid(eq_tipo,cli_id):
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Consulta na tabela tb_equipamento_pj
        cur.execute("select eq_id, eq_tipo, eq_marca, eq_modelo, eq_serial, pj_nomefantasia, tb_equipamento.cli_id from tb_equipamento, tb_pj, tb_cliente WHERE tb_equipamento.cli_id = tb_cliente.cli_id and tb_pj.cli_id = tb_cliente.cli_id and tb_cliente.cli_id = %s and lower(eq_tipo) ilike %s;", (cli_id,"%"+eq_tipo+"%",))
        resultados_eq_pj = cur.fetchall()

        # Consulta na tabela tb_equipamento_pf
        cur.execute("select eq_id, eq_tipo, eq_marca, eq_modelo, eq_serial, pf_nomesocial, tb_equipamento.cli_id from tb_equipamento, tb_pf, tb_cliente WHERE tb_equipamento.cli_id = tb_cliente.cli_id and tb_pf.cli_id = tb_cliente.cli_id and tb_cliente.cli_id = %s and lower(eq_tipo) ilike %s;", (cli_id,"%"+eq_tipo+"%",))
        resultados_eq_pf = cur.fetchall()

        cur.close()
        connection.close()
        return resultados_eq_pf, resultados_eq_pj
    except Exception as e:
        return None    

@app.route('/consulta_equipamento', methods=['POST'])
def consulta_equipamento():
    global clienteID
    cli_id = clienteID
    if cli_id is None:
        eq_tipo = request.form.get('eq_tipo')
        resultados_eq_pf, resultados_eq_pj = search_equipamento(eq_tipo)
        return render_template('resultsEquipamento.html', resultados_eq_pf=resultados_eq_pf, resultados_eq_pj=resultados_eq_pj)
    else:
        eq_tipo = request.form.get('eq_tipo')
        resultados_eq_pf, resultados_eq_pj = search_equipamento_clidid(eq_tipo, cli_id)
        return render_template('resultsEquipamento.html', resultados_eq_pf=resultados_eq_pf, resultados_eq_pj=resultados_eq_pj)

def get_detalhes_equipamento(eq_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("select * from tb_equipamento where eq_id = %s;", (eq_id,))
        detalhes_equipamento = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_equipamento:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["eq_id", "eq_tipo", "eq_marca", "eq_modelo", "eq_serial", "cli_id"]
            detalhes_equipamento = dict(zip(keys, detalhes_equipamento))

        return detalhes_equipamento

    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None

@app.route('/editarEquipamento/<string:eq_id>')
def editarEquipamento(eq_id):
    detalhes_equipamento = get_detalhes_equipamento(eq_id)

    if detalhes_equipamento is not None:
        eq_id = detalhes_equipamento.get('eq_id')
        eq_tipo = detalhes_equipamento.get('eq_tipo')
        eq_marca = detalhes_equipamento.get('eq_marca')
        eq_modelo = detalhes_equipamento.get('eq_modelo')
        eq_serial = detalhes_equipamento.get('eq_serial')
        cli_id = detalhes_equipamento.get('cli_id')

        return render_template('editarEquipamento.html', eq_id=eq_id, eq_tipo=eq_tipo, eq_marca=eq_marca, eq_modelo=eq_modelo, eq_serial=eq_serial, cli_id=cli_id)

@app.route('/editar_equipamento', methods=['POST'])
def editar_equipamento():
    # Recebe os dados do formulário HTML
    eq_id = request.form['eq_id']
    eq_tipo = request.form['eq_tipo']
    eq_marca = request.form['eq_marca']
    eq_modelo = request.form['eq_modelo']
    eq_serial = request.form['eq_serial']


    # Insere os assunto no banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE tb_equipamento SET eq_tipo = %s, eq_marca = %s, eq_modelo = %s, eq_serial = %s WHERE eq_id = %s;", (eq_tipo, eq_marca, eq_modelo, eq_serial, eq_id))
        connection.commit()

        
        cursor.close()
        connection.close()
        return redirect(url_for('sucesso'))
    except Exception as e:
        return f"Erro ao inserir os dados no banco de dados: {e}"
    
@app.route('/consulta_cliente_readonly', methods=['POST'])
def consulta_cliente_readonly():
    nome = request.form.get('nome')
    
    results_pf, results_pj = search_cliente(nome)
    return render_template('resultsClienteReadOnly.html', results_pf=results_pf, results_pj=results_pj) 

@app.route('/detalhesPF/<string:cliente_id>')
def detalhes_clientePF(cliente_id):
    detalhes_cliente = get_detalhes_cliente_pf(cliente_id)

    if detalhes_cliente is not None:
        cli_id = detalhes_cliente.get('cli_id')
        pf_cpf = detalhes_cliente.get('pf_cpf')
        pf_nome = detalhes_cliente.get('pf_nome')
        pf_nomesocial = detalhes_cliente.get('pf_nomesocial')
        cli_endereco = detalhes_cliente.get('cli_endereco')
        cli_cep = detalhes_cliente.get('cli_cep')
        cli_telefone = detalhes_cliente.get('cli_telefone')
        cli_celular = detalhes_cliente.get('cli_celular')    
        cli_email = detalhes_cliente.get('cli_email')
        return render_template('detalhesPF.html', cli_id=cli_id, pf_cpf=pf_cpf, pf_nome=pf_nome, pf_nomesocial=pf_nomesocial, cli_endereco=cli_endereco, cli_cep=cli_cep, cli_telefone=cli_telefone, cli_celular=cli_celular, cli_email=cli_email)

@app.route('/detalhesPJ/<string:cliente_id>')
def detalhes_cliente(cliente_id):
    detalhes_cliente = get_detalhes_cliente_pj(cliente_id)

    if detalhes_cliente is not None:
        cli_id = detalhes_cliente.get('cli_id')
        pj_cnpj = detalhes_cliente.get('pj_cnpj')
        pj_razaosocial = detalhes_cliente.get('pj_razaosocial')
        pj_nomefantasia = detalhes_cliente.get('pj_nomefantasia')
        cli_endereco = detalhes_cliente.get('cli_endereco')
        cli_cep = detalhes_cliente.get('cli_cep')
        cli_telefone = detalhes_cliente.get('cli_telefone')
        cli_celular = detalhes_cliente.get('cli_celular')    
        cli_email = detalhes_cliente.get('cli_email')
        return render_template('detalhesPJ.html', cli_id=cli_id, pj_cnpj=pj_cnpj, pj_razaosocial=pj_razaosocial, pj_nomefantasia=pj_nomefantasia, cli_endereco=cli_endereco, cli_cep=cli_cep, cli_telefone=cli_telefone, cli_celular=cli_celular, cli_email=cli_email)   

def getSelectEquipamento():

    global clienteID
    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cli_id = clienteID
    cli_id = str(cli_id)
    cur = connection.cursor()
    cur.execute("SELECT eq_id, eq_tipo, eq_serial FROM tb_equipamento where cli_id = %s", (cli_id))
    selectEquipamento = []

    for row in cur:
        selectEquipamento.append({"eq_id": row[0],"eq_tipo": row[1],"eq_serial": row[2]})

    connection.close()

    return selectEquipamento

def getSelectAssunto():

    connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
    
    cur = connection.cursor()
    cur.execute("SELECT * from tb_assunto")
    selectAssunto = []

    for row in cur:
        selectAssunto.append({"as_id": row[0],"as_nome": row[1]})

    connection.close()

    return selectAssunto

#Inserir chamado
@app.route('/inserir_chamado_cliente', methods=['POST'])

def inserir_chamado_cliente():
    global usuarioid2

    # Recebe os dados do formulário HTML
    cha_id = request.form['cha_id']
    cha_texto = request.form['cha_texto']
    eq_id = request.form.get('selectEquipamento')
    cha_hora = datetime.now()
    us_id = int (usuarioid2)

    as_id = request.form.get('selectAssunto')
    out_assunto = request.form['out_assunto']  

    if out_assunto: 
        try:
            connection = psycopg2.connect(
                host=db_host, port=db_port, database=db_name,
                user=db_user, password=db_password
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tb_chamado (cha_id, cha_texto, eq_id, cha_hora, us_id) VALUES (%s, %s, %s, %s, %s);", (cha_id, cha_texto, eq_id, cha_hora, us_id))           
            connection.commit()
            cursor.execute("INSERT INTO tb_outros (cha_id, out_assunto) VALUES (%s, %s);", (cha_id, out_assunto))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('sucesso'))
        except Exception as e:
            return f"Erro ao inserir os dados no banco de dados: {e}" 
    else:
        try:
            connection = psycopg2.connect(
                host=db_host, port=db_port, database=db_name,
                user=db_user, password=db_password
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tb_chamado (cha_id, cha_texto, cha_hora, as_id, eq_id, us_id) VALUES (%s, %s, %s, %s, %s, %s);", (cha_id, cha_texto, cha_hora, as_id, eq_id, us_id))    
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('sucesso'))
        except Exception as e:
            return f"Erro ao inserir os dados no banco de dados: {e}"  

@app.route('/usuarioCliente')
def usuarioCliente():
    global clienteID
    connection = psycopg2.connect(
        host=db_host, port=db_port, database=db_name,
        user=db_user, password=db_password
    )
    
    cursor = connection.cursor()
    cursor.execute('SELECT MAX (us_id) FROM tb_user')

    us_id = cursor.fetchone()[0]
    cli_id = clienteID

    if us_id is not None:
        us_id = us_id + 1
    else:
        us_id = 1  

    selectSetor = getSelectSetor()
    


    return render_template('usuarioCliente.html', us_id=us_id, selectSetor = selectSetor, cli_id=cli_id)  

def search_chamado_chadid(cha_id):
    
    
    
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        
        # Consulta na tabela tb_equipamento_pj
        cur.execute("select cha_id, pj_nomefantasia, as_nome from tb_chamado, tb_pj, tb_assunto, tb_cliente, tb_equipamento where tb_pj.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.as_id = tb_assunto.as_id and tb_chamado.cha_id = %s;", (cha_id,))
        resultados_pj_ass = cur.fetchall()

        cur.execute("select tb_chamado.cha_id, pj_nomefantasia, out_assunto from tb_chamado, tb_pj, tb_outros, tb_cliente, tb_equipamento where tb_pj.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = tb_outros.cha_id and tb_chamado.cha_id = %s;", (cha_id,))
        resultados_pj_out = cur.fetchall()        

        cur.execute("select cha_id, pf_nomesocial, as_nome from tb_chamado, tb_pf, tb_assunto, tb_cliente, tb_equipamento where tb_pf.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.as_id = tb_assunto.as_id and tb_chamado.cha_id = %s;", (cha_id,))
        resultados_pf_ass = cur.fetchall()  

        cur.execute("select tb_chamado.cha_id, pf_nomesocial, out_assunto from tb_chamado, tb_pf, tb_outros, tb_cliente, tb_equipamento where tb_pf.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = tb_outros.cha_id and tb_chamado.cha_id = %s;", (cha_id,))
        resultados_pf_out = cur.fetchall()  

        cur.close()
        connection.close()
        return resultados_pj_ass, resultados_pj_out, resultados_pf_ass, resultados_pf_out
    except Exception as e:
        return None    

def search_chamado_todes():
    try:
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )
        cur = connection.cursor()

        cur.execute("select cha_id, pj_nomefantasia, as_nome from tb_chamado, tb_pj, tb_assunto, tb_cliente, tb_equipamento where tb_pj.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.as_id = tb_assunto.as_id;")
        resultados_pj_ass = cur.fetchall()

        cur.execute("select tb_chamado.cha_id, pj_nomefantasia, out_assunto from tb_chamado, tb_pj, tb_outros, tb_cliente, tb_equipamento where tb_pj.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = tb_outros.cha_id;")
        resultados_pj_out = cur.fetchall()        

        cur.execute("select cha_id, pf_nomesocial, as_nome from tb_chamado, tb_pf, tb_assunto, tb_cliente, tb_equipamento where tb_pf.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.as_id = tb_assunto.as_id;")
        resultados_pf_ass = cur.fetchall()  

        cur.execute("select tb_chamado.cha_id, pf_nomesocial, out_assunto from tb_chamado, tb_pf, tb_outros, tb_cliente, tb_equipamento where tb_pf.cli_id = tb_cliente.cli_id and tb_equipamento.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = tb_outros.cha_id;")
        resultados_pf_out = cur.fetchall()   

        cur.close()
        connection.close()
        return resultados_pj_ass, resultados_pj_out, resultados_pf_ass, resultados_pf_out       
    except Exception as e:
        return None
    
@app.route('/consulta_chamado', methods=['POST'])
def consulta_chamado():
 

    cha_id = request.form.get('cha_id')
    if cha_id:
        resultados_pj_ass, resultados_pj_out, resultados_pf_ass, resultados_pf_out = search_chamado_chadid(cha_id)
    else:
        resultados_pj_ass, resultados_pj_out, resultados_pf_ass, resultados_pf_out = search_chamado_todes()    
    return render_template('resultsChamados.html', resultados_pj_ass = resultados_pj_ass, resultados_pj_out = resultados_pj_out, resultados_pf_ass = resultados_pf_ass, resultados_pf_out = resultados_pf_out)

def get_detalhes_cha_pj_as(cha_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("select tb_chamado.cha_id, us_nome, pj_nomefantasia, as_nome, eq_tipo, eq_serial, cha_texto, cha_hora from tb_chamado, tb_assunto, tb_equipamento, tb_user_cliente, tb_cliente, tb_pj, tb_user where tb_chamado.as_id = tb_assunto.as_id and tb_chamado.us_id = tb_user.us_id and tb_user_cliente.us_id = tb_user.us_id and tb_cliente.cli_id = tb_user_cliente.cli_id and tb_pj.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = %s;", (cha_id,))
        get_detalhes_cha_pj_as = cur.fetchone()

        cur.close()
        connection.close()

        if get_detalhes_cha_pj_as:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["cha_id", "us_nome", "pj_nomefantasia", "as_nome", "eq_tipo", "eq_serial", "cha_texto", "cha_hora"]
            get_detalhes_cha_pj_as = dict(zip(keys, get_detalhes_cha_pj_as))

        return get_detalhes_cha_pj_as
    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None    

@app.route('/detalhesChamadoPJass/<string:cha_id>')
def detalhes_ChamadoPJass(cha_id):
    detalhes_cha_pj_as = get_detalhes_cha_pj_as(cha_id)

    if detalhes_cha_pj_as is not None:
        cha_id = detalhes_cha_pj_as.get('cha_id')
        us_nome = detalhes_cha_pj_as.get('us_nome')
        pj_nomefantasia = detalhes_cha_pj_as.get('pj_nomefantasia')
        as_nome = detalhes_cha_pj_as.get('as_nome')
        eq_tipo = detalhes_cha_pj_as.get('eq_tipo')
        eq_serial = detalhes_cha_pj_as.get('eq_serial')
        cha_texto = detalhes_cha_pj_as.get('cha_texto')
        cha_hora = detalhes_cha_pj_as.get('cha_hora')    
        
        return render_template('detalhesChanadoPJass.html', cha_id=cha_id, us_nome=us_nome, pj_nomefantasia=pj_nomefantasia, as_nome=as_nome, eq_tipo=eq_tipo, eq_serial=eq_serial, cha_texto=cha_texto, cha_hora=cha_hora)

def get_detalhes_cha_pj_out(cha_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("select tb_chamado.cha_id, us_nome, pj_nomefantasia, out_assunto, eq_tipo, eq_serial, cha_texto, cha_hora from tb_chamado, tb_outros, tb_equipamento, tb_user_cliente, tb_cliente, tb_pj, tb_user where tb_chamado.cha_id = tb_outros.cha_id and tb_chamado.us_id = tb_user.us_id and tb_user_cliente.us_id = tb_user.us_id and tb_cliente.cli_id = tb_user_cliente.cli_id and tb_pj.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = %s;", (cha_id,))
        get_detalhes_cha_pj_out = cur.fetchone()

        cur.close()
        connection.close()

        if get_detalhes_cha_pj_out:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["cha_id", "us_nome", "pj_nomefantasia", "out_assunto", "eq_tipo", "eq_serial", "cha_texto", "cha_hora"]
            get_detalhes_cha_pj_out = dict(zip(keys, get_detalhes_cha_pj_out))

        return get_detalhes_cha_pj_out
    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None 

@app.route('/detalhesChamadoPJout/<string:cha_id>')
def detalhes_ChamadoPJout(cha_id):
    detalhes_cha_pj_out = get_detalhes_cha_pj_out(cha_id)

    if detalhes_cha_pj_out is not None:
        cha_id = detalhes_cha_pj_out.get('cha_id')
        us_nome = detalhes_cha_pj_out.get('us_nome')
        pj_nomefantasia = detalhes_cha_pj_out.get('pj_nomefantasia')
        out_assunto = detalhes_cha_pj_out.get('out_assunto')
        eq_tipo = detalhes_cha_pj_out.get('eq_tipo')
        eq_serial = detalhes_cha_pj_out.get('eq_serial')
        cha_texto = detalhes_cha_pj_out.get('cha_texto')
        cha_hora = detalhes_cha_pj_out.get('cha_hora')    
        
        return render_template('detalhesChanadoPJout.html', cha_id=cha_id, us_nome=us_nome, pj_nomefantasia=pj_nomefantasia, out_assunto=out_assunto, eq_tipo=eq_tipo, eq_serial=eq_serial, cha_texto=cha_texto, cha_hora=cha_hora)

def get_detalhes_cha_pf_as(cha_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("select tb_chamado.cha_id, us_nome, pf_nomesocial, as_nome, eq_tipo, eq_serial, cha_texto, cha_hora from tb_chamado, tb_assunto, tb_equipamento, tb_user_cliente, tb_cliente, tb_pf, tb_user where tb_chamado.as_id = tb_assunto.as_id and tb_chamado.us_id = tb_user.us_id and tb_user_cliente.us_id = tb_user.us_id and tb_cliente.cli_id = tb_user_cliente.cli_id and tb_pf.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = %s;", (cha_id,))
        detalhes_cha_pf_as = cur.fetchone()

        cur.close()
        connection.close()

        if detalhes_cha_pf_as:
            # Convertemos a tupla de detalhes em um dicionário para facilitar o acesso aos dados
            keys = ["cha_id", "us_nome", "pf_nomesocial", "as_nome", "eq_tipo", "eq_serial", "cha_texto", "cha_hora"]
            detalhes_cha_pf_as = dict(zip(keys, detalhes_cha_pf_as))

        return detalhes_cha_pf_as
    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None  

@app.route('/detalhesChamadoPFass/<string:cha_id>')
def detalhes_ChamadoPFass(cha_id):
    detalhes_cha_pf_as = get_detalhes_cha_pf_as(cha_id)

    if detalhes_cha_pf_as is not None:
        cha_id = detalhes_cha_pf_as.get('cha_id')
        us_nome = detalhes_cha_pf_as.get('us_nome')
        pf_nomesocial = detalhes_cha_pf_as.get('pf_nomesocial')
        as_nome = detalhes_cha_pf_as.get('as_nome')
        eq_tipo = detalhes_cha_pf_as.get('eq_tipo')
        eq_serial = detalhes_cha_pf_as.get('eq_serial')
        cha_texto = detalhes_cha_pf_as.get('cha_texto')
        cha_hora = detalhes_cha_pf_as.get('cha_hora')    
        
        return render_template('detalhesChanadoPFass.html', cha_id=cha_id, us_nome=us_nome, pf_nomesocial=pf_nomesocial, as_nome=as_nome, eq_tipo=eq_tipo, eq_serial=eq_serial, cha_texto=cha_texto, cha_hora=cha_hora)

def get_detalhes_cha_pf_out(cha_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("select tb_chamado.cha_id, us_nome, pf_nomesocial, out_assunto, eq_tipo, eq_serial, cha_texto, cha_hora from tb_chamado, tb_outros, tb_equipamento, tb_user_cliente, tb_cliente, tb_pf, tb_user where tb_chamado.cha_id = tb_outros.cha_id and tb_chamado.us_id = tb_user.us_id and tb_user_cliente.us_id = tb_user.us_id and tb_cliente.cli_id = tb_user_cliente.cli_id and tb_pf.cli_id = tb_cliente.cli_id and tb_chamado.eq_id = tb_equipamento.eq_id and tb_chamado.cha_id = %s;", (cha_id,))
        detalhes_cha_pf_out = cur.fetchall()

        cur.close()
        connection.close()

        return detalhes_cha_pf_out
    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None 

@app.route('/detalhesChamadoPFout/<string:cha_id>')
def detalhes_ChamadoPFout(cha_id):
    detalhes_cha_pf_out = get_detalhes_cha_pf_out(cha_id)


    cha_id = detalhes_cha_pf_out.get('cha_id')
    us_nome = detalhes_cha_pf_out.get('us_nome')
    pf_nomesocial = detalhes_cha_pf_out.get('pf_nomesocial')
    out_assunto = detalhes_cha_pf_out.get('out_assunto')
    eq_tipo = detalhes_cha_pf_out.get('eq_tipo')
    eq_serial = detalhes_cha_pf_out.get('eq_serial')
    cha_texto = detalhes_cha_pf_out.get('cha_texto')
    cha_hora = detalhes_cha_pf_out.get('cha_hora')    
        
    return render_template('detalhesChanadoPFout.html', cha_id=cha_id, us_nome=us_nome, pf_nomesocial=pf_nomesocial, out_assunto=out_assunto, eq_tipo=eq_tipo, eq_serial=eq_serial, cha_texto=cha_texto, cha_hora=cha_hora)

def get_detalhes_eventos(cha_id):
    try:
        # Estabeleça uma conexão com o banco de dados
        connection = psycopg2.connect(
            host=db_host, port=db_port, database=db_name,
            user=db_user, password=db_password
        )

        cur = connection.cursor()

        # Execute uma consulta para recuperar os detalhes do cliente com base no cliente_id
        cur.execute("select eve_id, us_id, set_nome, sta_nome, eve_nota, eve_data from tb_evento, tb_setor, tb_acoes, tb_status where tb_evento.sta_id = tb_status.sta_id and tb_evento.aco_id = tb_acoes.aco_id and tb_evento.set_id = tb_setor.set_id and cha_id = %s;", (cha_id,))
        detalhes_eventos = cur.fetchall()

        cur.close()
        connection.close()

        return detalhes_eventos
    except Exception as e:
        print(f"Erro ao recuperar detalhes do cliente: {str(e)}")
        return None 

@app.route('/consulta_evento', methods=['POST'])
def consulta_evento():
 

    cha_id = request.form.get('cha_id')

    detalhes_eventos = get_detalhes_eventos(cha_id)

 
    return render_template('resultsEventos.html', detalhes_eventos = detalhes_eventos)

if __name__ == '__main__':
    app.run()