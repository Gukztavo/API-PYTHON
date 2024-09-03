EndPoints:
1- Listar Receitas:
    GET/receitas

2- Listar Ingredientes
    GET/ingredientes

3- Lista um unico ingrediente 
    GET/ingrediente{id}

4- Cria nova Receitas
    POST/receita
    {
        "nome":"Nome receita",
        "ingredientes":[id_ingrediente,id_ingrediente,]
    }

5- Cria novo ingrediente
    POST/ingrediente

    {
        "nome":"nome ingrediente"
    }

6- Atualizar Receita
    PUT/receita/{id}

    {
        "nome":"Novo nome receita",
        "ingredientes":[id_ingrediente,id_ingrediente]

    }

7- Atualizar ingrediente
    PUT/ingrediente/{id}
        {
            "nome":"nome ingrediente"       
        }

8- Delete Ingrediente
    DELETE/ingrediente/{id}
        
9- Filtrar Receita por ingrediente
    GET/receita/filtrar

    ex: /receita/filtrar?ingredientes=1
