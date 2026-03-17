"""
Auto Web Automator v3 — Vision-Powered
URL: https://dadosabertos.curitiba.pr.gov.br/
Tarefa: preciso baixar todos os csv's desse site
"""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

downloads_dir = r"C:\Users\israb\Documents\Agente_RPA\automation_project\downloads"
Path(downloads_dir).mkdir(parents=True, exist_ok=True)

def main():
    total_downloads = 0
    datasets_processados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(60000)

        print("Passo 1: Acessando URL alvo...")
        page.goto("https://dadosabertos.curitiba.pr.gov.br/", wait_until='networkidle')
        time.sleep(3)

        print("Passo 2: Fechando modal de boas-vindas...")
        try:
            modal_selectors = [
                "button:has-text('Pular tutorial')",
                "button.close",
                ".modal button[aria-label='Close']",
                "button:has-text('×')",
                ".btn:has-text('Pular')",
                ".introjs-skipbutton"
            ]
            for selector in modal_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click(timeout=5000)
                        print(f"Modal fechado com seletor: {selector}")
                        time.sleep(2)
                        break
                except:
                    continue
        except Exception as e:
            print(f"Nenhum modal encontrado ou erro ao fechar: {e}")

        print("Passo 3: Navegando para 'Conjuntos de Dados'...")
        try:
            page.get_by_role("link", name="Conjuntos de Dados").click(timeout=10000)
            print("Menu clicado com get_by_role")
        except:
            try:
                page.locator("a[href*='conjuntos']").first.click(timeout=10000)
                print("Menu clicado com locator href")
            except:
                print("Navegando diretamente para página de conjuntos...")
                page.goto("https://dadosabertos.curitiba.pr.gov.br/conjuntodado", wait_until='networkidle')

        page.wait_for_load_state('networkidle')
        time.sleep(3)

        print("Passo 4: Coletando links dos datasets...")
        page_number = 1

        while True:
            print(f"\n--- Processando página {page_number} ---")
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Coletar todos os links de datasets na página atual
            dataset_links = page.locator("a[href*='conjuntodado/detalhe?chave=']").all()
            print(f"Encontrados {len(dataset_links)} datasets nesta página")

            if len(dataset_links) == 0:
                print("Nenhum dataset encontrado, finalizando...")
                break

            # Processar cada dataset
            for idx in range(len(dataset_links)):
                try:
                    # Re-localizar elementos para evitar stale references
                    dataset_links = page.locator("a[href*='conjuntodado/detalhe?chave=']").all()
                    if idx >= len(dataset_links):
                        break

                    dataset_link = dataset_links[idx]
                    dataset_url = dataset_link.get_attribute('href')

                    if dataset_url in datasets_processados:
                        print(f"Dataset {idx+1} já processado, pulando...")
                        continue

                    print(f"\nProcessando dataset {idx+1}/{len(dataset_links)}: {dataset_url}")

                    # Abrir página do dataset
                    dataset_link.click()
                    page.wait_for_load_state('networkidle')
                    time.sleep(2)

                    # Procurar botões de download CSV
                    csv_selectors = [
                        "a[href$='.csv']",
                        "a[download][href*='.csv']",
                        "a:has-text('CSV')",
                        "button:has-text('CSV')",
                        "a:has-text('Baixar')",
                        ".download-link"
                    ]

                    download_realizado = False
                    for selector in csv_selectors:
                        try:
                            if page.locator(selector).count() > 0:
                                print(f"Tentando download com seletor: {selector}")
                                with page.expect_download(timeout=30000) as download_info:
                                    page.locator(selector).first.click()

                                download = download_info.value
                                filepath = os.path.join(downloads_dir, download.suggested_filename)
                                download.save_as(filepath)
                                print(f"✓ Download salvo: {download.suggested_filename}")
                                total_downloads += 1
                                download_realizado = True
                                time.sleep(1)
                                break
                        except Exception as e:
                            print(f"Erro com seletor {selector}: {e}")
                            continue

                    if not download_realizado:
                        print("⚠ Nenhum CSV encontrado para download neste dataset")

                    datasets_processados.append(dataset_url)

                    # Voltar para listagem
                    page.go_back(wait_until='networkidle')
                    time.sleep(2)

                except Exception as e:
                    print(f"Erro ao processar dataset {idx+1}: {e}")
                    try:
                        page.go_back(wait_until='networkidle')
                        time.sleep(2)
                    except:
                        page.goto("https://dadosabertos.curitiba.pr.gov.br/conjuntodado", wait_until='networkidle')
                        time.sleep(2)
                    continue

            # Verificar se existe próxima página
            print("\nVerificando próxima página...")
            try:
                next_button = None
                pagination_selectors = [
                    ".pagination a:has-text('Próxima')",
                    ".pagination a[rel='next']",
                    "button:has-text('Próxima')",
                    "a:has-text('›')",
                    ".next-page"
                ]

                for selector in pagination_selectors:
                    if page.locator(selector).count() > 0:
                        next_button = page.locator(selector).first
                        break

                if next_button and next_button.is_visible():
                    print(f"Navegando para página {page_number + 1}...")
                    next_button.click()
                    page.wait_for_load_state('networkidle')
                    time.sleep(3)
                    page_number += 1
                else:
                    print("Não há mais páginas, finalizando...")
                    break
            except Exception as e:
                print(f"Erro ao buscar próxima página: {e}")
                break

        print(f"\n{'='*50}")
        print(f"RESUMO DA AUTOMAÇÃO:")
        print(f"Total de downloads realizados: {total_downloads}")
        print(f"Total de datasets processados: {len(datasets_processados)}")
        print(f"Pasta de destino: {downloads_dir}")
        print(f"{'='*50}")

        browser.close()
        print("\nAUTOMACAO_CONCLUIDA")

if __name__ == "__main__":
    main()