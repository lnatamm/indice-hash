import streamlit as st
import time
import json
from entities.tabela import Table
from entities.tupla import Tuple

# Configuração da página
st.set_page_config(
    page_title="Sistema de Índice Hash",
    page_icon="🔍",
    layout="wide"
)

# Título da aplicação
st.title("🔍 Sistema de Índice Hash")
st.markdown("---")

# Inicializar estado da sessão
if 'table' not in st.session_state:
    st.session_state.table = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'search_results' not in st.session_state:
    st.session_state.search_results = {}

# Sidebar para configurações
st.sidebar.header("⚙️ Configurações")

# Configurações da página
st.sidebar.subheader("📄 Configurações da Página")
page_size = st.sidebar.number_input(
    "Tamanho da Página",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100,
    help="Número de tuplas por página"
)

# Configurações do bucket
st.sidebar.subheader("🪣 Configurações do Bucket")
bucket_size = st.sidebar.number_input(
    "Tamanho do Bucket",
    min_value=5,
    max_value=100,
    value=10,
    step=5,
    help="Número de elementos por bucket"
)

# Configurações da chave hash
st.sidebar.subheader("🔑 Configurações da Chave Hash")
hash_key_size = st.sidebar.number_input(
    "Tamanho da Chave Hash (n)",
    min_value=10000,
    max_value=1000000,
    value=300000,
    step=10000,
    help="Tamanho do espaço de hash"
)

hash_type = st.sidebar.selectbox(
    "Tipo de Hash",
    ["custom", "python"],
    help="Escolha entre hash customizado ou hash nativo do Python"
)

# Botão para carregar dados
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Carregar Dados", type="primary"):
    with st.spinner("Carregando dados e criando índice..."):
        try:
            # Carregar o JSON da pasta data
            with open('data/words_dictionary.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Criar tabela
            table = Table(page_size=page_size, hash_type=hash_type, n=hash_key_size)
            
            # Inserir dados
            for key, value in data.items():
                table.insert(
                    tuple=Tuple(
                        key=key,
                        value=value
                    )
                )
            
            # Gerar hashes
            table.generate_hashes(bucket_size)
            
            # Salvar no estado da sessão
            st.session_state.table = table
            st.session_state.data_loaded = True
            
            st.sidebar.success(f"✅ Dados carregados com sucesso!")
            st.sidebar.info(f"📊 Total de palavras: {len(data)}")
            st.sidebar.info(f"📄 Páginas criadas: {len(table.get_pages())}")
            
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao carregar dados: {str(e)}")

# Área principal
if st.session_state.data_loaded:
    st.success("✅ Dados carregados e prontos para busca!")
    
    # Seção de busca
    st.header("🔍 Busca de Palavras")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_word = st.text_input(
            "Digite a palavra para buscar:",
            placeholder="Ex: zwitterionic",
            help="Digite a palavra que deseja buscar no dicionário"
        )
    
    with col2:
        st.markdown("### Ações")
        col_search_hash, col_search_normal = st.columns(2)
        
        with col_search_hash:
            search_with_hash = st.button(
                "🔍 Buscar com Índice",
                type="primary",
                help="Busca usando o índice hash (mais rápido)"
            )
        
        with col_search_normal:
            search_without_hash = st.button(
                "🔍 Buscar sem Índice",
                help="Busca sequencial (mais lenta)"
            )
    
    # Processar buscas
    if search_with_hash and search_word:
        with st.spinner("Buscando com índice hash..."):
            timer_start = time.time()
            result = st.session_state.table.search_with_hash(search_word)
            timer_end = time.time()
            
            search_time = timer_end - timer_start
            
            st.session_state.search_results['with_hash'] = {
                'word': search_word,
                'result': result,
                'time': search_time,
                'method': 'Com Índice Hash'
            }
    
    if search_without_hash and search_word:
        with st.spinner("Buscando sem índice..."):
            timer_start = time.time()
            result = st.session_state.table.search(search_word)
            timer_end = time.time()
            
            search_time = timer_end - timer_start
            
            st.session_state.search_results['without_hash'] = {
                'word': search_word,
                'result': result,
                'time': search_time,
                'method': 'Sem Índice'
            }
    
    # Exibir resultados
    if st.session_state.search_results:
        st.markdown("---")
        st.header("📊 Resultados da Busca")
        
        for key, result_data in st.session_state.search_results.items():
            with st.expander(f"🔍 {result_data['method']} - Palavra: '{result_data['word']}'", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Método", result_data['method'])
                
                with col2:
                    if result_data['result']:
                        st.metric("Resultado", "✅ Encontrada")
                    else:
                        st.metric("Resultado", "❌ Não encontrada")
                
                with col3:
                    st.metric("Tempo", f"{result_data['time']:.9f}s")
                
                if result_data['result']:
                    st.success(f"✅ Palavra '{result_data['word']}' encontrada!")
                else:
                    st.warning(f"❌ Palavra '{result_data['word']}' não encontrada no dicionário.")
                
                st.code(f"Tempo de execução: {result_data['time']:.9f} segundos")

else:
    st.info("👈 Configure as opções na barra lateral e clique em 'Carregar Dados' para começar.")
    
    # Mostrar informações sobre o sistema
    st.markdown("---")
    st.header("ℹ️ Sobre o Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Funcionalidades")
        st.markdown("""
        - **Busca com Índice Hash**: Utiliza estrutura de hash para busca rápida
        - **Busca Sequencial**: Busca linear através de todas as páginas
        - **Configuração Flexível**: Ajuste tamanhos de página, bucket e chave hash
        - **Comparação de Performance**: Compare tempos de execução dos métodos
        """)
    
    with col2:
        st.subheader("⚙️ Configurações Disponíveis")
        st.markdown("""
        - **Tamanho da Página**: Número de tuplas por página
        - **Tamanho do Bucket**: Elementos por bucket no índice hash
        - **Chave Hash**: Tamanho do espaço de hash (n)
        - **Tipo de Hash**: Customizado ou nativo do Python
        """)

# Footer
st.markdown("---")
st.markdown("🔍 **Sistema de Índice Hash** - Desenvolvido para comparação de performance entre busca com e sem índice")
