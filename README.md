# Sistema de Índice Hash

Este projeto implementa um sistema de índice hash para busca eficiente de palavras em um dicionário, com interface web desenvolvida em Streamlit.

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pipenv install
```

### 2. Executar a Aplicação Streamlit
```bash
pipenv run streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`.

## 🔧 Funcionalidades

### Configurações
- **Tamanho da Página**: Define quantas tuplas cabem em cada página
- **Tamanho do Bucket**: Define quantos elementos cabem em cada bucket do índice hash
- **Tamanho da Chave Hash**: Define o espaço de hash (parâmetro n)
- **Tipo de Hash**: Escolha entre hash customizado ou nativo do Python

### Busca
- **Busca com Índice Hash**: Utiliza a estrutura de hash para busca rápida
- **Busca Sequencial**: Busca linear através de todas as páginas
- **Comparação de Performance**: Mostra o tempo de execução de cada método

## 📊 Interface

A interface permite:
1. Configurar os parâmetros do sistema na barra lateral
2. Carregar os dados do dicionário
3. Digitar uma palavra para buscar
4. Executar busca com ou sem índice (independentemente)
5. Visualizar resultados e tempos de execução

## 🏗️ Estrutura do Projeto

```
indice-hash/
├── app.py                 # Interface Streamlit
├── main.py               # Script original de teste
├── entities/             # Entidades do sistema
│   ├── bucket.py         # Implementação de bucket
│   ├── pagina.py         # Implementação de página
│   ├── tabela.py         # Implementação de tabela
│   └── tupla.py          # Implementação de tupla
├── utils/
│   └── hash.py           # Funções de hash
├── data/
│   └── words_dictionary.json  # Dicionário de palavras
└── Pipfile               # Dependências do projeto
```

## 🔍 Como Usar

1. **Configure os parâmetros** na barra lateral:
   - Ajuste o tamanho da página (padrão: 1000)
   - Ajuste o tamanho do bucket (padrão: 10)
   - Ajuste o tamanho da chave hash (padrão: 300000)
   - Escolha o tipo de hash

2. **Carregue os dados** clicando em "🔄 Carregar Dados"

3. **Digite uma palavra** no campo de busca

4. **Execute as buscas**:
   - Clique em "🔍 Buscar com Índice" para busca rápida
   - Clique em "🔍 Buscar sem Índice" para busca sequencial
   - Os botões funcionam independentemente

5. **Visualize os resultados** com tempo de execução e status da busca

# indice-hash
Implementação de um Índice Hash em Python
