import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
import plotly.graph_objects as go
import plotly.subplots as sp

def plot_causal_dag(causal_model_dict, title, node_color='skyblue'):
    """Generates and displays a causal DAG from a dictionary of causal relationships and weights.

    Args:
        causal_model_dict (dict): A dictionary where keys are strings like 'Source -> Target'
                                  and values are the weights of the causal effect.
        title (str): The title for the DAG plot.
        node_color (str): The color for the nodes in the DAG.
    """
    G = nx.DiGraph()

    # Add nodes and edges with weights from the causal_model_dict
    for path, weight in causal_model_dict.items():
        source, target = path.split(' -> ')
        G.add_edge(source, target, weight=weight)

    # Define node positions for a clear layout
    pos = {
        'X1': (0, 0.5),   # Top left
        'X2': (1, 0.5),   # Top right
        'T': (0.5, 1), # Middle
        'Y': (0.5, 0)    # Bottom
    }

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw the graph
    nx.draw_networkx(
        G,
        pos,
        ax=ax,
        node_color=node_color,
        node_size=2000,
        font_size=10,
        with_labels=True,
        arrowstyle='->',
        arrowsize=20,
        edge_color='gray'
    )

    # Extract edge labels and format them
    edge_labels = nx.get_edge_attributes(G, 'weight')
    formatted_edge_labels = {
        (u, v):
        f'{d["weight"]:.1f}' for u, v, d in G.edges(data=True)
    }

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, ax=ax, font_color='gray')


    # Set title and turn off axes
    ax.set_title(title, fontsize=16)
    ax.axis('off')

    # Display the plot
    plt.show()

def plot_positivity_check_plotly(df, ps_column, treatment_column, title):
    """Generates a mirrored histogram plot using Plotly for a given propensity score distribution, vertically oriented."""

    ps_treated = df[df[treatment_column] == 1][ps_column]
    ps_control = df[df[treatment_column] == 0][ps_column]

    # Use 30 bins spanning 0 to 1
    bins = np.linspace(0, 1, 30)

    # Calculate histograms for density and counts
    hist_control_density, bins_control = np.histogram(ps_control, bins=bins, density=True)
    hist_control_counts, _ = np.histogram(ps_control, bins=bins, density=False)

    hist_treated_density, bins_treated = np.histogram(ps_treated, bins=bins, density=True)
    hist_treated_counts, _ = np.histogram(ps_treated, bins=bins, density=False)

    # Create figure
    fig = go.Figure()

    # Plot Control Group (positive frequencies on x-axis)
    fig.add_trace(go.Bar(
        y=bins_control[:-1], # Propensity score on Y-axis
        x=hist_control_density, # Density on X-axis
        width=np.diff(bins_control), # Bar height corresponds to bin width
        orientation='h',
        marker_color='forestgreen',
        name='Control',
        customdata=hist_control_counts,
        hovertemplate='Propensity Score: %{y:.2f}<br>' +
                      'Relative Frequency: %{x:.2f}<br>' +
                      'Absolute Frequency: %{customdata:.0f}<extra></extra>'
    ))

    # Plot Treated Group (negative frequencies on x-axis, mirrored)
    fig.add_trace(go.Bar(
        y=bins_treated[:-1], # Propensity score on Y-axis
        x=-hist_treated_density, # Mirror by making negative on X-axis
        width=np.diff(bins_treated),
        orientation='h',
        marker_color='#00008B',
        name='Treated',
        customdata=hist_treated_counts,
        hovertemplate='Propensity Score: %{y:.2f}<br>' +
                      'Relative Frequency: %{x:.2f}<br>' +
                      'Absolute Frequency: %{customdata:.0f}<extra></extra>'
    ))

    # Calculate separate min/max/median limits for each group
    min_ps_treated = ps_treated.min()
    max_ps_treated = ps_treated.max()
    median_ps_treated = ps_treated.median()
    min_ps_control = ps_control.min()
    max_ps_control = ps_control.max()
    median_ps_control = ps_control.median()

    # Add horizontal lines for treated group min/max/median
    fig.add_hline(y=min_ps_treated, line_width=1.5, line_dash='dot', line_color='darkblue', annotation_text=f'Treated Min ({min_ps_treated:.2f})', annotation_position='bottom right')
    fig.add_hline(y=max_ps_treated, line_width=1.5, line_dash='dot', line_color='darkblue', annotation_text=f'Treated Max ({max_ps_treated:.2f})', annotation_position='top right')
    fig.add_hline(y=median_ps_treated, line_width=1.5, line_dash='dash', line_color='darkblue', annotation_text=f'Treated Median ({median_ps_treated:.2f})', annotation_position='right')

    # Add horizontal lines for control group min/max/median
    fig.add_hline(y=min_ps_control, line_width=1.5, line_dash='dot', line_color='forestgreen', annotation_text=f'Control Min ({min_ps_control:.2f})', annotation_position='bottom left')
    fig.add_hline(y=max_ps_control, line_width=1.5, line_dash='dot', line_color='forestgreen', annotation_text=f'Control Max ({max_ps_control:.2f})', annotation_position='top left')
    fig.add_hline(y=median_ps_control, line_width=1.5, line_dash='dash', line_color='forestgreen', annotation_text=f'Control Median ({median_ps_control:.2f})', annotation_position='left')

    fig.update_layout(
        title_text=title,
        xaxis_title='Frequency (Density)', # Swapped axis titles
        yaxis_title='Propensity Score',
        bargap=0,
        hovermode='y unified' # Changed hovermode for vertical plot
    )

    # Adjust x-axis tick labels to show absolute values (since density is now on x)
    current_max_x = max(np.max(hist_control_density), np.max(hist_treated_density))
    fig.update_xaxes(range=[-1.1 * current_max_x, 1.1 * current_max_x], showticklabels=True)

    # Customizing tick labels to show absolute values for negative ticks on the new x-axis
    current_xtickvals = list(fig.layout.xaxis.tickvals) if fig.layout.xaxis.tickvals is not None else []
    if not current_xtickvals:
        x_min, x_max = fig.layout.xaxis.range
        current_xtickvals = np.linspace(x_min, x_max, 5).tolist() # Generate 5 ticks
    new_xtickvals = sorted(list(set([t for t in current_xtickvals if t >= 0] + [-t for t in current_xtickvals if t > 0])))
    fig.update_xaxes(tickvals=new_xtickvals, ticktext=[f'{abs(t):.2f}' for t in new_xtickvals], tickmode='array')

    # Propensity score (y-axis) should always be 0-1
    fig.update_yaxes(range=[0, 1])

    return fig

def plot_propensity_score_boxplots(df, ps_column, treatment_column, title):
    """Generates boxplots for propensity scores for treated and control groups."""

    fig = go.Figure()

    # Common hover template for both boxplots
    hover_template_str = '<b>%{y.name}</b><br>Min: %{y.min:.4f}<br>Q1: %{y.q1:.4f}<br>Median: %{y.median:.4f}<br>Q3: %{y.q3:.4f}<br>Max: %{y.max:.4f}<extra></extra>'

    # Boxplot for Control Group
    fig.add_trace(go.Box(
        y=df[df[treatment_column] == 0][ps_column],
        name='Control',
        marker_color='forestgreen',
        boxpoints=False,
        hovertemplate=hover_template_str
    ))

    # Boxplot for Treated Group
    fig.add_trace(go.Box(
        y=df[df[treatment_column] == 1][ps_column],
        name='Treated',
        marker_color='#00008B',
        boxpoints=False,
        hovertemplate=hover_template_str
    ))

    fig.update_layout(
        title_text=title,
        yaxis_title='Propensity Score',
        showlegend=True
    )

    # Ensure y-axis is from 0 to 1 for propensity scores
    fig.update_yaxes(range=[0, 1])

    return fig


def calculate_smd(df, covariates, treatment_column):
    """Calculates Standardized Mean Differences (SMD) for covariates.

    Args:
        df (pd.DataFrame): The input DataFrame.
        covariates (list): A list of covariate column names.
        treatment_column (str): The name of the treatment column (binary: 0 or 1).

    Returns:
        pd.Series: A Series containing the SMD for each covariate.
    """

    smd_values = {}
    treated_group = df[df[treatment_column] == 1]
    control_group = df[df[treatment_column] == 0]

    for cov in covariates:
        mean_treated = treated_group[cov].mean()
        mean_control = control_group[cov].mean()
        std_treated = treated_group[cov].std()
        std_control = control_group[cov].std()

        # Pooled standard deviation (assuming unequal sample sizes)
        n_treated = len(treated_group)
        n_control = len(control_group)

        pooled_std = np.sqrt(((n_treated - 1) * std_treated**2 + (n_control - 1) * std_control**2) / (n_treated + n_control - 2))

        smd = (mean_treated - mean_control) / pooled_std
        smd_values[cov] = smd

    return pd.Series(smd_values)



def plot_love_plot(smd_series, title, subplot_fig, row, col, x_limit, dot_color='skyblue'):
    """Generates a Love Plot (SMD plot) for covariate balance using Plotly.

    Args:
        smd_series (pd.Series): A Series of SMD values for covariates.
        title (str): The title for the plot. (Note: This title is now handled by make_subplots's subplot_titles)
        subplot_fig (go.Figure): The Plotly figure object to add the subplot to.
        row (int): The row index for the subplot.
        col (int): The column index for the subplot.
        x_limit (float): The maximum absolute value for the x-axis limits.
        dot_color (str): The color for the scatter plot dots.
    """
    covariates = smd_series.index.tolist()

    # Add scatter trace for SMD values
    subplot_fig.add_trace(go.Scatter(
        x=smd_series,
        y=covariates,
        mode='markers',
        marker=dict(color=dot_color, size=10),
        name='SMD',
        hovertemplate='Covariate: %{y}<br>SMD: %{x:.4f}<extra></extra>'
    ), row=row, col=col)

    # Add vertical line for SMD = 0
    subplot_fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1, row=row, col=col)
    # Add vertical line for SMD = 0.1 (threshold)
    subplot_fig.add_vline(x=0.1, line_dash="dash", line_color="red", line_width=1.5,
                          annotation_text='SMD = 0.1', annotation_position='top right', row=row, col=col)
    # Add vertical line for SMD = -0.1 (threshold)
    subplot_fig.add_vline(x=-0.1, line_dash="dash", line_color="red", line_width=1.5,
                          annotation_text='SMD = -0.1', annotation_position='top left', row=row, col=col)

    # Update layout for the specific subplot's axes
    subplot_fig.update_xaxes(title_text='Standardized Mean Difference', range=[-x_limit, x_limit], row=row, col=col)
    subplot_fig.update_yaxes(title_text='Covariate', categoryorder='array', categoryarray=covariates, row=row, col=col)
    # Removed subplot_fig.update_layout(title_text=title, row=row, col=col) as 'row' is not a valid layout property

    return subplot_fig


