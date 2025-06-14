# 🎓 Webscrapping UFSC TCCs

Este é um script em Python criado para **automatizar o download de Trabalhos de Conclusão de Curso (TCCs)** do repositório institucional da UFSC.  
Ele percorre as páginas recentes do repositório, encontra os links válidos e realiza o download de arquivos com extensões `.pdf`, `.doc` e `.docx`.

## ⚙️ Funcionalidades

- Acessa automaticamente a listagem de TCCs recentes
- Filtra e identifica arquivos com extensões permitidas
- Baixa os arquivos e salva em uma pasta local
- Evita arquivos corrompidos ou com caracteres inválidos no nome

## 📦 Requisitos

- Python 3.6 ou superior

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## 🧪 Criando o ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv

# Ativando:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

## 📁 Estrutura de saída
É necessário organizar uma pasta com o nome "tccs_ufsc" para armazenar os dowloads. 


Exemplo: <br>
📁 tccs_ufsc/ <br>
├── trabalho1.pdf <br>
├── trabalho2.docx <br>
└── ...