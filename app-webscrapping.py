import os
import re
import requests
from bs4 import BeautifulSoup

# Configurações
BASE_URL = "https://repositorio.ufsc.br/handle/123456789/41812/recent-submissions?offset={}"
BASE_REPO_URL = "https://repositorio.ufsc.br"
OUTPUT_DIR = "tccs_ufsc"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Extensões permitidas
ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*%]', '_', filename)  
    filename = re.sub(r'[^\x00-\x7F]+', '_', filename)  
    filename = re.sub(r'\s+', '_', filename)  
    filename = filename.strip()
    return filename[:100] 

def get_tcc_links(offset):
    url = BASE_URL.format(offset)
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao acessar a página: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tcc_links = []

    for link in soup.select(".artifact-title a"):
        href = link.get("href")
        if href:
            tcc_links.append(BASE_REPO_URL + href)

    return tcc_links

def download_tcc(tcc_url):
    try:
        response = requests.get(tcc_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao acessar o TCC: {tcc_url} - {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    file_links = []
    for link in soup.select("a"):
        link_text = link.text.strip().lower()
        if any(link_text.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            file_links.append(link)

    if file_links:
        file_url = BASE_REPO_URL + file_links[0]["href"]
        file_name = file_url.split("/")[-1].split("?")[0]  
        file_name = sanitize_filename(file_name)  
        file_path = os.path.join(OUTPUT_DIR, file_name)

        try:
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            with open(file_path, "wb") as file:
                file.write(file_response.content)
            print(f"📥 Baixado: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro ao baixar o arquivo: {file_url} - {e}")
        except OSError as e:
            print(f"⚠️ Erro ao salvar o arquivo {file_name}: {e}")
    else:
        print(f"❌ Arquivo não encontrado para {tcc_url}")

offset = 0
max_offset = 300  # Limite máximo de páginas para evitar loops infinitos

while offset <= max_offset:
    print(f"💢 Baixando TCCs da página offset={offset}...")
    tcc_links = get_tcc_links(offset)

    if not tcc_links:
        print("✅ Nenhum TCC encontrado. Encerrando...")
        break

    for tcc_link in tcc_links:
        download_tcc(tcc_link)

    offset += 20  # Avança para a próxima página

print("✅ Download concluído!")