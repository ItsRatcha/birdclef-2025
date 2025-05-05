# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:00:00 2024

@author: Based on a Jupyter Notebook map_visualizer.ipynb
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np # Kept numpy for potential future use, though KNN part is removed

# CONFIG
train_csv = 'train.csv'
taxonomy_csv = 'taxonomy.csv'
output_html = 'birdclef2025_map.html'

# --- Data Loading and Preparation ---

# Load data
try:
    train_df = pd.read_csv(train_csv)
except FileNotFoundError:
    print(f"Error: {train_csv} not found. Please place it in the same directory.")
    exit() # Exit if essential file is missing

try:
    taxonomy_df = pd.read_csv(taxonomy_csv)
    # Rename columns: first column is often the species ID, 4th is the common name
    # Use column indices for robustness against slight name changes in taxonomy.csv
    taxonomy_df = taxonomy_df.rename(columns={taxonomy_df.columns[0]: 'id',
                                            taxonomy_df.columns[3]: 'name'})
except FileNotFoundError:
    print(f"Error: {taxonomy_csv} not found. Please place it in the same directory.")
    exit() # Exit if essential file is missing


# Select relevant columns from train_df and rename for clarity
# Using column indices as in the notebook for consistency
# 0: primary_label (id), 3: filename, 7: latitude, 8: longitude
data = train_df[[train_df.columns[0], train_df.columns[3], train_df.columns[7], train_df.columns[8]]].copy() # Use .copy() to avoid SettingWithCopyWarning
data.columns = ['id', 'filename', 'lat', 'lon']

# Merge name with train.csv based on 'id'
data = data.merge(taxonomy_df[['id', 'name']], on='id', how='left')

# Drop rows where name is missing (likely due to ID not being in taxonomy) or lat/lon are missing
data = data.dropna(subset=['name', 'lat', 'lon'])

# --- Removed KNN color clustering ---
# The original notebook used KNN to assign a 'color_group'. This is removed
# as per the user request to remove dot color and use different colors per species.

# --- Plotly Map Visualization with Multi-Select and Mode Toggle ---

fig = go.Figure()

# Get unique species names and prepare colors
all_names = sorted(data['name'].unique())
# Use a qualitative color scale with enough distinct colors
colors = px.colors.qualitative.Plotly # You can choose others like 'Bold', 'Vivid', etc.
# If there are more species than colors in the palette, colors will repeat
num_species = len(all_names)
num_colors = len(colors)
species_colors = {name: colors[i % num_colors] for i, name in enumerate(all_names)}


# Add traces for each bird species (both scatter and density/heatmap)
# All traces are initially hidden
for i, name in enumerate(all_names):
    subset = data[data['name'] == name].copy() # Use .copy()
    # Create ogg file path for hover info
    subset['ogg_path'] = 'train_audio/' + subset['id'] + '/' + subset['filename']

    # Scatter trace for this species
    fig.add_trace(go.Scattermapbox(
        lon=subset['lon'],
        lat=subset['lat'],
        mode='markers',
        marker=dict(
            size=6,
            color=species_colors[name], # Use unique color for the species
            opacity=0.8
        ),
        name=f'{name}_scatter', # Unique name for scatter trace
        legendgroup=name,       # Group scatter and density for the same species
        showlegend=False,       # Hide individual scatter/density traces in legend
        visible=False,          # Initially hidden
        text=subset['ogg_path'], # Shows on hover
        hoverinfo='text'
    ))

    # Density/Heatmap trace for this species
    # Use a colorscale that perhaps relates to the species color or a standard one
    # 'Plasma' or 'Viridis' are good general choices for density
    density_colorscale = px.colors.sequential.Plasma # Example density colorscale

    fig.add_trace(go.Densitymapbox(
        lon=subset['lon'],
        lat=subset['lat'],
        z=None, # No z-value needed; density is calculated from lat/lon point count
        radius=10, # Adjust radius to control the spread of the heatmap
        colorscale=density_colorscale,
        opacity=0.6,
        name=f'{name}_density', # Unique name for density trace
        legendgroup=name,       # Group scatter and density for the same species
        showlegend=False,       # Hide individual scatter/density traces in legend
        visible=False,          # Initially hidden
        hoverinfo='skip'        # Skip hover info for density layer
    ))

# --- UI Buttons for Species Selection (Toggle) and Mode Selection ---

# Create buttons for selecting/deselecting species
species_buttons = []
for i, name in enumerate(all_names):
    # Button to toggle visibility of scatter trace for this species
    species_buttons.append(dict(
        label=name,
        method='update',
        args=[{
            'visible': [
                True if trace.name == f'{name}_scatter' else False for trace in fig.data
            ]
        }]
    ))

# Create buttons for selecting visualization mode (Scatter or Heatmap)
mode_buttons = [
    dict(
        label='Show Scatter',
        method='update',
        args=[{
            'visible': [
                True if trace.name.endswith('_scatter') else False for trace in fig.data
            ]
        }]
    ),
    dict(
        label='Show Heatmap',
        method='update',
        args=[{
            'visible': [
                True if trace.name.endswith('_density') else False for trace in fig.data
            ]
        }]
    ),
    dict(
        label='Hide All',
        method='update',
        args=[{'visible': [False] * len(fig.data)}]
    )
]

# --- Layout Configuration ---

fig.update_layout(
    # Mapbox layout - essential for Scattermapbox and Densitymapbox
    mapbox=dict(
        style='carto-positron', # Choose a map style (e.g., 'open-street-map', 'carto-positron', 'stamen-terrain')
        center=dict(lat=0, lon=0), # Initial map center
        zoom=1 # Initial zoom level
    ),
    title='Bird Species Locations - BirdCLEF 2025',
    # Add updatemenus for species selection and mode selection
    updatemenus=[
        dict( # Mode selection (Scatter/Heatmap) - Use buttons aligned horizontally
            type='buttons',
            direction='right',
            active=-1, # No button initially active
            x=0.01,
            y=1.1, # Position above the plot area
            buttons=mode_buttons,
            pad=dict(r=10, t=10) # Padding around buttons
        ),
        dict( # Species Selection (Toggle individual species) - Use a dropdown for many species
            type='dropdown',
            showactive=True,
            buttons=species_buttons,
            x=0.01,
            y=1.05, # Position just below mode buttons
            pad=dict(r=10, t=10) # Padding around dropdown
        ),
    ],
    margin={"r":0,"t":50,"l":0,"b":0}, # Adjust margins
)

# --- Save Output ---
fig.write_html(output_html)

print(f"Map visualization saved to {output_html}")