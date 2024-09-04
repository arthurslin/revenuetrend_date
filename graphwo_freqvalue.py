import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.ticker as ticker

def plot_wo_age_bucket(df_selection=None):
    try:
        if df_selection is None or df_selection.empty or len(df_selection)<5:
            print("No data available.")
            return

        df_filtered = df_selection.copy()

        nan_df = df_selection[df_selection['WO Age'].isna()].copy()      
        df_filtered = df_filtered.dropna(subset=['WO Age'])

        max_age = df_filtered['WO Age'].max()
        bins = range(0, int(max_age) + 101, 100)
       
        labels = [f'{i}-{i+99}' for i in bins[:-1]]
        
        df_filtered['WO Age Bucket'] = pd.cut(df_filtered['WO Age'], bins=bins, labels=labels, right=False)

        freq_counts = df_filtered['WO Age Bucket'].value_counts().reset_index()
        freq_counts.columns = ['WO Age Bucket', 'Frequency']
        
        wip_sums = df_filtered.groupby('WO Age Bucket')['WIP Value'].sum().reset_index()

        result_df = pd.merge(freq_counts, wip_sums, on='WO Age Bucket')
        result_df = result_df.sort_values('WO Age Bucket')

        fig, ax1 = plt.subplots(figsize=(16, 8))

        color = 'tab:red'
        ax1.set_xlabel('WO Age Bucket')
        ax1.set_ylabel('Frequency', color=color)
        ax1.bar(result_df['WO Age Bucket'], result_df['Frequency'], color=color, edgecolor='black')

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Sum of WIP Value (Millions)', color=color)
        ax2.bar(result_df['WO Age Bucket'], result_df['WIP Value'], color=color, width=0.20, edgecolor='black')

        # Custom formatter for millions
        def millions_formatter(x, pos):
            return '${:,.1f}M'.format(x / 1_000_000)

        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))

        ax1.set_ylim(bottom=0, top=ax1.get_ylim()[1]*1.1)
        ax2.set_ylim(top=result_df['WIP Value'].max() * 1.1)

        plt.title("Work Order Distribution Graph & WIP Value")
        plt.tight_layout()
        plt.grid()
        st.title("WO Age Distribution with WIP Value Sum")
        st.pyplot(fig)

    except KeyError as e:
        print(f"Error: Column '{e.args[0]}' not found in the DataFrame.")