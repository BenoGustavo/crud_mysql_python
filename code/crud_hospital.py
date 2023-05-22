import mysql.connector

# Conectando ao schema

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hospital_v2"
)

# CRUD HOSPITAL

# Criando hospital


def create_hospital(nome, email, telefone, logradouro, cep, numero, bairro):

    # Criando endereco para o hospital
    def create_endereco(logradouro, cep, numero, bairro):

        cursor = mydb.cursor()
        # Comando mysql
        sql = "INSERT INTO endereco (logradouro, cep, numero, bairro) VALUES (%s, %s, %s, %s)"
        val = (logradouro, cep, numero, bairro)
        cursor.execute(sql, val)
        mydb.commit()
        return cursor.lastrowid

    # Chamando a funcao que cria o endereco para o hospital
    create_endereco(logradouro, cep, numero, bairro)

    cursor = mydb.cursor()

    # Selecionando o ID do endereco
    sql = "SELECT * FROM endereco ORDER BY id_endereco DESC LIMIT 1"
    cursor.execute(sql)
    id_endereco = cursor.fetchone()

    # Tenta criar o hospital, caso não consiga deleta o endereco criado para ele e então finaliza a funcao

    try:
        # Criando o hospital, junto com o ID do respectivo endereco
        sql = "INSERT INTO hospital (nome, email, telefone, id_endereco) VALUES (%s, %s, %s,%s)"
        val = (nome, email, telefone, id_endereco[0],)
        cursor.execute(sql, val)
        mydb.commit()

    except:
        # Selecionando informaçoes
        sql = "SELECT * FROM endereco ORDER BY id_endereco DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()

        sql = "DELETE FROM endereco WHERE id_endereco = %s"
        # o primeiro elemento de 'result' é o ID da última linha
        val = (result[0],)
        cursor.execute(sql, val)
        mydb.commit()

    finally:
        return cursor.lastrowid


# Lendo informacoes da tabela hospital
def read_hospital(id_hospital):
    cursor = mydb.cursor()
    # Comando mysql || pegando informacoes do hospital com ID
    sql = "SELECT * FROM hospital WHERE id_hospital = %s"
    val = (id_hospital,)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    # Comando mysql || pegando informacoes do endereco hospital
    sql = "SELECT * FROM endereco WHERE id_endereco = %s"
    val = (result[4],)
    cursor.execute(sql, val)
    endereco = cursor.fetchone()

    # Retornando informacoes
    if result is None or endereco is None:
        return None
    return {'id': result[0], 'name': result[1], 'telefone': result[2], 'email': result[3], 'logradouro': endereco[1], 'cep': endereco[2], 'numero': endereco[3], 'bairro': endereco[4]}

# Atuailizando informacoes hospital


def update_hospital(id_hospital, nome, email, telefone, logradouro, cep, numero, bairro):
    cursor = mydb.cursor()
    # Comando mysql || atulizando dados
    sql = "UPDATE hospital SET nome = %s, email = %s, telefone = %s WHERE id_hospital = %s"
    val = (nome, email, telefone, id_hospital)
    cursor.execute(sql, val)
    mydb.commit()

    sql = "SELECT * FROM hospital WHERE id_hospital = %s"  # Selecionando ID endereco
    id = (id_hospital,)
    cursor.execute(sql, id)
    endereco = cursor.fetchone()  # Armazenando ID endereco

    # Atuailizando informacoes endereco
    def update_endereco(logradouro, cep, numero, bairro, endereco):

        # Comando mysql || Atuailizar informacoes endereco do hospital
        sql = "UPDATE endereco SET logradouro = %s, cep = %s, numero = %s, bairro = %s WHERE id_endereco = %s"
        val = (logradouro, cep, numero, bairro, endereco)
        cursor.execute(sql, val)
        mydb.commit()
        return cursor.rowcount

    # Funcao que atualiza o endereco
    update_endereco(logradouro, cep, numero, bairro, endereco[4])

    return cursor.rowcount

# Deletando dados hospital


def delete_hospital(id_hospital):

    cursor = mydb.cursor()
    sql = "SELECT * FROM hospital WHERE id_hospital = %s"  # Selecionando ID endereco
    id = (id_hospital,)
    cursor.execute(sql, id)
    id_endereco = cursor.fetchone()  # Armazenando ID endereco

    # Deletando endereco || RECEBENDO ERRO POIS N POSSO DELETAR CHAVE ESTRANGEIRA
    sql = "DELETE FROM endereco WHERE id_endereco = %s"
    val = (id_endereco[4],)
    cursor.execute(sql, val)

    cursor = mydb.cursor()
    # Deletando informacoes do hospital
    sql = "DELETE FROM hospital WHERE id_hospital = %s"
    val = (id_hospital,)
    cursor.execute(sql, val)
    mydb.commit()

    return cursor.rowcount


# Utilizando

# create_hospital("TESTE2","TESTE2@GMAIL.COM","321","LOGRADOURO2","768","876789","BAIRRO2")
# update_hospital("5","nome","string","123","string","123","123","string")
