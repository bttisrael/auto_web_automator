# 🤖 Curitiba Open Data Downloader

Automação web para download em massa de todos os arquivos CSV disponíveis no Portal de Dados Abertos de Curitiba.

## 📋 Descrição

Este projeto automatiza o processo de navegação e download de datasets no portal [dadosabertos.curitiba.pr.gov.br](https://dadosabertos.curitiba.pr.gov.br/), coletando sistematicamente todos os arquivos CSV disponíveis. Utilizando Playwright com capacidades de visão computacional, o sistema navega autonomamente pelo portal, identifica conjuntos de dados e realiza downloads de forma estruturada.

## ✅ Pré-requisitos

- Python 3.8 ou superior
- Playwright
- Conexão estável com a internet
- Aproximadamente 2GB de espaço em disco (varia conforme datasets disponíveis)

## 🔧 Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd curitiba-opendata-downloader

# Instale as dependências
pip install playwright
playwright install chromium

# Execute o script
python main.py
```

## 🚀 Como Usar

Execute o script principal:

```bash
python main.py
```

O sistema irá:
1. Acessar o portal automaticamente
2. Navegar por todas as páginas de datasets
3. Baixar cada arquivo CSV encontrado
4. Salvar os arquivos na pasta `./downloads/`
5. Gerar um log de operações em `download_log.txt`

## 📊 Resultado Esperado

- **Pasta downloads/**: Todos os arquivos CSV organizados
- **download_log.txt**: Registro detalhado com:
  - Total de datasets processados
  - Arquivos baixados com sucesso
  - Erros ou falhas encontradas
  - Timestamp de cada operação

## ⚙️ Como Funciona

O sistema utiliza uma abordagem híbrida de automação:

1. **Navegação Inteligente**: Fecha modais automaticamente e navega pela estrutura do portal
2. **Extração de Dados**: Identifica links de datasets através de padrões específicos (`/conjuntodado/detalhe?chave=`)
3. **Paginação Automática**: Calcula e percorre todas as páginas de resultados
4. **Visão Computacional**: Implementa **self-healing** visual com 2 correções automáticas para lidar com mudanças na interface, garantindo robustez mesmo com alterações no layout
5. **Download Gerenciado**: Identifica e baixa todos os CSV de cada dataset

## ⚠️ Limitações

- **Taxa de sucesso atual**: Em desenvolvimento (últimos testes não finalizaram completamente)
- **Dependência de estrutura**: Mudanças significativas no portal podem requerer ajustes
- **Tempo de execução**: Pode levar várias horas dependendo do volume de dados
- **Rate limiting**: Não implementado - pode ser bloqueado por requisições excessivas
- **Validação de arquivos**: Não verifica integridade dos CSV baixados
- **Formatos alternativos**: Baixa apenas CSV, ignorando XLS, JSON ou outros formatos

## 📝 Licença

MIT License - Sinta-se livre para usar e modificar.

---

**Nota**: Este é um projeto educacional. Respeite os termos de uso do portal e utilize com responsabilidade.