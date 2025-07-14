import streamlit as st
from streamlit_option_menu import option_menu
import requests
import os
import pandas as pd
import math

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.markdown("""
<style>
.stApp { background-color: #1C1C1E; color: #E5E5E5; }
.css-1d391kg, .css-18e3th9 { background-color: #262730 !important; color: #E5E5E5; }
input, textarea, .stTextInput > div > div > input {
    background-color: #262730;
    color: #E5E5E5;
    border: 1px solid #505050;
    border-radius: 6px;
}
.stButton > button {
    background-color: #505050;
    color: #E5E5E5;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
}
.stButton > button:hover { background-color: #3A3A3C; }
.stDataFrame { background-color: #2C2C2E; }
h1, h2, h3, h4, h5, h6 { color: #E5E5E5; }
</style>
""", unsafe_allow_html=True)

def list_products():
    res = requests.get(f"{API_URL}/product/")
    return res.json() if res.status_code == 200 else []

def create_product(data):
    return requests.post(f"{API_URL}/products/", json=data)

def update_product(product_id, data):
    return requests.put(f"{API_URL}/products/{product_id}", json=data)

def delete_product(product_id):
    return requests.delete(f"{API_URL}/products/{product_id}")

def main():
    st.set_page_config(page_title="CRUD de Produtos", layout="wide")
    st.title("Gerenciamento de Produtos") 

    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 28px;">
                <span style="font-size: 3em;">💻</span>
                <span style="font-size: 2.2em; color: #E5E5E5; font-weight: bold;">MG Store</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        choice = option_menu(
            menu_title="Menu de Navegação",
            options=["Listar Produtos", "Criar Produto", "Editar Produto", "Deletar Produto"],
            icons=["list-task", "plus", "pencil-square", "trash"],
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#262730"},
                "icon": {"color": "#E5E5E5", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "2px",
                    "color": "#D0D0D0"
                },
                "nav-link-selected": {
                    "background-color": "#3A3A3C",
                    "font-weight": "bold",
                    "color": "#FFFFFF"
                },
            }
        )

    if choice == "Listar Produtos":
        st.markdown("### 📋 Lista de Produtos")
        with st.spinner("Carregando produtos..."):
            products = list_products()
        if products:
            # Paginação simples
            page_size = 10
            total = len(products)
            total_pages = math.ceil(total / page_size)
            page = st.number_input("Página", min_value=1, max_value=total_pages, value=1, step=1)
            start = (page - 1) * page_size
            end = start + page_size
            df = pd.DataFrame(products)
            df = df[["id", "name", "description", "price", "category", "supplier_email"]]
            df = df.reset_index(drop=True)
            st.dataframe(df.iloc[start:end], use_container_width=True, hide_index=True)
            st.caption(f"Exibindo {start+1}-{min(end,total)} de {total} produtos")
        else:
            st.warning("Nenhum produto encontrado.")

    elif choice == "Criar Produto":
        st.markdown("### 📦 Criar Produto")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nome")
            price = st.number_input("Preço", min_value=0.01, format="%.2f")
            category = st.text_input("Categoria")
        with col2:
            description = st.text_area("Descrição")
            supplier_email = st.text_input("Email do Fornecedor")

        if st.button("Criar"):
            if not name or not description or not category or not supplier_email:
                st.toast("Preencha todos os campos obrigatórios!", icon="⚠️")
            else:
                data = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "category": category,
                    "supplier_email": supplier_email
                }
                with st.spinner("Criando produto..."):
                    res = create_product(data)
                if res.status_code == 200:
                    st.toast("✅ Produto criado com sucesso!", icon="✅")
                else:
                    st.toast(f"❌ Erro ao criar produto: {res.text}", icon="❌")

    elif choice == "Editar Produto":
        st.markdown("### 📝 Editar Produto")
        product_id = st.number_input("ID do Produto", min_value=1, step=1)
        if st.button("Buscar Produto"):
            with st.spinner("Buscando produto..."):
                res = requests.get(f"{API_URL}/product/{product_id}")
            if res.status_code == 200:
                product = res.json()
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Nome", product["name"])
                    price = st.number_input("Preço", min_value=0.01, format="%.2f", value=product["price"])
                    category = st.text_input("Categoria", product["category"])
                with col2:
                    description = st.text_area("Descrição", product["description"])
                    supplier_email = st.text_input("Email do Fornecedor", product["supplier_email"])

                if st.button("Atualizar"):
                    if not name or not description or not category or not supplier_email:
                        st.toast("Preencha todos os campos obrigatórios!", icon="⚠️")
                    else:
                        data = {
                            "name": name,
                            "description": description,
                            "price": price,
                            "category": category,
                            "supplier_email": supplier_email
                        }
                        with st.spinner("Atualizando produto..."):
                            update_res = update_product(product_id, data)
                        if update_res.status_code == 200:
                            st.toast("✅ Produto atualizado com sucesso!", icon="✅")
                        else:
                            st.toast(f"❌ Erro ao atualizar produto: {update_res.text}", icon="❌")
            else:
                st.toast("❌ Produto não encontrado.", icon="❌")

    elif choice == "Deletar Produto":
        st.markdown("### 🗑️ Deletar Produto")
        product_id = st.number_input("ID do Produto", min_value=1, step=1)
        confirm = st.checkbox("Confirmo que desejo deletar este produto")
        if st.button("Deletar"):
            if not confirm:
                st.toast("Marque a caixa de confirmação para deletar.", icon="⚠️")
            else:
                with st.spinner("Deletando produto..."):
                    res = delete_product(product_id)
                if res.status_code == 200:
                    st.toast("✅ Produto deletado com sucesso!", icon="✅")
                else:
                    st.toast("❌ Erro ao deletar produto ou produto não encontrado.", icon="❌")

if __name__ == "__main__":
    main()