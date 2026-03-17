"""
Automacao gerada por Auto Web Automator v1
URL: https://dadosabertos.curitiba.pr.gov.br/
Tarefa: quero baixar todos os csv's do site
Biblioteca: playwright
"""

from playwright.sync_api import sync_playwright
import time
import os
import re

def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.strip()
    return name[:200] if len(name) > 200 else name

def download_all_csvs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            accept_downloads=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        download_dir = "downloads_csvs"
        os.makedirs(download_dir, exist_ok=True)

        try:
            print("Acessando página principal...")
            page.goto("https://dadosabertos.curitiba.pr.gov.br/", timeout=60000)
            page.wait_for_load_state("networkidle")
            time.sleep(3)

            print("Navegando para página de conjuntos de dados...")
            page.goto("https://dadosabertos.curitiba.pr.gov.br/conjuntodado", timeout=60000)
            page.wait_for_load_state("networkidle")
            time.sleep(3)

            dataset_links = []
            page_num = 1

            print("Coletando links de todos os datasets...")
            while True:
                print(f"Processando página {page_num}...")

                try:
                    page.wait_for_selector("div.card, div.dataset-item, a[href*='/conjuntodado/'], a", timeout=30000, state="visible")
                    time.sleep(2)
                except:
                    print("Timeout esperando seletores, tentando continuar...")

                links = page.query_selector_all("a")

                found_links = []
                for link in links:
                    href = link.get_attribute("href")
                    if href and '/conjuntodado/detalhe/' in href:
                        found_links.append(link)

                print(f"Encontrados {len(found_links)} links na página {page_num}")

                for link in found_links:
                    href = link.get_attribute("href")
                    if href and href not in dataset_links:
                        full_url = f"https://dadosabertos.curitiba.pr.gov.br{href}" if href.startswith("/") else href
                        dataset_links.append(full_url)

                next_button = page.query_selector("a[aria-label='Next']:not(.disabled)")
                if not next_button:
                    next_button = page.query_selector("a.page-link:has-text('›'):not(.disabled)")
                if not next_button:
                    next_button = page.query_selector("li.page-item:not(.disabled) a:has-text('Próxima')")
                if not next_button:
                    next_button = page.query_selector("a:has-text('Próxima'):not(.disabled)")

                if next_button:
                    try:
                        next_button.click()
                        page.wait_for_load_state("networkidle")
                        time.sleep(3)
                        page_num += 1
                    except:
                        print("Não há mais páginas ou erro ao navegar")
                        break
                else:
                    print("Não encontrado botão de próxima página")
                    break

            print(f"\nTotal de datasets encontrados: {len(dataset_links)}")

            csv_downloads = []

            for idx, dataset_url in enumerate(dataset_links, 1):
                print(f"\n[{idx}/{len(dataset_links)}] Acessando dataset: {dataset_url}")

                try:
                    page.goto(dataset_url, timeout=60000)
                    page.wait_for_load_state("networkidle")
                    time.sleep(2)

                    dataset_title = "dataset"
                    try:
                        title_element = page.query_selector("h1")
                        if not title_element:
                            title_element = page.query_selector("h2")
                        if not title_element:
                            title_element = page.query_selector(".titulo, .dataset-title, .page-title")
                        if title_element:
                            dataset_title = sanitize_filename(title_element.inner_text().strip())
                    except:
                        pass

                    print(f"Dataset: {dataset_title}")

                    all_links = page.query_selector_all("a")
                    csv_links = []

                    for link in all_links:
                        href = link.get_attribute("href")
                        text = link.inner_text().strip().lower()

                        if href and ('.csv' in href.lower() or 'csv' in text or 'download' in text):
                            csv_links.append(link)

                    print(f"Encontrados {len(csv_links)} possíveis links de CSV")

                    for link_idx, csv_link in enumerate(csv_links):
                        try:
                            href = csv_link.get_attribute("href")
                            text = csv_link.inner_text().strip()

                            if not href:
                                continue

                            full_csv_url = f"https://dadosabertos.curitiba.pr.gov.br{href}" if href.startswith("/") else href

                            print(f"  Baixando CSV {link_idx + 1}: {text[:50]}...")

                            try:
                                with page.expect_download(timeout=120000) as download_info:
                                    csv_link.click()

                                download = download_info.value

                                original_filename = download.suggested_filename
                                new_filename = f"{dataset_title}_{link_idx + 1}_{original_filename}" if original_filename.endswith('.csv') else f"{dataset_title}_{link_idx + 1}.csv"
                                filepath = os.path.join(download_dir, new_filename)

                                download.save_as(filepath)
                                print(f"  ✓ Salvo: {filepath}")
                                csv_downloads.append(filepath)
                            except:
                                print(f"  → Tentando download direto da URL: {full_csv_url}")
                                response = page.request.get(full_csv_url)
                                if response.ok:
                                    filepath = os.path.join(download_dir, f"{dataset_title}_{link_idx + 1}.csv")
                                    with open(filepath, 'wb') as f:
                                        f.write(response.body())
                                    print(f"  ✓ Salvo: {filepath}")
                                    csv_downloads.append(filepath)

                            time.sleep(2)

                        except Exception as e:
                            print(f"  ✗ Erro ao baixar CSV: {str(e)}")
                            continue

                    if len(csv_links) == 0:
                        print("  Nenhum CSV encontrado neste dataset")

                except Exception as e:
                    print(f"Erro ao processar dataset: {str(e)}")
                    continue

                time.sleep(2)

            print(f"\n{'='*60}")
            print(f"Total de CSVs baixados: {len(csv_downloads)}")
            print(f"Salvos em: {os.path.abspath(download_dir)}")
            print(f"{'='*60}")

            for csv_file in csv_downloads:
                print(f"  - {csv_file}")

            print("\nAUTOMACAO_CONCLUIDA")

        except Exception as e:
            print(f"\nErro durante execução: {str(e)}")
            import traceback
            traceback.print_exc()

        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    download_all_csvs()