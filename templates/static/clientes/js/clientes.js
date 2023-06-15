function add_aparelho() {
    container = document.getElementById('form-aparelho')

    html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='aparelho' class='form-control' name='aparelho' > </div> <div class='col-md'><input type='text' placeholder='modelo' class='form-control' name='modelo' ></div> <div class='col-md'> <input type='number' placeholder='codigo' class='form-control' name='codigo'> </div> </div>"

    container.innerHTML += html
}

function exibir_form(tipo) {

    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if(tipo == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    }else if(tipo == "2"){
        add_cliente.style.display = "none";
        att_cliente.style.display = "block"
    }

}

function dados_cliente() {

    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData() // criando formulario vazio
    data.append('id_cliente', id_cliente)  // = 'id_cliente': id_cliente

    fetch("/clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,    
        },
        body: data // enviando dados como formulario
    }).then(function(result){
        return result.json()

    }).then(function(data){
        
        aux = document.getElementById('form-att-cliente')
        aux.style.display = 'block'
        document.getElementById('nome').value = data['cliente']['nome']
        document.getElementById('sobrenome').value = data['cliente']['sobrenome']
        document.getElementById('email').value = data['cliente']['email']
        document.getElementById('cpf').value = data['cliente']['cpf']

        div_aparelhos = document.getElementById('aparelhos')
        div_aparelhos.innerHTML = ""

        for(i=0; i<data['aparelhos'].length; i++) {
            
            div_aparelhos.innerHTML += "<form action='/clientes/update_aparelho/" + data['aparelhos'][i]['id'] + "' method='POST'>\
                <div class='row'>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='aparelho' value='" + data['aparelhos'][i]['fields']['aparelho'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='modelo' value='" + data['aparelhos'][i]['fields']['modelo'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='codigo' value='" + data['aparelhos'][i]['fields']['codigo'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='btn btn-success' type='submit' value='Salvar'>\
                        </div>\
                        </form>\
                        <div class='col-md'>\
                            <a class='btn btn-danger' href='/clientes/excluir_aparelho/" + data['aparelhos'][i]['id'] + "'>Excluir</a>\
                        </div>\
                </div><br>"

        }

    })

}