import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        
        st.subheader("Top 5 Clientes com Maior Receita")
        query = """
            SELECT c.nome, SUM(cr.valor) AS total_receita
            FROM clientes c
            JOIN contas_receber cr ON c.id = cr.cliente_id
            WHERE cr.status = 'Recebido'
            GROUP BY c.id
            ORDER BY total_receita DESC
            LIMIT 5
        """
        df_receitas = pd.read_sql_query(query, conn)
        st.dataframe(df_receitas)

        fig, ax = plt.subplots()
        ax.bar(df_receitas['nome'], df_receitas['total_receita'])
        ax.set_xlabel('Clientes')
        ax.set_ylabel('Receita Total')
        ax.set_title('Top 5 Clientes com Maior Receita')
        st.pyplot(fig)
        
        st.subheader("Status das Contas a Pagar e Receber")
        query_status = """
            SELECT status, COUNT(*) AS count_status
            FROM (
                SELECT status FROM contas_pagar
                UNION ALL
                SELECT status FROM contas_receber
            )
            GROUP BY status
        """
        df_status = pd.read_sql_query(query_status, conn)
        st.dataframe(df_status)
        
        fig2, ax2 = plt.subplots()
        ax2.bar(df_status['status'], df_status['count_status'])
        ax2.set_xlabel('Status')
        ax2.set_ylabel('Quantidade')
        ax2.set_title('Status das Contas a Pagar e Receber')
        st.pyplot(fig2)
        
        st.subheader("Comparação Receita vs Despesa")
        query_comparacao = """
            SELECT tipo, SUM(valor) AS total
            FROM lancamentos
            WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
            GROUP BY tipo
        """
        df_comparacao = pd.read_sql_query(query_comparacao, conn)
        st.dataframe(df_comparacao)
        
        fig3, ax3 = plt.subplots()
        ax3.bar(df_comparacao['tipo'], df_comparacao['total'])
        ax3.set_xlabel('Tipo')
        ax3.set_ylabel('Valor Total')
        ax3.set_title('Comparação Receita vs Despesa (Mês Atual)')
        st.pyplot(fig3)
    
    conn.close()

if __name__ == "__main__":
    main()
