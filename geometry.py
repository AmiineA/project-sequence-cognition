def get_grid_coordinates(center_x, center_y, spacing):
    """
    Génère les coordonnées (x, y) pour une grille 5x5 centrée.
    Indices de 0 à 24 (0 = Haut-Gauche, 24 = Bas-Droite).
    """
    coords = []
    rows = 5
    cols = 5
    
    # Calcul du point de départ (Haut-Gauche) pour que la grille soit centrée
    start_x = center_x - ((cols - 1) * spacing) / 2
    start_y = center_y - ((rows - 1) * spacing) / 2
    
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * spacing
            y = start_y + r * spacing
            coords.append((x, y))
            
    return coords