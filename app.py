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
st.title("Sistema de Índice Hash")
st.markdown("---")

# Inicializar estado da sessão
if 'table' not in st.session_state:
    st.session_state.table = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'search_results' not in st.session_state:
    st.session_state.search_results = {}
if 'statistics' not in st.session_state:
    st.session_state.statistics = {}

# Sidebar para configurações
st.sidebar.header("Configurações")

# Tamanho da página
page_size = st.sidebar.number_input(
    "Tamanho da Página (FR)",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100,
    help="Número de tuplas por página"
)

# Tamanho do bucket
bucket_size = st.sidebar.number_input(
    "Tamanho do Bucket",
    min_value=1,
    max_value=100,
    value=5,
    step=1,
    help="Número máximo de tuplas por bucket"
)

# Tipo de hash
hash_type = st.sidebar.selectbox(
    "Função Hash",
    ["custom", "python"],
    help="Escolha entre hash customizado ou nativo do Python"
)

# Botão para carregar dados
st.sidebar.markdown("---")
if st.sidebar.button("Carregar Dados", type="primary"):
    with st.spinner("Carregando dados e construindo índice..."):
        try:
            # Carregar o JSON da pasta data
            with open('data/words_dictionary.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Calcular número de buckets (NB > NR / FR)
            nr = len(data)  # Cardinalidade da tabela
            nb = max(1, (nr // bucket_size) + 1)  # Número de buckets
            
            # Criar tabela
            table = Table(page_size=page_size, hash_type=hash_type)
            
            # Inserir dados
            for key, value in data.items():
                table.insert(
                    tuple=Tuple(
                        key=key,
                        value=value
                    )
                )
            
            # Gerar hashes
            total_collisions = table.generate_hashes(bucket_size)
            
            # Calcular estatísticas
            total_overflows = 0

            for bucket in table.hash_index.values():
                bucket_data = bucket.get_data()
                total_overflows += bucket.get_overflow_count()
            
            collision_rate = (total_collisions / nr) * 100 if nr > 0 else 0
            overflow_rate = (total_overflows / len(table.hash_index)) * 100 if len(table.hash_index) > 0 else 0
            
            # Salvar no estado da sessão
            st.session_state.table = table
            st.session_state.data_loaded = True
            st.session_state.statistics = {
                'total_tuples': nr,
                'total_pages': len(table.get_pages()),
                'total_buckets': len(table.hash_index),
                'total_collisions': total_collisions,
                'total_overflows': total_overflows,
                'collision_rate': collision_rate,
                'overflow_rate': overflow_rate
            }
            
            st.sidebar.success("Dados carregados com sucesso!")
            
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar dados: {str(e)}")

# Área principal
if st.session_state.data_loaded and st.session_state.statistics and 'total_tuples' in st.session_state.statistics:
    stats = st.session_state.statistics
    
    # Estatísticas do sistema
    st.header("Estatísticas do Sistema")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Tuplas", stats['total_tuples'])
    with col2:
        st.metric("Total de Páginas", stats['total_pages'])
    with col3:
        st.metric("Total de Buckets", stats['total_buckets'])
    with col4:
        st.metric("Taxa de Colisões", f"{stats['collision_rate']:.2f}%")
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Taxa de Overflows", f"{stats['overflow_rate']:.2f}%")
    with col6:
        st.metric("Total de Colisões", stats['total_collisions'])
    with col7:
        st.metric("Total de Overflows", stats['total_overflows'])
    with col8:
        st.metric("Tamanho da Página", page_size)
    
    st.markdown("---")
    
    # Visualização das estruturas de dados
    st.header("Visualização das Estruturas de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Estrutura da Tabela")
        st.markdown(f"""
        - **Total de Tuplas**: {stats['total_tuples']}
        - **Total de Páginas**: {stats['total_pages']}
        - **Tuplas por Página**: {page_size}
        """)
        
        # Mostrar algumas páginas como exemplo
        if st.button("Mostrar Exemplo de Páginas"):
            st.write("**Primeiras 3 páginas:**")
            for i in range(min(3, len(st.session_state.table.get_pages()))):
                page = st.session_state.table.get_pages()[i]
                page_data = page.get_data()
                st.write(f"**Página {i+1}**: {len(page_data)} tuplas")
                if page_data:
                    st.write(f"Primeira tupla: {page_data[0].get_key()}")
                    if len(page_data) > 1:
                        st.write(f"Última tupla: {page_data[-1].get_key()}")
    
    with col2:
        st.subheader("Estrutura do Índice Hash")
        st.markdown(f"""
        - **Total de Buckets**: {stats['total_buckets']}
        - **Tamanho do Bucket**: {bucket_size}
        - **Taxa de Colisões**: {stats['collision_rate']:.2f}%
        - **Taxa de Overflows**: {stats['overflow_rate']:.2f}%
        """)
        
        # Mostrar alguns buckets como exemplo
        if st.button("Mostrar Exemplo de Buckets"):
            st.write("**Primeiros 3 buckets:**")
            bucket_count = 0
            for hash_key, bucket in st.session_state.table.hash_index.items():
                if bucket_count >= 3:
                    break
                bucket_data = bucket.get_data()
                st.write(f"**Bucket {hash_key}**: {len(bucket_data)} entradas")
                if bucket_data:
                    st.write(f"Primeira entrada: {bucket_data[0]['key']} -> Página {bucket_data[0]['page']}")
                bucket_count += 1
    
    st.markdown("---")
    
    # Seção de busca
    st.header("Busca de Chaves")
    
    search_word = st.text_input(
        "Chave de Busca:",
        placeholder="Digite uma palavra para buscar",
        help="Digite a chave que deseja buscar no dicionário"
    )
    
    if search_word:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Buscar com Índice Hash", type="primary"):
                with st.spinner("Buscando com índice hash..."):
                    timer_start = time.time()
                    result = st.session_state.table.search_with_hash(search_word)
                    timer_end = time.time()
                    
                    search_time = timer_end - timer_start
                    
                    # Encontrar a página onde a chave foi encontrada
                    page_found = None
                    if result:
                        hashed_key = st.session_state.table.hash_function(search_word)
                        if hashed_key in st.session_state.table.hash_index:
                            bucket_data = st.session_state.table.hash_index[hashed_key].get_data()
                            for entry in bucket_data:
                                if entry['key'] == search_word:
                                    page_found = entry['page'] + 1  # +1 para mostrar página 1-indexed
                                    break
                    
                    # Calcular custo (acessos a disco)
                    disk_accesses = 1  # Uma página lida
                    
                    st.session_state.search_results['with_hash'] = {
                        'word': search_word,
                        'result': result,
                        'time': search_time,
                        'disk_accesses': disk_accesses,
                        'page_found': page_found,
                        'method': 'Busca com Índice Hash'
                    }
        
        with col2:
            if st.button("Table Scan"):
                with st.spinner("Executando Table Scan..."):
                    timer_start = time.time()
                    result = None
                    pages_read = 0
                    page_found = None
                    
                    # Simular table scan
                    for page_num, page in enumerate(st.session_state.table.get_pages()):
                        pages_read += 1
                        for tuple in page.get_data():
                            if tuple.get_key() == search_word:
                                result = tuple.get_key()
                                page_found = page_num + 1  # +1 para mostrar página 1-indexed
                                break
                        if result:
                            break
                    
                    timer_end = time.time()
                    search_time = timer_end - timer_start
                    
                    st.session_state.search_results['table_scan'] = {
                        'word': search_word,
                        'result': result,
                        'time': search_time,
                        'pages_read': pages_read,
                        'page_found': page_found,
                        'method': 'Table Scan'
                    }
    
    # Exibir resultados
    if st.session_state.search_results:
        st.markdown("---")
        st.header("Resultados da Busca")
        
        for key, result_data in st.session_state.search_results.items():
            with st.expander(f"{result_data['method']} - Chave: '{result_data['word']}'", expanded=True):
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Método", result_data['method'])
                
                with col2:
                    if result_data['result']:
                        st.metric("Resultado", "Encontrada")
                    else:
                        st.metric("Resultado", "Não encontrada")
                
                with col3:
                    st.metric("Tempo", f"{result_data['time']:.9f}s")
                
                with col4:
                    if result_data['result'] and result_data.get('page_found'):
                        st.metric("Página Encontrada", f"Página {result_data['page_found']}")
                    else:
                        st.metric("Página Encontrada", "N/A")
                
                with col5:
                    if 'disk_accesses' in result_data:
                        st.metric("Acessos a Disco", result_data['disk_accesses'])
                    elif 'pages_read' in result_data:
                        st.metric("Páginas Lidas", result_data['pages_read'])
                
                if result_data['result']:
                    st.success(f"Chave '{result_data['word']}' encontrada na Página {result_data.get('page_found', 'N/A')}!")
                else:
                    st.warning(f"Chave '{result_data['word']}' não encontrada no dicionário.")
                
                # Mostrar custo estimado
                if 'disk_accesses' in result_data:
                    st.info(f"Custo estimado: {result_data['disk_accesses']} acesso(s) a disco")
                elif 'pages_read' in result_data:
                    st.info(f"Custo estimado: {result_data['pages_read']} página(s) lida(s)")

else:
    st.info("Configure as opções na barra lateral e clique em 'Carregar Dados' para começar.")
    
    # Mostrar informações sobre o sistema
    st.markdown("---")
    st.header("Sobre o Sistema")
    
    st.markdown("""
    Este sistema implementa um índice hash para busca eficiente de palavras em um dicionário.
    
    **Funcionalidades:**
    - Construção do índice hash com resolução de colisões
    - Busca por chave usando o índice construído
    - Table Scan para comparação de performance
    - Estatísticas de colisões e overflows
    - Cálculo de custos de acesso a disco
    
    **Estruturas de Dados:**
    - **Tupla**: Representa uma linha da tabela
    - **Tabela**: Contém todas as tuplas
    - **Página**: Divisão física da tabela
    - **Bucket**: Mapeia chaves em endereços de páginas
    - **Função Hash**: Mapeia chaves em endereços de buckets
    """)

# Footer
st.markdown("---")
st.markdown("Sistema de Índice Hash - Implementação didática")
