# # This R environment comes with many helpful analytics packages installed
# # It is defined by the kaggle/rstats Docker image: https://github.com/kaggle/docker-rstats
# # For example, here's a helpful package to load

# library(tidyverse) # metapackage of all tidyverse packages

import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow 
import pandas as pd
# dataset = pd.read_csv('/kaggle/input/lettuce-dataset-updated-copy/lettuce_dataset_updated_copy.csv', header= 0,
#                         encoding= 'unicode_escape')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

# list.files(path = "/kaggle/input/lettuce-dataset-updated-copy/lettuce_dataset_updated_copy.csv")

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# Load the dataset
df = pd.read_csv('/kaggle/input/lettuce-dataset-updated-copy/lettuce_dataset_updated_copy.csv', header= 0,
                        encoding= 'unicode_escape')

# --- Data Preparation for Visualization ---

# 1. Select representative Plant IDs (1, 35, and 70)
selected_plants = [1, 35, 70]
df_viz = df[df['Plant_ID'].isin(selected_plants)].copy()

# 2. Select key columns for plotting
plot_vars = ['Temperature (°C)', 'Humidity (%)', 'TDS Value (ppm)', 'pH Level']
id_vars = ['Plant_ID', 'Growth Days']
df_melted = df_viz[id_vars + plot_vars]

# 3. Melt the DataFrame from wide to long format
# This is necessary for using seaborn's FacetGrid to plot multiple metrics
df_melted = df_melted.melt(
    id_vars=id_vars,
    value_vars=plot_vars,
    var_name='Metric',
    value_name='Value'
)

# --- Create Visualization (Faceted Line Plot) ---

# Set a style for better visualization
sns.set_style("whitegrid")

# Create a FacetGrid
g = sns.FacetGrid(
    df_melted,
    col='Metric',
    col_wrap=2,
    sharex=True,
    sharey=False,  # Important: each metric needs its own Y-scale
    height=4,
    aspect=1.2
)

# Map a line plot onto the grid, colored by Plant_ID
g.map_dataframe(
    sns.lineplot,
    x='Growth Days',
    y='Value',
    hue='Plant_ID',
    palette='viridis',
    linewidth=2
)

# Add title and adjust aesthetics
g.set_axis_labels("Growth Days", "Value")
g.set_titles(col_template="{col_name}")
g.add_legend(title="Plant ID")
plt.subplots_adjust(top=0.9)
g.fig.suptitle(
    'Key Environmental Metrics Over Lettuce Growth Period (Plant IDs 1, 35, 70)',
    fontsize=16,
    fontweight='bold'
)

# Save the plot
plt.savefig('lettuce_environmental_metrics_python.png', dpi=300)
plt.close()

print("Visualization successfully created and saved as 'lettuce_environmental_metrics_python.png'")