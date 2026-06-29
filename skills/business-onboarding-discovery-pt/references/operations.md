# Contratos Das Operações

Todas as operações recebem `tenant_id` e retornam JSON. Nenhuma operação
publica agentes automaticamente.

## Entrada Pelo Console

`business_console_discovery_start_pt` aceita `message`, `tenant_id`
opcional, `owner_name`, `company_name` e `initial_context`. Use quando a
conversa começar no chat do console antes do WhatsApp; a ferramenta
cria/carrega o tenant e devolve a próxima pergunta.

`business_frontend_discovery_start_pt` aceita os mesmos campos e é a
entrada preferida para a tela do plugin. A rota REST equivalente é
`POST /api/tenant-discovery/frontend-start`.

## Perfil

`business_profile_update_pt` recebe `profile_patch` como objeto ou string
JSON. O `tenant_id` do argumento é a fonte da verdade. Campos escalares
em conflito retornam `conflicts` e preservam o valor existente; para
substituir, envie o campo em `_replace`.

## Perguntas

`business_next_question_pt` registra `asked_count` por lacuna para evitar
repetição infinita. A resposta indica `unblocks_agents`,
`related_plugins`, `should_request_file` e `suggested_source_types`.

## Fontes

Registre fontes em `/knowledge-sources` ou `/knowledge-sources/upload`.
Depois chame `business_knowledge_ingest_pt` com `source_id`. Site e
Instagram não fazem scraping; use conteúdo colado.

## Readiness

Critérios críticos bloqueiam o agente. Score suficiente sem falha crítica
deixa o agente pronto para revisão humana, não para publicação automática.

## Compliance

Clínica, advocacia, imobiliária e contabilidade são nichos regulados.
Agentes voltados ao cliente continuam bloqueados sem credencial
profissional e consentimento LGPD.
