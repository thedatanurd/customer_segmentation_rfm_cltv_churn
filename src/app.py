import streamlit as st
from streamlit_option_menu import option_menu
import charts as c
import snowflake.connector
import pandas as pd
from data_dictionaries import render_data_dictionary_app

# ──────────────────────────────────────────────────────────────────────────────
# 1. Load Data Function
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    creds = st.secrets["snowflake"]
    user = creds["user"]
    password = creds["password"]
    account = creds["account"]
    warehouse = creds["warehouse"]
    database = creds["database"]
    schema = creds["schema"]

    query_customer = "SELECT * FROM MARKETING_MART.MART_CUSTOMER_KPIS_AND_SEGMENTATION"
    query_overall = "SELECT * FROM MARKETING_MART.MART_OVERALL_CUSTOMER_KPIS"
    query_engagement = "SELECT * FROM MARKETING_MART.MART_CUSTOMER_DAU_MAU_STICKINESS"


    with snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    ) as conn:
        cur = conn.cursor()
        df_customer = cur.execute(query_customer).fetch_pandas_all()
        df_overall = cur.execute(query_overall).fetch_pandas_all()
        df_engagement = cur.execute(query_engagement).fetch_pandas_all()

    df_customer = df_customer[df_customer['CUSTOMERID'].notna()]
    return df_customer, df_overall, df_engagement

# ──────────────────────────────────────────────────────────────────────────────
# 2. Load Data
# ──────────────────────────────────────────────────────────────────────────────
df_customer, df_overall, df_engagement = load_data()

# ──────────────────────────────────────────────────────────────────────────────
# 3. Sidebar Navigation
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    selected = option_menu(
        'Main Menu',
        ['CLTV Segmentation', 'RFM Segmentation', 'Churn Risk Segmentation', 'Churn Metrics', 'Engagement Metrics', 'Overall Customer KPIS'],
        default_index=0
    )

# ──────────────────────────────────────────────────────────────────────────────
# 4. Metrics from df_overall
# ──────────────────────────────────────────────────────────────────────────────
if not df_overall.empty:
    AVERAGE_CUSTOMER_AOV = df_overall['AVERAGE_CUSTOMER_AOV'].iloc[0]
    TOTAL_CUSTOMERS = df_overall['TOTAL_CUSTOMERS'].iloc[0]
    AVERAGE_CLTV_PROFIT = df_overall['AVERAGE_CLTV_PROFIT'].iloc[0]
else:
    AVERAGE_CUSTOMER_AOV = TOTAL_CUSTOMERS = AVERAGE_CLTV_PROFIT = "N/A"

# ──────────────────────────────────────────────────────────────────────────────
# 5. Main View Rendering
# ──────────────────────────────────────────────────────────────────────────────
if selected == 'CLTV Segmentation':
    st.markdown("<h3 style='text-align: center;'>CLTV Segmentation</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(c.cltv_seg_pie(df_customer), use_container_width=True)
    with col2:
        st.plotly_chart(c.cltv_seg_bar(df_customer), use_container_width=True)
        
    render_data_dictionary_app("data_dictionaries/cltv_segmentation_data_dictionary.json")
    
elif selected == 'RFM Segmentation':
    st.markdown("<h3 style='text-align: center;'>RFM Segmentation</h3>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(c.rfm_seg_pie(df_customer), use_container_width=True)
    with col4:
        st.plotly_chart(c.rfm_seg_bar(df_customer), use_container_width=True)
    render_data_dictionary_app("data_dictionaries/rfm_segmentation_data_dictionary.json")
    
elif selected == 'Churn Risk Segmentation':
    st.markdown("<h3 style='text-align: center;'>Churn Risk Segmentation</h3>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(c.churn_seg_pie(df_customer), use_container_width=True)
    with col6:
        st.plotly_chart(c.churn_seg_bar(df_customer), use_container_width=True)
        
    render_data_dictionary_app("data_dictionaries/churn_risk_segmentation_full_data_dictionary.json")

elif selected == 'Churn Metrics':
    st.markdown("<h2 style='text-align: center;'>Churn Metrics</h2>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Customer Churn</h3>", unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        st.plotly_chart(c.churn_flag_pie(df_customer), use_container_width=True)
    with col8: 
        st.plotly_chart(c.churn_flag_bar(df_customer), use_container_width=True)
    render_data_dictionary_app("data_dictionaries/churn_status_data_dictionary.json")

elif selected == 'Engagement Metrics':    
    st.markdown("<h3 style='text-align: center;'>Engagement Metrics (DAU/MAU/Stickiness)</h3>", unsafe_allow_html=True)
    if not df_engagement.empty:
                       # Generate the graphs
            dau_mean= df_engagement['DAU'].mean()
            mau_mean= df_engagement['MAU'].mean()
            stickiness_mean= df_engagement['STICKINESS'].mean()
    
       
            st.markdown(f"<h4 style='text-align: center;' > Average DAU {dau_mean:.2f}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;' > Average MAU {mau_mean:.2f}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;' > Average Stickiness {stickiness_mean:.2f}</h4>", unsafe_allow_html=True)
            # Ensure datetime format
            df_engagement['INVOICEDATE'] = pd.to_datetime(df_engagement['INVOICEDATE'], errors='coerce')

            # Convert to native Python date for compatibility with st.slider
            min_date = df_engagement['INVOICEDATE'].min().date()
            max_date = df_engagement['INVOICEDATE'].max().date()
            st.markdown("<br><br>", unsafe_allow_html=True)
            # Date range slider
            start_date, end_date = st.slider(
                "Select Date Range for graphs:",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY-MM-DD"
            )

            # Filter DataFrame based on selected range
            df_filtered = df_engagement[
                (df_engagement['INVOICEDATE'] >= pd.to_datetime(start_date)) &
                (df_engagement['INVOICEDATE'] <= pd.to_datetime(end_date))
            ]

 
            fig_dau, fig_mau, fig_stickiness = c.dau_mau_stickiness_line(df_filtered)

            # Display the graphs
            col9, col10, col11 = st.columns(3)
            with col9:
                st.plotly_chart(fig_dau, use_container_width=True)
            with col10: 
                st.plotly_chart(fig_mau, use_container_width=True)
            with col11: 
                st.plotly_chart(fig_stickiness, use_container_width=True)
            render_data_dictionary_app('data_dictionaries/engagement_metrics_data_dictionary.json')
            
elif selected == 'Overall Customer KPIS':
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Overall</h3>", unsafe_allow_html=True)
    cola, colb, colc, cold = st.columns(4)
    with cola:
        st.markdown(f"<h6 style='text-align: center;'>Average Customer AOV: {AVERAGE_CUSTOMER_AOV:.2f}</h6>", unsafe_allow_html=True)
    with colb:
        st.markdown(f"<h6 style='text-align: center;'>Total Customers: {TOTAL_CUSTOMERS}</h6>", unsafe_allow_html=True)
    with colc:
        st.markdown(f"<h6 style='text-align: center;'>Average CLTV Profit: {AVERAGE_CLTV_PROFIT:.2f}</h6>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    render_data_dictionary_app("data_dictionaries/overall_kpis.json")    
else:
            st.warning("Engagement data is not available.")