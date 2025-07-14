import streamlit as st
from streamlit_option_menu import option_menu
import requests
import os
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")

# 🎨 Estilização com tons suaves de preto e cinza
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #1C1C1E;
    color: #E5E5E5;
}

/* Sidebar */
.css-1d391kg, .css-18e3th9 {
    background-color: #262730 !important;
    color: #E5E5E5;
}

/* Input fields */
input, textarea, .stTextInput > div > div > input {
    background-color: #262730;
    color: #E5E5E5;
    border: 1px solid #505050;
    border-radius: 6px;
}

/* Buttons */
.stButton > button {
    background-color: #505050;
    color: #E5E5E5;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
}

.stButton > button:hover {
    background-color: #3A3A3C;
}

/* DataFrame Table Styling */
.stDataFrame {
    background-color: #2C2C2E;
}

/* Markdown headings */
h1, h2, h3, h4, h5, h6 {
    color: #E5E5E5;
}
</style>
""", unsafe_allow_html=True)

# 🌐 Funções API
def list_products():
    res = requests.get(f"{API_URL}/product/")
    return res.json() if res.status_code == 200 else []

def create_product(data):
    return requests.post(f"{API_URL}/products/", json=data)

def update_product(product_id, data):
    return requests.put(f"{API_URL}/products/{product_id}", json=data)

def delete_product(product_id):
    return requests.delete(f"{API_URL}/products/{product_id}")

# 🧠 App principal
def main():
    st.set_page_config(page_title="CRUD de Produtos", layout="wide")

    with st.sidebar:
        choice = option_menu(
            menu_title=None,
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
        products = list_products()
        if products:
            df = pd.DataFrame(products)
            df = df[["id", "name", "description", "price", "category", "supplier_email"]]
            df = df.reset_index(drop=True)
            st.dataframe(df, hide_index=True)
        else:
            st.warning("Nenhum produto encontrado.")

    elif choice == "Criar Produto":
        st.markdown("### ➕ Criar Produto")
        name = st.text_input("Nome")
        description = st.text_area("Descrição")
        price = st.number_input("Preço", min_value=0.01, format="%.2f")
        category = st.text_input("Categoria")
        supplier_email = st.text_input("Email do Fornecedor")

        if st.button("Criar"):
            data = {
                "name": name,
                "description": description,
                "price": price,
                "category": category,
                "supplier_email": supplier_email
            }
            res = create_product(data)
            if res.status_code == 200:
                st.success("✅ Produto criado com sucesso!")
            else:
                st.error(f"❌ Erro ao criar produto: {res.text}")

    elif choice == "Editar Produto":
        st.markdown("### 📝 Editar Produto")
        product_id = st.number_input("ID do Produto", min_value=1, step=1)
        if st.button("Buscar Produto"):
            res = requests.get(f"{API_URL}/product/{product_id}")
            if res.status_code == 200:
                product = res.json()
                name = st.text_input("Nome", product["name"])
                description = st.text_area("Descrição", product["description"])
                price = st.number_input("Preço", min_value=0.01, format="%.2f", value=product["price"])
                category = st.text_input("Categoria", product["category"])
                supplier_email = st.text_input("Email do Fornecedor", product["supplier_email"])

                if st.button("Atualizar"):
                    data = {
                        "name": name,
                        "description": description,
                        "price": price,
                        "category": category,
                        "supplier_email": supplier_email
                    }
                    update_res = update_product(product_id, data)
                    if update_res.status_code == 200:
                        st.success("✅ Produto atualizado com sucesso!")
                    else:
                        st.error(f"❌ Erro ao atualizar produto: {update_res.text}")
            else:
                st.error("❌ Produto não encontrado.")

    elif choice == "Deletar Produto":
        st.markdown("### 🗑️ Deletar Produto")
        product_id = st.number_input("ID do Produto", min_value=1, step=1)
        if st.button("Deletar"):
            res = delete_product(product_id)
            if res.status_code == 200:
                st.success("✅ Produto deletado com sucesso!")
            else:
                st.error("❌ Erro ao deletar produto ou produto não encontrado.")

if __name__ == "__main__":
    main()