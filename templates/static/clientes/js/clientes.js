function add_aparelho() {
    container = document.getElementById('form-aparelho')

    html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='aparelho' class='form-control' name='aparelho' > </div> <div class='col-md'><input type='text' placeholder='modelo' class='form-control' name='modelo' ></div> <div class='col-md'> <input type='number' placeholder='codigo' class='form-control' name='codigo'> </div> </div>"

    container.innerHTML += html
}

function deletar_cliente(delete_id) {
    id = delete_id.getAttribute("value")
    var ask = window.confirm("Tem certeza que deseja excluir o cliente?")
    if (ask) {
        window.alert("Cliente excluido com sucesso!")
        window.location.href = "excluir_cliente/" + id
    }
}