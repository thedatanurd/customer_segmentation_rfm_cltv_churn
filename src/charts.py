import plotly.express as px
import pandas as pd

# ── RFM Segment Charts ─────────────────────────────────────────────

def dau_mau_stickiness_line(df_engagement):
    # Ensure all relevant columns are numeric
    df_engagement['DAU'] = pd.to_numeric(df_engagement['DAU'], errors='coerce')
    df_engagement['MAU'] = pd.to_numeric(df_engagement['MAU'], errors='coerce')
    df_engagement['STICKINESS'] = pd.to_numeric(df_engagement['STICKINESS'], errors='coerce')

    # Ensure date column is in datetime format
    df_engagement['INVOICEDATE'] = pd.to_datetime(df_engagement['INVOICEDATE'], errors='coerce')

    # Plot
    fig_1 = px.line(df_engagement, x='INVOICEDATE', y='DAU',
                  title='DAU Over Time')
    
    fig_2 = px.line(df_engagement, x='INVOICEDATE', y='MAU',
                  title='MAU Over Time')
    
    fig_3= px.line(df_engagement, x='INVOICEDATE', y='STICKINESS',
                  title='Stickiness Over Time')

    fig_1.update_layout(xaxis_title='Date', yaxis_title=None)
    fig_2.update_layout(xaxis_title='Date', yaxis_title=None)
    fig_3.update_layout(xaxis_title='Date', yaxis_title=None)

    return fig_1, fig_2, fig_3


def rfm_seg_pie(df):
    fig = px.pie(df, names='RFM_SEGMENTATION')
    fig.update_traces(hovertemplate='%{label}<br> %{value}<extra></extra>')
    return fig

def rfm_seg_bar(df):
    count_df = df['RFM_SEGMENTATION'].value_counts().reset_index()
    count_df.columns = ['RFM_SEGMENTATION', 'count']
    
    fig = px.bar(count_df, x='RFM_SEGMENTATION', y='count')
    fig.update_traces(
        marker_color="#7EC0F0",
        marker_line_width=0,
        hovertemplate='%{x}<br> %{y}<extra></extra>'
    )
    fig.update_layout(xaxis_title=None)
    return fig

# ── CLTV Segment Charts ─────────────────────────────────────────────

def cltv_seg_pie(df):
    fig = px.pie(df, names='CLTV_PROFIT_SEGMENTATION')
    fig.update_traces(hovertemplate='%{label}<br> %{value}<extra></extra>')
    return fig

def cltv_seg_bar(df):
    count_df = df['CLTV_PROFIT_SEGMENTATION'].value_counts().reset_index()
    count_df.columns = ['CLTV_PROFIT_SEGMENTATION', 'count']
    
    fig = px.bar(count_df, x='CLTV_PROFIT_SEGMENTATION', y='count')
    fig.update_traces(
        marker_color='#7EC0F0',
        marker_line_width=0,
        hovertemplate='%{x}<br> %{y}<extra></extra>'
    )
    fig.update_layout(xaxis_title=None)
    return fig

# ── Churn Flag Charts ─────────────────────────────────────────────

def churn_flag_pie(df):
    fig = px.pie(df, names='ISCHURNED')
    fig.update_traces(hovertemplate='%{label}<br> %{value}<extra></extra>')
    return fig

def churn_flag_bar(df):
    count_df = df['ISCHURNED'].value_counts().reset_index()
    count_df.columns = ['ISCHURNED', 'count']
    
    fig = px.bar(count_df, x='ISCHURNED', y='count')
    fig.update_traces(
        marker_color='#7EC0F0',
        marker_line_width=0,
        hovertemplate='%{x}<br> %{y}<extra></extra>'
    )
    fig.update_layout(xaxis_title=None)
    return fig

# ── Churn Risk Group Charts ─────────────────────────────────────────────

def churn_seg_pie(df):
    fig = px.pie(df, names='CHURN_RISK_GROUP')
    fig.update_traces(hovertemplate='%{label}<br> %{value}<extra></extra>')
    fig.update_layout(xaxis_title=None)
    return fig

def churn_seg_bar(df):
    count_df = df['CHURN_RISK_GROUP'].value_counts().reset_index()
    count_df.columns = ['CHURN_RISK_GROUP', 'count']
    
    fig = px.bar(count_df, x='CHURN_RISK_GROUP', y='count')
    fig.update_traces(
        marker_color='#7EC0F0',
        marker_line_width=0,
        hovertemplate='%{x}<br> %{y}<extra></extra>'
    )
    fig.update_layout(xaxis_title=None)
    return fig
