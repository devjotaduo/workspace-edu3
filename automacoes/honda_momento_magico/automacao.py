import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Lista de chassis de exemplo a serem processados em lote
LISTA_CHASSIS = [
    "9C2JB0100VR215130",
    # Adicione os próximos chassis aqui
]

URL_HOME = "https://academiadevendashonda.konviva.com.br/lms/#/home"

# Tempo de espera do vídeo em segundos (ajustar conforme duração real, ex: 5 minutos)
TEMPO_VIDEO_S = 305

# Status possíveis de cada chassi
APROVADO = "APROVADO"
REPROVADO = "REPROVADO"
DUPLICADO = "DUPLICADO"
NAO_CONFIRMADO = "NAO_CONFIRMADO"
ERRO = "ERRO"

# Palavras usadas para interpretar a mensagem final da avaliação
TERMOS_REPROVADO = [
    "reprovado", "não atingiu", "nao atingiu", "insuficiente",
    "não foi aprovado", "nao foi aprovado", "não aprovado", "nao aprovado",
]
TERMOS_APROVADO = ["aprovado", "parabéns", "parabens", "concluído", "concluido"]


def classificar_resultado(texto):
    """Interpreta o texto da mensagem final. Reprovação é checada primeiro
    porque 'reprovado' e 'não foi aprovado' também contêm 'aprovado'."""
    texto = texto.lower()
    if any(t in texto for t in TERMOS_REPROVADO):
        return REPROVADO
    if any(t in texto for t in TERMOS_APROVADO):
        return APROVADO
    return NAO_CONFIRMADO


def processar_chassi(page, chassi):
    """Executa o fluxo completo de um chassi. Retorna (status, detalhe)."""
    # 2. Navegação até o Catálogo
    page.click("text=Conteúdo")
    page.click("text=Catálogo")

    # 3. Seleção do curso Momento Mágico
    page.fill("input[placeholder*='O que deseja buscar']", "Momento Mágico")
    page.press("input[placeholder*='O que deseja buscar']", "Enter")
    page.click("text=Momento Mágico")
    page.click("text=Saiba mais")

    # 4. Matrícula sem QR Code
    page.click("text=Matricule-se")
    page.click("text=Preencher sem usar QR Code")

    # 5. Inserção do Chassi
    page.fill("input[placeholder*='Insira o número do chassi']", chassi)
    page.click("button:has-text('Salvar')")

    # 6. Tratamento de Retornos (Duplicado vs Sucesso)
    # wait_for de fato espera o alerta aparecer (is_visible responde na hora)
    try:
        page.locator("text=Número de chassis já cadastrado no curso").wait_for(
            state="visible", timeout=3000
        )
        page.click("button:has-text('Cancelar')")
        return DUPLICADO, "Número de chassis já cadastrado no curso"
    except PlaywrightTimeoutError:
        pass

    # Se avançou com sucesso para o curso
    try:
        page.click("text=Acessar curso", timeout=5000)
    except PlaywrightTimeoutError:
        print("[INFO] Já redirecionado para a sala de aula.")

    # 7. Execução da Aula
    page.click("text=Momento Mágico")
    # Aciona o player de vídeo
    page.locator("video").evaluate("node => node.play()")
    print("[INFO] Aguardando o término do vídeo...")
    time.sleep(TEMPO_VIDEO_S)

    page.click("text=Próximo")

    # 8. Avaliação
    page.click("button:has-text('Sim')")  # Confirma tentativa única

    # Questões 1 e 2 - Seleciona 'SIM' (Opção A)
    alternativas_sim = page.locator("input[value='S']")  # Ajustar seletor conforme o DOM real do rádio button
    alternativas_sim.nth(0).click()
    alternativas_sim.nth(1).click()

    page.click("text=Finalizar Avaliação")
    page.click("button:has-text('Sim')")  # Confirma finalização

    # Lê a mensagem final antes de fechar o modal, para saber o resultado real
    botao_ok = page.locator("button:has-text('OK')")
    try:
        botao_ok.wait_for(state="visible", timeout=10000)
    except PlaywrightTimeoutError:
        return NAO_CONFIRMADO, "Mensagem final da avaliação não apareceu"

    modal = page.locator("[role='dialog'], .modal, .swal2-popup").filter(has=botao_ok).last
    try:
        mensagem = modal.inner_text(timeout=2000).strip().removesuffix("OK").strip()
    except PlaywrightTimeoutError:
        mensagem = ""
    botao_ok.click()

    if not mensagem:
        return NAO_CONFIRMADO, "Não foi possível ler a mensagem final"
    return classificar_resultado(mensagem), " ".join(mensagem.split())


def imprimir_resumo(resultados):
    print("\n========== RESUMO ==========")
    for chassi, status, detalhe in resultados:
        print(f"{chassi}  {status:<15} {detalhe}")
    contagem = {}
    for _, status, _ in resultados:
        contagem[status] = contagem.get(status, 0) + 1
    print("----------------------------")
    print("  ".join(f"{s}: {n}" for s, n in contagem.items()))


def executar_automacao():
    resultados = []
    with sync_playwright() as p:
        # Inicializa o navegador (headless=False permite acompanhar visualmente a execução)
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Acesso à página de login
            page.goto(URL_HOME)
            print("[INFO] Faça o login manualmente na janela do navegador se necessário...")

            # Pausa para login manual ou automação de credenciais
            page.wait_for_url("**/lms/#/portal", timeout=60000)
            print("[INFO] Login realizado com sucesso.")

            for chassi in LISTA_CHASSIS:
                print(f"[PROCESSANDO] Iniciando chassi: {chassi}")
                # Cada chassi tem seu próprio tratamento de erro:
                # uma falha não interrompe os demais
                try:
                    status, detalhe = processar_chassi(page, chassi)
                except Exception as e:
                    status, detalhe = ERRO, str(e).splitlines()[0]
                    # Volta para a home para o próximo chassi começar de um estado limpo.
                    # O reload é necessário: goto para outra âncora (#/home) não recarrega a página
                    try:
                        page.goto(URL_HOME)
                        page.reload()
                    except Exception:
                        pass

                print(f"[{status}] Chassi {chassi}: {detalhe}")
                resultados.append((chassi, status, detalhe))

        except Exception as e:
            print(f"[ERRO CRÍTICO] Ocorreu um erro durante a execução: {e}")
        finally:
            imprimir_resumo(resultados)
            browser.close()

    return resultados


if __name__ == "__main__":
    executar_automacao()
