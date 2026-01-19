"""
A* Algorithm implementation for routing on NetworkX graphs.
Compatible with OSMnx graphs where nodes have 'y' (lat) and 'x' (lon) attributes.
"""
import heapq
import math
import networkx as nx


def haversine_distance(node1_data, node2_data):
    """
    Calculate the great circle distance between two nodes in meters.
    
    Args:
        node1_data: Dictionary containing 'y' (lat) and 'x' (lon)
        node2_data: Dictionary containing 'y' (lat) and 'x' (lon)
        
    Returns:
        Distance in meters
    """
    R = 6371000  # Radius of Earth in meters
    
    lat1, lon1 = node1_data['y'], node1_data['x']
    lat2, lon2 = node2_data['y'], node2_data['x']
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def astar_path(G, source, target, weight='length'):
    """
    Find the shortest path between source and target using A* algorithm.
    
    Args:
        G: NetworkX graph
        source: Source node ID
        target: Target node ID
        weight: Edge attribute to use as cost (default: 'length')
        
    Returns:
        List of node IDs representing the path
        
    Raises:
        nx.NetworkXNoPath: If no path exists
    """
    if source not in G or target not in G:
        raise nx.NodeNotFound(f"Source {source} or target {target} not in graph")

    # Priority queue storing (f_score, node_id)
    open_set = [(0, source)]
    
    # Cost from start to node
    g_score = {source: 0}
    
    # Predecessor map for path reconstruction
    came_from = {}
    
    target_data = G.nodes[target]
    
    while open_set:
        # Get node with lowest f_score
        current_f, current = heapq.heappop(open_set)
        
        if current == target:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return list(reversed(path))
        
        # Build strict f_score check to avoid processing suboptimal paths?
        # Standard A* doesn't strictly need a 'visited' set if using g_score check,
        # but for performance we often check if we found a better way.
        
        for neighbor in G.neighbors(current):
            # Calculate tentative g_score
            edge_data = G.get_edge_data(current, neighbor)
            # Handle MultiGraph (OSMnx often returns MultiDiGraph), take shortest edge
            if isinstance(edge_data, dict) and 0 in edge_data: # MultiGraph with keys
                 # Find min weight among parallel edges
                 cost = float('inf')
                 for key in edge_data:
                     cost = min(cost, edge_data[key].get(weight, 1))
            else:
                 cost = edge_data.get(weight, 1)
            
            tentative_g = g_score[current] + cost
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                
                # Heuristic: straight line distance to target
                h = haversine_distance(G.nodes[neighbor], target_data)
                f_score = tentative_g + h
                
                heapq.heappush(open_set, (f_score, neighbor))
                
    raise nx.NetworkXNoPath(f"No path between {source} and {target}")
