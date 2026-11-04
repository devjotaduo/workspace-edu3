# Quadro de Metas — redesign (protótipo)

Abra `index.html` no navegador. Arquivo único, sem build, sem dependências (só a fonte Inter do Google Fonts).
Os dados são os de novembro/2026, regional BA, tirados da tela atual.

## O que mudou em relação à tela atual

| Problema na tela atual | Como o redesign resolve |
|---|---|
| Cada vendedor ocupa um bloco de 4 painéis com cerca de 30 números, e não dá para comparar vendedores | Uma **linha por vendedor** com as colunas que importam para a decisão: sugerida, meta ABA, meta JUA, homologada e desvio |
| O cálculo (loja → área → vendedor) aparece espalhado em tabelas | Ao clicar na linha, abre uma **cascata explicada**: Meta da loja × peso da área = Meta da área × participação do vendedor = Meta sugerida → sua decisão |
| Desvios graves passam despercebidos (Denilson −88,6%, Jaedson sem meta) | Selo de desvio colorido em cada linha e o painel **"O que precisa da sua atenção"**, com atalho até o vendedor |
| Não fica claro quanto da meta das lojas foi distribuído | KPIs no topo e barra **Homologado / Sugerido / Meta das lojas**, também separada por loja |
| O ajuste em lote não diz a quem se aplica | Botão com o alcance escrito ("Aplicar +10% a 3 selecionados" ou "a todos visíveis (4)") |
| Salvar sem saber o que mudou | Marca "não salvo" na linha e barra de salvar com o número de alterações, o impacto em R$ e a opção de descartar |
| Rótulos técnicos ("Peso Área/Loja", "Rateio") | Linguagem de negócio, mais a seção "Como a meta sugerida é calculada" |

Também tem: tema escuro, layout para celular em cartões, navegação por teclado, filtros por canal (com contagem), área e busca.

## Lógica preservada
- `meta da área na loja = meta da loja × (fat. área / fat. loja)`
- `meta sugerida = meta da área × (fat. vendedor / fat. área)`
- `homologada = meta ABA + meta JUA` (valores editáveis)

O "Salvar" grava só no `localStorage` do navegador. Na integração real, ele deve chamar a API.
