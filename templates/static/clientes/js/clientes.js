function add_aparelho() {
    container = document.getElementById('form-aparelho')

    html = "<br>\
    <div class='row'>\
        <div class='col-md'> <input type='text' placeholder='aparelho' class='form-control' name='aparelho'> </div>\
        <div class='col-md'> <input type='text' placeholder='modelo' class='form-control' name='modelo'></div>\
        <div class='col-md'> <input type='number' placeholder='codigo' class='form-control' name='codigo'> </div>\
        <a onclick='remove_aparelho()' class='delete' title='Excluir' data-toggle='tooltip'><i class='material-icons'>&#xE872;</i></a>\
    </div>"

    container.innerHTML += html
}

function remove_aparelho() {
    // remover block acima
}

function deletar_aparelho(id){
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_aparelho = id.getAttribute("value")
    console.log(id_aparelho)
    id_cliente = document.getElementById('id').value

    fetch('/clientes/excluir_aparelho/' + id_aparelho, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            id_cliente: id_cliente,
        })

    })
}

function deletar_cliente(delete_id) {
    id = delete_id.getAttribute("value")
    var ask = window.confirm("Tem certeza que deseja excluir o cliente?")
    if (ask) {
        window.alert("Cliente excluido com sucesso!")
        window.location.href = "excluir_cliente/" + id
    }
}