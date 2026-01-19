
import json
import os

NOTEBOOK_PATH = "route_optimization_gironde.ipynb"

new_cells = [
  {
   "cell_type": "markdown",
   "id": "astar-markdown",
   "metadata": {},
   "source": [
    "# Step 4: A* Routing Visualization\n",
    "We calculate and visualize the exact road path between stops using the A* algorithm."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "astar-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "import os\n",
    "sys.path.append(os.getcwd())\n",
    "from astar import astar_path\n",
    "\n",
    "def plot_path_folium(G, path, m, color='green', weight=5, opacity=0.7):\n",
    "    \"\"\"Plot a path on a folium map.\"\"\"\n",
    "    route_coords = []\n",
    "    for node in path:\n",
    "        if node in G.nodes:\n",
    "            point = G.nodes[node]\n",
    "            route_coords.append((point['y'], point['x']))\n",
    "    \n",
    "    if route_coords:\n",
    "        folium.PolyLine(\n",
    "            route_coords,\n",
    "            color=color,\n",
    "            weight=weight,\n",
    "            opacity=opacity\n",
    "        ).add_to(m)\n",
    "    return m\n",
    "\n",
    "print(\"Calculating A* paths between stops...\")\n",
    "\n",
    "# Calculate and plot paths between consecutive stops\n",
    "try:\n",
    "    if 'route_idx' in locals() and 'G' in locals() and 'df' in locals() and 'm' in locals():\n",
    "        for i in range(len(route_idx) - 1):\n",
    "            # Get node IDs from dataframe using the route index\n",
    "            u_idx = route_idx[i]\n",
    "            v_idx = route_idx[i+1]\n",
    "            \n",
    "            u = df.iloc[u_idx]['node']\n",
    "            v = df.iloc[v_idx]['node']\n",
    "            \n",
    "            # Calculate path\n",
    "            path = astar_path(G, u, v, weight='length')\n",
    "            \n",
    "            # Plot path\n",
    "            plot_path_folium(G, path, m)\n",
    "            \n",
    "        print(\"Paths added to map (green lines).\")\n",
    "    else:\n",
    "        print(\"Required variables (route_idx, G, df, m) not found. Please run previous cells first.\")\n",
    "    \n",
    "except Exception as e:\n",
    "    print(f\"Error plotting paths: {e}\")\n",
    "\n",
    "m.save('route_map_with_astar.html')\n",
    "m"
   ]
  }
]

def update_notebook():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"Error: {NOTEBOOK_PATH} not found.")
        return

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Check if we already added it (simple check)
    if nb['cells'][-1]['source'][0].startswith("# Step 4"):
        print("Notebook already updated.")
        return

    nb['cells'].extend(new_cells)
    
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
        
    print(f"Successfully appended {len(new_cells)} cells to {NOTEBOOK_PATH}")

if __name__ == "__main__":
    update_notebook()
