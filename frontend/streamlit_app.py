import streamlit as st
import requests
import os
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000") 

def list_products():
    res = requests.get(f"{API_URL}/product/")
    if res.status_code == 200:
        return res.json()
    else:
        st.error("Erro ao buscar produtos")
        return []

def create_product(data):
    res = requests.post(f"{API_URL}/products/", json=data)
    return res

def update_product(product_id, data):
    res = requests.put(f"{API_URL}/products/{product_id}", json=data)
    return res

def delete_product(product_id):
    res = requests.delete(f"{API_URL}/products/{product_id}")
    return res

def main():
    st.title("CRUD de Produtos com FastAPI + Streamlit")

    menu = ["Listar Produtos", "Criar Produto", "Editar Produto", "Deletar Produto"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Listar Produtos":
        products = list_products()
        if products:
            df = pd.DataFrame(products)
            df = df[["id", "name", "description", "price", "category", "supplier_email"]]
            df = df.reset_index(drop=True)
            st.dataframe(df, hide_index=True)
        else:
            st.write("Nenhum produto encontrado.")

    elif choice == "Criar Produto":
        st.subheader("Criar Novo Produto")
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
                st.success("Produto criado com sucesso!")
            else:
                st.error(f"Erro ao criar produto: {res.text}")

    elif choice == "Editar Produto":
        st.subheader("Editar Produto Existente")
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
                        st.success("Produto atualizado com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar produto: {update_res.text}")
            else:
                st.error("Produto não encontrado")

    elif choice == "Deletar Produto":
        st.subheader("Deletar Produto")
        product_id = st.number_input("ID do Produto", min_value=1, step=1)
        if st.button("Deletar"):
            res = delete_product(product_id)
            if res.status_code == 200:
                st.success("Produto deletado com sucesso!")
            else:
                st.error("Erro ao deletar produto ou produto não encontrado")

if __name__ == "__main__":
    main()
