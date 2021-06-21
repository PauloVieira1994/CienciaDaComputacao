from flask import Flask, request, jsonify
app = Flask(__name__)

# --> AREA DE DADOS
client = {
    'name': 'Dummy',
    'is_active': False
}


queues     = []     # relacao de filas
idx_queues = {}     # idx das filas cadastradas

def print_all_queues():
    for queue in queues:
        print(f"Fila {queue['name']}")
        print(f"....: {queue['max']}/{queue['qtd']} ({queue['total']})")
        print(queue['queue'])

@app.route('/client')
def get_client():
    return jsonify(client)

@app.route('/client', methods=['POST'])
def register_client():
    '''
    Cadastro cliente do servico
    @_client dicionario com os campos a serem utilizados
    '''
   
    _client = request.json
    client['name']      = _client['name']
    client['is_active'] = _client['is_active']

    return jsonify(client)

@app.route('/client/active', methods=['POST'])
def update_active_client():
    '''
    Manutencao do status ativo do cliente
    @is_active True/False Ativo/Bloqueado
    '''
    _client = request.json
    client['is_active'] = _client['is_active']

    return jsonify(client)

@app.route('/queues', methods=['POST'])
def add_queue():
    '''
    Adiciona uma fila ao servico
    @dic_queue dicionario com os campos da nova fila
    '''
    dic_queue = request.json

    for filas in dic_queue: 
        idx_queues[filas['name']] = len(queues)
        queues.append(filas)

    
    return jsonify(queues)

@app.route('/queues/<queue_name>')
def get_all_queues():
    return jsonify({
        "idx_queues": idx_queues,
        "queues": queues
    })

@app.route('/element/<queue_name>/<element>', methods=['POST'])
def add_element(queue_name, element):
    #print(f"A fila de nome {queue_name} esta na posicao {idx_queues[queue_name]}")
    #print(queues[idx_queues[queue_name]]['queue'])
    queues[idx_queues[queue_name]]['queue'].append(element)
    queues[idx_queues[queue_name]]['qtd'] += 1

    return jsonify(queues)

@app.route('/element/<queue_name>', methods=['DELETE'])
def del_element(queue_name):
    #print(f"A fila de nome {queue_name} esta na posicao {idx_queues[queue_name]}")
    #print(queues[idx_queues[queue_name]]['queue'])
    queues[idx_queues[queue_name]]['queue'].pop(0)
    queues[idx_queues[queue_name]]['qtd'] -= 1

    return jsonify(queues)
