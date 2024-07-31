
# Machine Halt Monitoring Service

## Descrição

Este é um serviço REST para monitorar paradas de máquinas, criado utilizando Flask. Ele permite criar, listar, atualizar e deletar registros de paradas de máquinas (ver detalhes na sessão de Endpoints). Inicialmente, o serviço armazena os dados na memória, mas está preparado para ser atualizado para usar um banco de dados no futuro.

## Funcionalidades

- **Criar Parada de Máquina**: Permite criar uma nova parada de máquina.
- **Obter Parada de Máquina**: Permite obter detalhes de uma parada de máquina específica pelo ID.
- **Listar Paradas de Máquinas**: Permite listar paradas de uma determinada máquina dentro de um intervalo de tempo.
- **Atualizar Parada de Máquina**: Permite atualizar ou o tempo de término ou a razão da parada de uma máquina.
- **Excluir Todas as Paradas**: Permite excluir todas as paradas de máquinas.

## Endpoints

### Criar uma nova parada de máquina
- **URL:** `/machine-halt`
- **Método:** `POST`
- **Corpo da Requisição:**
  ```json
  {
    "machine_tag": "string",  //identificador da máquina
    "start_time": "datetime"  //tempo de início da parada (formato ISO 8601)
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

### Finalizar uma parada de máquina
- **URL:** `/machine-halt`
- **Método:** `PUT`
- **Corpo da Requisição:**
  ```json
  {
    "id": "int",          // identificador da parada
    "end_time": "datetime",  // (tempo de finalização da parada (formato ISO 8601))
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
### Alterar o motivo para da parada
- **URL:** `/machine-halt`
- **Método:** `PUT`
- **Corpo da Requisição:**
  ```json
  {
    "id": "int",          // identificador da parada
    "reason": "string"    // motivo da parada
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

### Deletar todas as paradas de máquinas
- **URL:** `/machine-halt/all`
- **Método:** `DELETE`
- **Resposta de Sucesso:**
  - **Código:** `204 No Content`

## Como Executar

### Pré-requisitos

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Marshmallow

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/lucaselvieira/machineHaltService.git
   cd machineHaltService
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
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
 
## Contato

Lucas E Lopes Vieira - [Email](mailto:lucaselvieira@gmail.com)

Link do Projeto: [https://github.com/lucaselvieira/machineHaltService.git](https://github.com/lucaselvieira/machineHaltService.git)
