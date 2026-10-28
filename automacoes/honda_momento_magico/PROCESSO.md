# Mapeamento do Processo: Automação Acadêmica - Honda

## Visão Geral
Este documento detalha o fluxo passo a passo executado na plataforma da Academia de Vendas Honda para o cadastro em lote de chassis no curso **Momento Mágico**, reprodução do conteúdo, resposta automatizada da avaliação e tratamento de registros duplicados.

---

## Etapas do Fluxo

1. **Autenticação (Login)**
   - O usuário acessa o portal e insere as credenciais de acesso.

2. **Navegação até o Catálogo**
   - Na barra lateral (sidebar), clica em **Conteúdo** e depois em **Catálogo**.
   - Localiza o curso **Momento Mágico** e clica no botão **Saiba mais**.

3. **Matrícula em Lote via Chassis**
   - Clica no botão **Matricule-se**.
   - Seleciona a opção **Preencher sem usar QR Code**.
   - Insere iterativamente cada chassi contido na lista de dados de entrada.
   - Clica em **Salvar**.

4. **Tratamento de Exceções e Retornos**
   - **Caso de Duplicidade:** Se o sistema exibir o alerta `Erro ao salvar ficha: Número de chassis já cadastrado no curso`, o robô captura o erro, registra no log e passa para o próximo chassi da lista.
   - **Caso de Sucesso/Pendente:** Exibe a mensagem de confirmação de ficha realizada e prossegue para a sala de aula.

5. **Execução do Conteúdo (Aula)**
   - Clica em **Acessar curso**.
   - Seleciona o item **Momento Mágico** no sumário.
   - Aciona o **Play** no player de vídeo e aguarda o término da contagem/reprodução.
   - Clica no botão **Próximo**.

6. **Avaliação Automatizada**
   - No modal de confirmação de tentativa única, clica em **Sim**.
   - **Questão 1:** Seleciona automaticamente a alternativa **a) SIM**.
   - **Questão 2:** Seleciona automaticamente a alternativa **a) SIM** (opção 1/A correspondente).
   - Clica em **Finalizar Avaliação**.
   - Confirma o encerramento clicando em **Sim** no modal.
   - Fecha a notificação final de aproveitamento necessário clicando em **OK**.