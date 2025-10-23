#!/usr/bin/env python3

import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import re
import pandas as pd

# Color mapping for each Cas12 subtype
SUBTYPE_COLORS = {
    'cas12f': '#FF6B6B',
    'cas12k': '#4ECDC4',
    'cas12a': '#45B7D1',
    'cas12d': '#96CEB4',
    'cas12b': '#FECA57',
    'cas12c': '#FF9FF3',
    'cas12l': '#54A0FF',
    'cas12j': '#5F27CD',
    'cas12m': '#00D2D3',
    'cas12g': '#FF6348',
    'cas12e': '#2ED573',
    'cas12h': '#A55EEA',
    'cas12i': '#FFA502'
}

def analyze_subtypes(input_folder: str, keyword="cas12"):
    """
    Analyze files in a folder to extract Cas12 subtype occurrences.
    
    Args:
        input_folder: Path to folder containing files to analyze
        keyword: Keyword to search for (default: "cas12")
    
    Returns:
        Dictionary with filename as key and [subtypes_dict, keyword_count, total_lines] as value
    """
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
                    # Extract subtype letters following 'cas12'
                    matches = re.findall(r'cas12([a-zA-Z])', line.lower())
                    for subtype in matches:
                        full_subtype = f"cas12{subtype}"
                        all_subtypes[full_subtype] = all_subtypes.get(full_subtype, 0) + 1 

        data[file_name] = [all_subtypes, keyword_count, lines]
    
    return data

def create_dataframe(data):
    """
    Convert analysis data to pandas DataFrame for visualization.
    
    Args:
        data: Dictionary from analyze_subtypes function
    
    Returns:
        DataFrame with columns: File, Subtype, Count
    """
    df_data = []
    for filename, values in data.items():
        file_subtypes = values[0]
        for subtype, count in file_subtypes.items():
            df_data.append({'File': filename, 'Subtype': subtype, 'Count': count})
    
    return pd.DataFrame(df_data)

def plot_individual_diagrams(data, output_dir="../../DIAGRAMS"):
    """
    Create individual bar charts for each file showing Cas12 subtype distribution.
    
    Args:
        data: Dictionary from analyze_subtypes function
        output_dir: Directory to save individual diagram PDFs
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for filename, values in data.items():
        file_subtypes = values[0]

        if file_subtypes:
            # Sort subtypes alphabetically
            sorted_items = sorted(file_subtypes.items(), key=lambda x: x[0])
            subtypes = [item[0] for item in sorted_items]
            counts = [item[1] for item in sorted_items]
            
            # Apply specific colors for each subtype
            colors = [SUBTYPE_COLORS.get(subtype, '#95A5A6') for subtype in subtypes]

            # Create Plotly bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=subtypes, 
                    y=counts,
                    text=[str(count) for count in counts],
                    textposition='outside',
                    marker=dict(
                        color=colors
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
            
            # Remove file extension for output filename
            clean_filename = Path(filename).stem
            output_file = output_path / f"{clean_filename}_diagram.pdf"
            
            # Save as PDF
            fig.write_image(str(output_file))
            
            print(f"Individual diagram saved: {output_file}")

def plot_subtype_diagram(df, output_path="../../DIAGRAMS/HEADERS_diagram.pdf"):
    """
    Create grouped bar chart comparing Cas12 subtypes across all files.
    
    Args:
        df: DataFrame with File, Subtype, and Count columns
        output_path: Path to save the combined diagram PDF
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Pivot data for grouped bar chart
    pivot_df = df.pivot(index='File', columns='Subtype', values='Count').fillna(0)
    
    # Sort columns (subtypes) alphabetically
    pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)
    
    # Create Plotly grouped bar chart
    fig = go.Figure()
    
    # Add bar series for each subtype in alphabetical order
    for subtype in pivot_df.columns:
        color = SUBTYPE_COLORS.get(subtype, '#95A5A6')
        fig.add_trace(go.Bar(
            name=subtype,
            x=pivot_df.index,
            y=pivot_df[subtype],
            text=[str(int(val)) if val > 0 else '' for val in pivot_df[subtype]],
            textposition='outside',
            marker_color=color
        ))
    
    fig.update_layout(
        title="Cas12 Subtypes Comparison Across Files",
        xaxis_title="Files",
        yaxis_title="Count",
        xaxis_tickangle=60,
        barmode='group',
        width=1200,
        height=600,
        legend_title="Subtypes"
    )
    
    # Save as PDF
    fig.write_image(str(output_path))
    print(f"Combined diagram saved: {output_path}")

def main():
    """
    Main function to run the complete Cas12 subtype analysis and visualization pipeline.
    """
    # Analyze files in HEADERS directory
    data = analyze_subtypes("../../HEADERS")
    
    # Convert to DataFrame for visualization
    df = create_dataframe(data)
    
    # Generate visualizations
    plot_subtype_diagram(df)
    plot_individual_diagrams(data)
    
    # Print summary information
    print("Analyzed files:", list(data.keys()))
    print("Found subtypes:", df['Subtype'].unique())

if __name__ == "__main__":
    main()