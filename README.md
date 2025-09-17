# API Flask Netflix

Esta aplicação é uma API RESTful desenvolvida com Flask para consultar, cadastrar, atualizar e remover filmes e usuários do catálogo da Netflix. Possui autenticação JWT, documentação interativa via Swagger (Flasgger) e suporte a filtros dinâmicos via query string.

## Funcionalidades

- **Filmes**
  - Listagem de todos os filmes, com filtros por tipo, país, ano, classificação e gênero.
  - Consulta de filme por ID.
  - Cadastro, atualização e remoção de filmes (requer autenticação).

- **Usuários**
  - Cadastro de usuário com confirmação por e-mail.
  - Login e logout com JWT.
  - Atualização e remoção de usuários.
  - Blacklist de tokens JWT.

- **Documentação**
  - Swagger disponível em `/apidocs`.

## Estrutura

```
api-flask-netflix/
├── app.py                # Arquivo principal da aplicação Flask
├── blacklist.py          # Gerenciamento de blacklist de tokens JWT
├── conf/                 # Configurações (JSON)
├── database/             # Arquivos de banco, filtros e migrações
├── instance/             # Banco SQLite
├── models/               # Modelos ORM (Movie, User)
├── resources/            # Endpoints RESTful
├── templates/            # Templates HTML para confirmação de usuário
├── sql_alchemy.py        # Inicialização do SQLAlchemy
├── README.md             # Este arquivo
```

## Instalação

1. **Clone o repositório**
   ```sh
   git clone https://github.com/seu-usuario/api-flask-netflix.git
   cd api-flask-netflix
   ```

2. **Crie e ative um ambiente virtual**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```sh
   pip install -r requiriments.txt
   ```

4. **Configure os arquivos**
   - Edite `conf/config.json` com suas configurações de banco e chaves secretas.
   - Edite `conf/flasgger.json` se desejar customizar a documentação Swagger.

5. **Execute a aplicação**
   ```sh
   python app.py
   ```

## Uso

- **Swagger:** Acesse [http://localhost:5000/apidocs](http://localhost:5000/apidocs) para visualizar e testar os endpoints.
- **Exemplo de filtro:**  
  ```
  GET /movies?type=Movie&country=Brazil&release_year=2020
  ```

## Testes de Requests

- Exemplos de requisições para todos os endpoints estão disponíveis no arquivo `requests.har`, podendo ser importados diretamente no Postman, Insomnia ou outra ferramenta compatível.

## Banco de Dados

- Utiliza SQLite (`instance/movie.db`).
- Scripts de migração disponíveis em `database/migration.sql`.

## Autenticação

- JWT via `flask_jwt_extended`.
- Blacklist de tokens em `blacklist.py`.

## Licença

Este projeto está sob a licença MIT.

---

**Dúvidas ou sugestões?**  
Abra uma issue ou envie um pull request!