# Projeto: Agente de Monitoramento Web (DevOps Challenge)

Este projeto foi desenvolvido como parte de um desafio prático para a vaga de Analista de Operações Pleno - foco em DevOps. Ele consiste em um agente de monitoramento que verifica a latência, disponibilidade e tempo de resposta de sites públicos, armazenando os dados em um banco PostgreSQL e exibindo os resultados em um dashboard Grafana.

:hammer: Tecnologias Utilizadas

- Docker
- Docker Compose
- Python 3.10 (slim)
- PostgreSQL 15
- Grafana
- iputils-ping
- Bibliotecas Python: requests, psycopg2-binary

:gear: Estrutura do Projeto

```## Sumário
agent-web/
├── Dockerfile
├── main.py
├── README.md
docker-compose.yml
init.sql
grafana_dashboard_web_monitor.json
```

:page_with_curl: Descrição do Funcionamento

O script main.py executa um loop a cada 60 segundos:

  - Realiza ping para www.google.com, www.youtube.com e www.rnp.br
  - Mede a latência (RTT) e perda de pacotes
  - Executa requisições HTTP (GET) e armazena o código de status e tempo de resposta
  - Os dados coletados são inseridos na tabela metrics do PostgreSQL
  - O Grafana exibe essas métricas em tempo real

:package: Instruções para Execução

1. Clonar o repositório
   ```sh
   git clone <seu-repositorio>
   cd agent-web
   ```
2. Subir os containers
   ```sh
   docker-compose down --volumes --remove-orphans
   docker-compose build --no-cache
   docker-compose up -d
   ```
3. Verificar logs do agente
   ```sh
   docker logs -f agent-web
   ```
4. Validar dados no banco
   ```sh
   docker exec -it pgtest psql -U user -d monitoramento -c "SELECT * FROM metrics ORDER BY id DESC LIMIT 10;"
   ```
5. Acessar Grafana
    URL: http://localhost:3000
    Usuário: admin
    Senha: admin

:bookmark_tabs: init.sql (criação da tabela)
   ```sh
    CREATE TABLE IF NOT EXISTS metrics (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        host VARCHAR(100),
        rtt_ms FLOAT,
        loss_pct FLOAT,
        http_status INT,
        http_time_ms FLOAT
    );
   ```

:bar_chart: Dashboard no Grafana

1. Acesse http://localhost:3000
2. Configure o DataSource:
  - Tipo: PostgreSQL
  - Host: pgtest:5432  
  - Database: monitoramento
  - User: user / Password: pass
3. Crie um dashboard com:
  - Gráfico de latência (RTT)
  - Status HTTP por host
  - Tempo de resposta HTTP
  - Perda de pacotes

:triangular_ruler: High Level Design (HLD)

Componentes
  - agent-web: container com script Python que coleta dados e insere no PostgreSQL
  - pgtest: container PostgreSQL com volume persistente e script de inicialização
  - grafana: visualiza os dados com dashboards personalizados

Fluxo
```## Sumário
[agent-web] ➞ coleta dados de rede e HTTP
         ➞ insere em [PostgreSQL]
                 ➞ Grafana consome via datasource
```

