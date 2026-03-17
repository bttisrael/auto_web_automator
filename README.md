# 🤖 Automação de Download - Dados Abertos Curitiba

Automação web desenvolvida com **Playwright** para download massivo de todos os arquivos CSV disponíveis no portal de Dados Abertos da Prefeitura de Curitiba.

## 📋 Descrição

Este script navega automaticamente pelo site [dadosabertos.curitiba.pr.gov.br](https://dadosabertos.curitiba.pr.gov.br/), identifica todos os conjuntos de dados disponíveis, acessa cada página de detalhe e realiza o download de todos os arquivos CSV encontrados.

## 🔧 Pré-requisitos

- Python 3.8 ou superior
- Playwright
- Conexão estável com a internet
- Espaço em disco para armazenamento dos arquivos CSV

## 📦 Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd <diretorio-do-projeto>

# Instale as dependências
pip install playwright

# Instale o navegador Chromium
playwright install chromium
```

## 🚀 Como Usar

```bash
python automation.py
```

Os arquivos CSV serão salvos automaticamente no diretório `downloads/` na raiz do projeto.

## ✅ Resultado Esperado

- **Navegação automática** por todas as páginas de conjuntos de dados
- **Download completo** de todos os arquivos CSV disponíveis
- **Logs detalhados** do progresso da execução
- **Organização** dos arquivos por dataset no diretório de downloads

## 📁 Estrutura do Projeto

```
.
├── automation.py          # Script principal
├── downloads/             # Diretório de arquivos baixados
├── README.md             # Documentação
└── requirements.txt      # Dependências Python
```

## ⚠️ Limitações Conhecidas

- **Rate Limiting**: O script implementa delays entre requisições para evitar sobrecarga no servidor
- **Paginação**: Múltiplas páginas são navegadas automaticamente
- **Datasets com múltiplos arquivos**: Cada conjunto pode conter vários CSVs (ex: 5 arquivos por dataset)
- **Termos de uso**: Verifique se há necessidade de aceitar termos antes do download
- **Self-healing**: Sistema com 1 correção automática aplicada para maior robustez

## 📊 Status

- ✅ Testes passando
- ✅ Self-healing ativo
- ⚠️ Downloads detectados: verificar volume total após execução completa

## 📄 Licença

Este projeto é fornecido como está, para fins educacionais e de automação pessoal. Respeite os termos de uso do portal de Dados Abertos de Curitiba.