function add_aparelho() {
    container = document.getElementById('form-aparelho')

    html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='aparelho' class='form-control' name='aparelho' > </div> <div class='col-md'><input type='text' placeholder='modelo' class='form-control' name='modelo' ></div> <div class='col-md'> <input type='number' placeholder='codigo' class='form-control' name='codigo'> </div> </div>"

    container.innerHTML += html
}

function update_cliente() {

    id = document.getElementById('id').value
    nome_completo = document.getElementById('nome_completo').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value

    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,    
        },
        body: JSON.stringify({
            nome_completo: nome_completo,
            email: email,
            cpf: cpf,            
        })
    }).then(function(result){
        return result.json()
    }).then(function(data){
        if(data['status'] == '200') {
            nome_completo = data['nome_completo']
            email = data['email']
            cpf = data['cpf']
            console.log('Dados alterados com sucesso')
        }else {
            console.log('Algo deu errado')
        }


    })

}