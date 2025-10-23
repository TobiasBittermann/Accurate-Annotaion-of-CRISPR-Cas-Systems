#!/usr/bin/env python3

import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import re
import pandas as pd

def analyze_subtypes(input_folder: str, keyword="cas12"):
    root_folder = Path(input_folder)
    data = {}
    
    for file in root_folder.iterdir():
        file_name = file.name
        all_subtypes = {}
        keyword_count = 0
        lines = 0

        with open(file, 'r') as infile:
            for line in infile:
                lines += 1
                if keyword in line.lower():
                    keyword_count += 1
                    matches = re.findall(r'cas12([a-zA-Z])', line.lower())
                    for subtype in matches:
                        full_subtype = f"cas12{subtype}"
                        all_subtypes[full_subtype] = all_subtypes.get(full_subtype, 0) + 1 

        data[file_name] = [all_subtypes, keyword_count, lines]
    
    return data

def create_dataframe(data):
    df_data = []
    for filename, values in data.items():
        file_subtypes = values[0]
        for subtype, count in file_subtypes.items():
            df_data.append({'File': filename, 'Subtype': subtype, 'Count': count})
    
    return pd.DataFrame(df_data)

def plot_individual_diagrams(data, output_dir="../DIAGRAMS"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for filename, values in data.items():
        file_subtypes = values[0]

        if file_subtypes:
            subtypes = list(file_subtypes.keys())
            counts = list(file_subtypes.values())

            # Erstelle Plotly Bar Chart
            fig = go.Figure(data=[
                go.Bar(
                    x=subtypes, 
                    y=counts,
                    text=[str(count) for count in counts],
                    textposition='outside',
                    marker=dict(
                        color=px.colors.qualitative.Set1[:len(subtypes)]
                    )
                )
            ])
            
            fig.update_layout(
                title=f"Cas12 Subtypes in {filename}",
                xaxis_title="Subtypes",
                yaxis_title="Count",
                xaxis_tickangle=60,
                width=800,
                height=600,
                showlegend=False
            )
            
            # Dateiname ohne Endung für Ausgabe
            clean_filename = Path(filename).stem
            output_file = output_path / f"{clean_filename}_diagram.pdf"
            
            # Speichere als PDF
            fig.write_image(str(output_file))
            
            print(f"Einzeldiagramm gespeichert: {output_file}")

def plot_subtype_diagram(df, output_path="../DIAGRAMS/HEADERS_diagram.pdf"):
    # Ordner erstellen falls nicht vorhanden
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pivot_df = df.pivot(index='File', columns='Subtype', values='Count').fillna(0)
    
    # Erstelle Plotly Grouped Bar Chart
    fig = go.Figure()
    
    # Füge für jeden Subtyp eine Bar-Serie hinzu
    colors = px.colors.qualitative.Set1
    for i, subtype in enumerate(pivot_df.columns):
        fig.add_trace(go.Bar(
            name=subtype,
            x=pivot_df.index,
            y=pivot_df[subtype],
            text=[str(int(val)) if val > 0 else '' for val in pivot_df[subtype]],
            textposition='outside',
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title="Cas12 Subtypes",
        xaxis_title="Files",
        yaxis_title="Count",
        xaxis_tickangle=60,
        barmode='group',  # Für grouped bars statt stacked
        width=1200,
        height=600,
        legend_title="Subtypes"
    )
    
    # Speichere als PDF
    fig.write_image(str(output_path))
    print(f"Diagramm gespeichert: {output_path}")

def main():
    data = analyze_subtypes("../HEADERS")
    df = create_dataframe(data)
    plot_subtype_diagram(df)
    plot_individual_diagrams(data)
    
    print("Analysierte Dateien:", list(data.keys()))
    print("Gefundene Subtypen:", df['Subtype'].unique())

if __name__ == "__main__":
    main()