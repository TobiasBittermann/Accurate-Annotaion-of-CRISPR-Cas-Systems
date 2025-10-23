from Bio import Phylo
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib
import gc

# Farbschema für unterschiedliche Quellen
SOURCE_COLORS = {
    "NCBI": "red",
    "CasPedia": "blue",
    "blastp_CasPedia": "cyan",
    "tblastn_CasPedia": "magenta",
    "CRISPR-Cas_Atlas": "green",
    "Marcus": "orange",
    "UniProt": "violet"
}


def get_label_color(label):
    """
    Bestimmt die Farbe eines Labels basierend auf der Quelle.
    Erwartet Label im Format: Name|Typ|Quelle
    """
    if "|" in label:
        parts = label.split("|")
        source = parts[-1]
        return SOURCE_COLORS.get(source, "black")
    return "black"

def plot_tree_from_newick_colored(nwk_file_path, svg_output_path):
    """
    Liest eine Newick-Datei und speichert den phylogenetischen Baum als SVG,
    wobei die Labels nach Quelle eingefärbt werden.
    """
    nwk_file_path = Path(nwk_file_path)
    svg_output_path = Path(svg_output_path)
    
    print(f"Reading Newick file: {nwk_file_path}")
    tree = Phylo.read(nwk_file_path, "newick")
    print("Tree loaded successfully.")
    
    num_seqs = len(tree.get_terminals())
    # Dynamische Größenberechnung ohne Beschränkung
    width = max(15, num_seqs * 0.3)  # Etwas kompakter für sehr große Bäume
    height = max(10, num_seqs * 0.25)
    
    print(f"Figure size set to width={width}, height={height} for {num_seqs} sequences")
    
    # SVG-Backend für Vektorgrafiken
    matplotlib.use('SVG')
    
    # Für sehr große Bäume: reduzierte DPI
    dpi = 150 if num_seqs > 500 else 300
    
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    axes = fig.add_subplot(1, 1, 1)
    
    print("Drawing tree with colored labels...")
    
    # Label-Funktion definieren
    def colored_label_func(clade):
        if clade.name:
            return clade.name
        return ""
    
    # Zeichnen des Baums mit Labels
    Phylo.draw(tree, do_show=False, axes=axes, label_func=colored_label_func)
    
    # Labels nachträglich einfärben
    for text in axes.get_children():
        if hasattr(text, 'get_text') and callable(getattr(text, 'get_text')):
            label_text = text.get_text()
            if label_text:
                text.set_color(get_label_color(label_text))
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.3, right=0.95, top=0.95, bottom=0.05)
    
    # Direkt als SVG speichern
    fig.savefig(svg_output_path, format="svg", bbox_inches='tight')
    print(f"SVG file saved: {svg_output_path}")
    
    # Speicher freigeben
    plt.close(fig)
    gc.collect()
    print("Figure closed and memory freed.")

# Folder definieren
input_folder = Path("../../NWK")
output_folder = Path("../../SVG")
output_folder.mkdir(exist_ok=True)

nwk_files = list(input_folder.glob("*.nwk"))
print(f"Found {len(nwk_files)} .nwk files in {input_folder}")

for nwk_file in nwk_files:
    svg_output_path = output_folder / f"{nwk_file.stem}.svg"
    print(f"--- Plotting {nwk_file.name} tree ---")
    try:
        plot_tree_from_newick_colored(nwk_file, svg_output_path)
        print(f"--- Done plotting {nwk_file.name} tree ---")
    except Exception as e:
        print(f"Error processing {nwk_file.name}: {e}")
        print(f"--- Failed plotting {nwk_file.name} tree ---")
