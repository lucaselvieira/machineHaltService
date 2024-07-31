
# Machine Halt Monitoring Service

## Descrição

Este é um serviço REST para monitorar paradas de máquinas, criado utilizando Flask. Ele permite criar, listar, atualizar e deletar registros de paradas de máquinas (ver detalhes na sessão de Endpoints). Inicialmente, o serviço armazena os dados na memória, mas está preparado para ser atualizado para usar um banco de dados no futuro.

## Endpoints

### Criar uma nova parada de máquina
- **URL:** `/machine-halt`
- **Método:** `POST`
- **Corpo da Requisição:**
  ```json
  {
    "machine_tag": "string",  // identificador da máquina
    "start_time": "datetime"  // tempo de início da parada (formato ISO 8601)
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `201 Created`
  - **Corpo:**
    ```json
    {
      "id": "int",
      "machine_tag": "string",
      "start_time": "datetime",
      "end_time": "datetime or null",
      "reason": "string"
    }
    ```

### Obter uma parada de máquina por ID
- **URL:** `/machine-halt/<id>`
- **Método:** `GET`
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Corpo:**
    ```json
    {
      "id": "int",
      "machine_tag": "string",
      "start_time": "datetime",
      "end_time": "datetime or null",
      "reason": "string"
    }
    ```

### Listar paradas de uma máquina dentro de um intervalo de tempo
- **URL:** `/machine-halt/list`
- **Método:** `GET`
- **Parâmetros de Consulta:**
  - `machine_tag`: Identificador da máquina (obrigatório)
  - `interval_start`: Início do intervalo de tempo (formato ISO 8601, obrigatório)
  - `interval_end`: Fim do intervalo de tempo (formato ISO 8601, obrigatório)
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Corpo:**
    ```json
    [
      {
        "id": "int",
        "machine_tag": "string",
        "start_time": "datetime",
        "end_time": "datetime or null",
        "reason": "string"
      }
    ]
    ```

### Atualizar uma parada de máquina
- **URL:** `/machine-halt`
- **Método:** `PUT`
- **Corpo da Requisição:**
  ```json
  {
    "id": "int",          // identificador da parada
    "end_time": "datetime",  // (tempo de finalização da parada (formato ISO 8601)) - (opcional)
    "reason": "string"    // motivo da parada (opcional)
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Corpo:**
    ```json
    {
      "id": "int",
      "machine_tag": "string",
      "start_time": "datetime",
      "end_time": "datetime or null",
      "reason": "string"
    }
    ```

### Deletar todas as paradas de máquinas
- **URL:** `/machine-halt/all`
- **Método:** `DELETE`
- **Resposta de Sucesso:**
  - **Código:** `204 No Content`

## Como Executar

### Pré-requisitos

- Python 3.6 ou superior
- pip

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Executando o Serviço

1. Inicie o servidor Flask:
   ```bash
   python app.py
   ```

2. O serviço estará disponível em `http://127.0.0.1:5000`.

### Testes

1. Para rodar os testes, execute:
   ```bash
   python -m unittest discover -s tests
   ```

## Contribuição

1. Fork este repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/fooBar`).
3. Commit suas mudanças (`git commit -am 'Add some fooBar'`).
4. Push para a branch (`git push origin feature/fooBar`).
5. Crie um novo Pull Request.

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Contato

Seu Nome - [Seu Email](mailto:seu-email@example.com)

Link do Projeto: [https://github.com/seu-usuario/nome-do-repositorio](https://github.com/seu-usuario/nome-do-repositorio)
