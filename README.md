# Automação de Download - Dados Abertos Curitiba

## 📋 Descrição

Ferramenta de automação web desenvolvida para realizar o download completo de todos os arquivos CSV disponíveis no portal de Dados Abertos da Prefeitura de Curitiba. O projeto utiliza Playwright para navegação automatizada e extração inteligente de conjuntos de dados.

## 🎯 O que a automação faz

Esta automação acessa o portal de dados abertos, identifica todos os conjuntos de dados disponíveis (incluindo páginas paginadas), navega pelos detalhes de cada dataset e realiza o download sistemático de todos os arquivos CSV, organizando-os com nomenclatura apropriada baseada em seus metadados.

## 📦 Pré-requisitos

- Python 3.8+
- Playwright
- Requests (opcional, para downloads otimizados)

## 🚀 Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd curitiba-dados-abertos

# Instale as dependências
pip install -r requirements.txt

# Instale os navegadores do Playwright
playwright install chromium
```

## 💻 Como usar

```bash
# Execute a automação
python main.py

# Os arquivos CSV serão salvos no diretório ./downloads/
```

## 📁 Estrutura do Projeto

```
├── main.py                 # Script principal da automação
├── requirements.txt        # Dependências do projeto
├── downloads/             # Diretório de saída dos CSVs
└── README.md
```

## ⚙️ Como funciona

1. **Inicialização**: Acessa a página principal e aguarda carregamento completo
2. **Descoberta**: Identifica todos os cards/links de conjuntos de dados
3. **Navegação**: Itera por páginas paginadas (se houver)
4. **Extração**: Para cada dataset, acessa a página de detalhes e localiza URLs dos CSVs
5. **Download**: Realiza download programático com nomenclatura inteligente
6. **Organização**: Salva arquivos com nomes baseados em metadados do portal

## ⚠️ Notas e Limitações

- **Paginação dinâmica**: O site pode usar scroll infinito ou botões de navegação
- **Rate limiting**: Implementado delay entre requisições para evitar bloqueios
- **Tokens CSRF**: Sistema detecta e gerencia tokens de verificação quando necessário
- **Nomenclatura**: Arquivos podem ter nomes genéricos; a automação os renomeia automaticamente
- **Self-healing**: Sistema com 1 tentativa de recuperação automática em caso de falhas

## 📊 Status

✅ Testado e funcional  
🔄 Self-healing implementado  
⚡ Complexidade: Média

---

**Desenvolvido para facilitar o acesso programático aos dados públicos de Curitiba**