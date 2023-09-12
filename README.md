# bringel

## Como executar

Para executar em ambiente de desenvolvimento é possível utilizar o docker-compose

Para isso é necessário possuir o [docker](https://docs.docker.com/engine/install/) e [docker-compose](https://docs.docker.com/compose/install/) instalados e rodar o seguinte comando:

```docker-compose up ```

Para rodar em segundo plano inclua `-d` como argumento ao comando acima

O docker-compose irá subir todos os containers necessários para executar a aplicação.

## Docker

O arquivo Dockerfile foi criado de forma a aproveitar o máximo o cache das camadas docker, o que fara com que os builds fiquem mais rápidos

Primeiro são instaladas as dependências do sistema operacional, atualizado o pip e configurado um usuário não root como usuário da aplicação.

Essas camadas não precisam ser reconstruidas com frequência.

Depois é copiado o `requirements.txt` e são instalados as dependências python do projeto

Essas camadas só são executadas novamente caso o arquivo `requirements.txt` tenha sido alterado. Em todos os builds onde isso não acontecer o cache dessas camadas será utilizado.

Depois são copiados os arquivos de inicialização e o fonte do projeto, camadas que podem ser alteradas com mais frequência durante o ciclo de vida do projeto

Para finalizar são carregados os argumentos de build `APP_VERSION` e `APP_MODE` que serão carregados como variáveis de ambiente do container por padrão (é possível sobrescrever e fornecer um novo valor).

O script de inicialização utiliza a variável `APP_MODE` para inicializar o webserver ou o celery, dessa forma ambos utilizam o mesmo build de imagem, ganhando agilidade durante o build

## docker-compose

O docker-compose sobe dois containers com o build do Dockerfile local, um para a API e outro para o worker do Celery (a diferença entre eles é apenas a variavel de ambiente `APP_MODE`)

Também sobe o postgres como banco de dado e redis como broker para o celery

## Documentação da API

A API possui documentação nos seguintes formatos:

* Swagger em `/swagger/`
* OpenAPI em `/swagger/?format=openapi`
* Redoc em `/redoc/`


## GraphQL

Foi adicionado suporte a consultas GraphQL via [django-restql](https://yezyilomo.github.io/django-restql/)

## CI/CD

Foi implementado dois workflows do github actions. 

* `tests.yml` roda a cada push e tem objetivo de validar o linter e executar a suite de testes
* `build.yml` roda a cada nova tag e tem objetivo de fazer o build da imagem docker do projeto

Obs: Por ser um projeto de teste a imagem docker faz build, porem não está sendo enviado (push) para nenhum repositório.
Seria possível integrar o github actions com o dockerhub, Amazon ECR, Google Artifact Registry ou Azure Container Registry.
Também seria possível disparar o deploy dessa nova versão no ambiente de testes e/ou produtivo.
