from flask import Flask, Response, request
import ssl
from urllib.parse import quote_plus
from sqlalchemy import create_engine


app = Flask(__name__)

@app.route ("/parkingplustickets/ws/validacaoTicketsService", methods=['GET','POST'])
def hello_world():
    parametros = (
        # Driver que será utilizado na conexão
        'DRIVER={ODBC Driver 13 for SQL Server};'
        # IP ou nome do servidor.
        'SERVER=localhost\SQLEXPRESS;'
        # Porta
        'PORT=1433;'
        # Banco que será utilizado.
        'DATABASE=parkingnet;'
        # Nome de usuário.
        'UID=sa;'
        # Senha/Token.
        'PWD=325014')

    url_db = quote_plus(parametros)

    db = create_engine("mssql+pyodbc:///?odbc_connect=%s" % url_db)

    conexao = db.connect()

    # resultado = conexao.execute("select * from tabela_preco")
    # for row in resultado:
    #    print(row)

    # sql = "SELECT FirstName, LastName FROM clients WHERE ID = 1"
    # result = engine.execute(sql).fetchone()
    # print(type(result))  # <class 'sqlalchemy.engine.result.Row'>
    # print(result['FirstName'])  # Gord



    if request.method == 'POST':
       body = request.get_data(as_text=True)
       print (body)
       ini =body.find('numeroTicket')+13
       fim = ini +13
       print (body[ini:fim])
       codigobarras = (body[ini:fim])
       ini = body.find('valorCompra') + 12
       fim = body.find('</valorCompra')
       print(body[ini:fim])
       valorcompra = (body[ini:fim])

       sql = """\
         EXEc USP_EFETUA_PAGAMENTO_13DIG @CodigoBarrasPOD = ?, @ValorCompra = ?, @Tarifa = ?
         """

       params = (codigobarras, valorcompra, 1)
       resultado = conexao.execute(sql, params).first()
       print(resultado)
       tipoRetorno, descricaoRetorno, valorTotal, valorAPagar, valorPreValidado, tempoPreValidado = resultado

       xml = f"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:abonarTicketPorValorCompraResponse xmlns:ns2="http://webservices.servicovalidacaotickets.parkingplus.rd.wpssa.com.br/"><return>&lt;DadosTicket&gt;
       &lt;tipoRetorno&gt;{tipoRetorno}&lt;/tipoRetorno&gt;
       &lt;descricaoRetorno&gt;{descricaoRetorno}&lt;/descricaoRetorno&gt;
       &lt;valorTotal&gt;{valorTotal}&lt;/valorTotal&gt;
       &lt;valorAPagar&gt;{valorAPagar}&lt;/valorAPagar&gt;
       &lt;valorPreValidado&gt;{valorPreValidado}&lt;/valorPreValidado&gt;
       &lt;tempoPreValidado&gt;{tempoPreValidado}&lt;/tempoPreValidado&gt;
       &lt;/DadosTicket&gt;</return></ns2:abonarTicketPorValorCompraResponse></soap:Body></soap:Envelope>"""
       print(xml)
       return Response(xml, mimetype='text/xml')


    if request.method == 'GET':
       body1 = request.get_data(as_text=True)
       xml = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:abonarTicketPorValorCompraResponse xmlns:ns2="http://webservices.servicovalidacaotickets.parkingplus.rd.wpssa.com.br/"><return>&lt;DadosTicket&gt;
       &lt;tipoRetorno&gt;0&lt;/tipoRetorno&gt;
       &lt;descricaoRetorno&gt;Ticket Invalido&lt;/descricaoRetorno&gt;
       &lt;valorTotal&gt;0.00&lt;/valorTotal&gt;
       &lt;valorAPagar&gt;0.00&lt;/valorAPagar&gt;
       &lt;valorPreValidado&gt;0.00&lt;/valorPreValidado&gt;
       &lt;tempoPreValidado&gt;0&lt;/tempoPreValidado&gt;
       &lt;/DadosTicket&gt;</return></ns2:abonarTicketPorValorCompraResponse></soap:Body></soap:Envelope>"""
       return  xml



if (__name__) == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE
    context.load_verify_locations('certificado.pem')
    context.load_cert_chain('certificado.pem',keyfile=None, password=None)
    app.run(port=443, host='0.0.0.0', ssl_context=context,  debug=True)
    #app.run(debug=True, port=5000)







