# Projeto: Agente de Monitoramento Web (DevOps Challenge)

Este projeto foi desenvolvido como parte de um desafio prático para a vaga de Analista de Operações Pleno - foco em DevOps. Ele consiste em um agente de monitoramento que verifica a latência, disponibilidade e tempo de resposta de sites públicos, armazenando os dados em um banco PostgreSQL e exibindo os resultados em um dashboard Grafana.

## Tecnologias Utilizadas

- Docker
- Docker Compose
- Python 3.10 (slim)
- PostgreSQL 15
- Grafana
- iputils-ping
 Bibliotecas Python: requests, psycopg2-binary

## Estrutura do Projeto

agent-web/
├── Dockerfile
├── main.py
├── venv/ (local)
docker-compose.yml
init.sql

:page_with_curl: Descrição do Funcionamento

O script main.py executa um loop a cada 60 segundos:
    Realiza ping para www.google.com, www.youtube.com e www.rnp.br
    Mede a latência (RTT) e perda de pacotes
    Executa requisições HTTP (GET) e armazena o código de status e tempo de resposta
    Os dados coletados são inseridos na tabela metrics do PostgreSQL
    O Grafana exibe essas métricas em tempo real

:package: Instruções para Execução

1. Clonar o repositório
    git clone <seu-repositorio>
    cd agent-web

2. Subir os containers
    docker-compose down --volumes --remove-orphans
    docker-compose build --no-cache
    docker-compose up -d

3. Verificar logs do agente
    docker logs -f agent-web

4. Validar dados no banco
    docker exec -it pgtest psql -U user -d monitoramento -c "SELECT * FROM metrics ORDER BY id DESC LIMIT 10;"

5. Acessar Grafana
    URL: http://localhost:3000
    Usuário: admin
    Senha: admin

    **É necessário configurar o PostgreSQL como datasource e montar o dashboard manualmente (instruções no final deste README).**

:bookmark_tabs: init.sql (criação da tabela)

    CREATE TABLE IF NOT EXISTS metrics (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        host VARCHAR(100),
        rtt_ms FLOAT,
        loss_pct FLOAT,
        http_status INT,
        http_time_ms FLOAT
    );

:bar_chart: Dashboard no Grafana

Acesse http://localhost:3000

Configure o DataSource:

    Tipo: PostgreSQL
    Host: pgtest:5432
    Database: monitoramento
    User: user / Password: pass

Crie um dashboard com:

    Gráfico de latência (RTT)
    Status HTTP por host
    Tempo de resposta HTTP
    Perda de pacotes

:triangular_ruler: High Level Design (HLD)

Componentes

    agent-web: container com script Python que coleta dados e insere no PostgreSQL
    pgtest: container PostgreSQL com volume persistente e script de inicialização
    grafana: visualiza os dados com dashboards personalizados

Fluxo
    [agent-web] ➞ coleta dados de rede e HTTP
            ➞ insere em [PostgreSQL]
                    ➞ Grafana consome via datasource