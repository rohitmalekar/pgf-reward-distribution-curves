# Read data file from the data folder
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(layout="centered")

def read_data(file_path):
    try:
        # Read the data file (supports csv, excel, etc. based on pandas)
        data = pd.read_csv(file_path)
        # Filter out the specific row
        data = data[~((data['to_project_name'] == 'nativesintech') & 
                     (data['from_project_name'] == 'opencollective'))]
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def create_distribution_curve(df, selected_pools):
    # Create a new figure
    fig = go.Figure()

    
    
    # Create distribution for each selected pool
    for pool_name in selected_pools:
        pool_data = df[df['grant_pool_name'] == pool_name]
        
        # Sort projects by funding amount (descending)
        sorted_amounts = sorted(pool_data['f0_'], reverse=True)
        total_funding = sum(sorted_amounts)
        total_projects = len(sorted_amounts)
        
        # Calculate cumulative percentages
        cumulative_funding = np.cumsum(sorted_amounts) / total_funding * 100
        project_percentiles = np.linspace(100/total_projects, 100, total_projects)
        
        # Add starting point (0,100) to the data
        x_values = np.concatenate(([0], project_percentiles))
        y_values = np.concatenate(([100], 100 - cumulative_funding))
        
        # Add trace for each pool
        fig.add_trace(
            go.Scatter(
                x=x_values,  # Changed from project_percentiles
                y=y_values,  # Changed from 100 - cumulative_funding
                name=pool_name,
                mode='lines+markers' if total_projects < 10 else 'lines',
                hovertemplate="Projects: %{x:.1f}%<br>Funding Remaining: %{y:.1f}%<extra></extra>"
            )
        )

    # Update layout
    fig.update_layout(
        title="Grant Funding Distribution by Pool",
        xaxis_title="Percentage of Projects Funded",
        yaxis_title="Percentage of Funding Remaining",
        hovermode='x unified',
        showlegend=True,
        template='plotly_white',
        xaxis=dict(
            gridcolor='lightgrey',
            range=[0, 100],  # Fix x-axis from 0 to 100
            constrain='domain'  # Maintain aspect ratio
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            range=[0, 100],  # Fix y-axis from 0 to 100
            constrain='domain'  # Maintain aspect ratio
        ),
        legend=dict(
            orientation="h",     # horizontal orientation
            yanchor="top",      # anchor point
            y=-0.2,             # position below the plot
            xanchor="center",   # anchor point
            x=0.5              # center horizontally
        ),
        height=800,
        width=800
    )
    
    return fig

def main():
    st.title("Grant Funding Distribution Analysis")
    
    # Read data
    data_path = "./data/funding by round.csv"  # Update with your file path
    df = read_data(data_path)
    
    if df is not None:
        # Get unique pool names
        all_pools = sorted(df['grant_pool_name'].unique())
        
        # Create multiselect dropdown
        selected_pools = st.multiselect(
            "Select Grant Pools to Display",
            options=all_pools,
            default=all_pools[:1]  # Default to first pool
        )
        
        # Show plot if pools are selected
        if selected_pools:
            fig = create_distribution_curve(df, selected_pools)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select at least one grant pool to display.")

if __name__ == "__main__":
    main()
        
