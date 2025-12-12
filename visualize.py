import argparse

import matplotlib.pyplot as plt
import networkx as nx


def parse_pagerank_output(lines):
    graph = {}
    pageranks = {}
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('"'):
            continue

        parts = line.split('\t', 1)
        if len(parts) >= 2:
            page_id = parts[0].strip('"')
            data = parts[1].strip('"')
            data_parts = data.split('\\t')
            pagerank = float(data_parts[0])
            outlinks = data_parts[1].split(',') if len(data_parts) > 1 and data_parts[1] else []
            
            pageranks[page_id] = pagerank
            graph[page_id] = outlinks
    return graph, pageranks


def visualize_graph(graph, pageranks, output_file):
    G = nx.DiGraph()

    all_nodes = set(graph.keys())
    for outlinks in graph.values():
        all_nodes.update(outlinks)

    for node in all_nodes:
        G.add_node(node)

    for page_id, outlinks in graph.items():
        for outlink in outlinks:
            G.add_edge(page_id, outlink)

    max_pr = max(pageranks.values()) if pageranks else 1
    min_pr = min(pageranks.values()) if pageranks else 0
    
    node_sizes = []
    node_colors = []
    labels = {}
    
    for node in G.nodes():
        pr = pageranks.get(node, 0)
        if max_pr > min_pr:
            normalized = (pr - min_pr) / (max_pr - min_pr)
        else:
            normalized = 0.5
        size = 500 + normalized * 2500
        node_sizes.append(size)
        node_colors.append(pr)
        labels[node] = f"{node}\n{pr:.3f}"

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color='gray',
        arrows=True,
        arrowsize=20,
        arrowstyle='-|>',
        connectionstyle='arc3,rad=0.1',
        alpha=0.7
    )

    nodes = nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.YlOrRd,
        alpha=0.9
    )

    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels=labels,
        font_size=10,
        font_weight='bold'
    )

    plt.colorbar(nodes, ax=ax, label='PageRank')
    title = 'Graph with PageRank values'

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()

    plt.savefig(output_file, dpi=150, bbox_inches='tight')


def main():
    parser = argparse.ArgumentParser(description='Visualization of the PageRank graph')
    parser.add_argument('--input', '-i', required=True, help='File with PageRank results (output of pagerank.py)')
    parser.add_argument('--output', '-o', required=True, help='File where to save the image')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        lines = f.readlines()

    graph, pageranks = parse_pagerank_output(lines)

    visualize_graph(graph, pageranks, args.output)


if __name__ == '__main__':
    main()

