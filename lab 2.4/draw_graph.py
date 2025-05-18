import math
import random
import matplotlib.pyplot as plt

random.seed(4206)

def draw_graph(matrix, directed=False):
    R = 10  # Radius of the circular layout
    if (len(matrix) > 1):
        angle_step = 2 * math.pi / (len(matrix) - 1)  # Angle between nodes

    # Calculate node positions
    positions = []
    for i in range(len(matrix)):
        if i == 0:
            positions.append((0, 0))  # Center node
            continue
        angle = i * angle_step
        x = R * math.cos(angle)
        y = R * math.sin(angle)
        positions.append((x, y))

    node_R = 0.8  # Node radius

    # Plot the nodes
    plt.figure(figsize=(8, 8))
    for i, (x, y) in enumerate(positions):
        plt.scatter(x, y, s=500, color="gray", zorder=2)  # Draw node
        plt.text(x, y, str(i + 1), fontsize=12, ha="center", va="center", zorder=4)  # Label node

    # Helper function to adjust for node boundary
    def adjust_for_R(x1, y1, x2, y2, offset):
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length == 0:
            return x1, y1, x2, y2
        scale = (length - offset) / length
        return x1 + dx * (1 - scale), y1 + dy * (1 - scale), x2 - dx * (1 - scale), y2 - dy * (1 - scale)

    # Plot the edges
    m = 1
    def rand(a):
        return random.choice([random.uniform(-2*a,(node_R + a/8)), random.uniform((node_R + a/8),2*a)])

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j]:
                # Draw self-loop if a node connects to itself
                edge_color = (random.randint(0, 235) / 255, random.randint(0, 235) / 255, random.randint(0, 235) / 255)  # Generate a random RGB color
                if matrix[i][i]:
                    x, y = positions[i]
                    loop_radius = 1  # Adjust for better visibility
                    if(x != 0 and y != 0):
                        vector_length = math.sqrt(x ** 2 + y ** 2)
                        x += x * loop_radius / vector_length
                        y += y * loop_radius / vector_length
                    else:
                        y += loop_radius
                    loop = plt.Circle((x, y), loop_radius, color=edge_color, fill=False, zorder=1)
                    plt.gca().add_patch(loop)
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                dx, dy = x2 - x1, y2 - y1
                length = math.sqrt(dx ** 2 + dy ** 2)
                x1, y1, x2, y2 = adjust_for_R(x1, y1, x2, y2, node_R)
                if (length >= 2*(R - node_R) and length <= 2*(R + node_R)):  # If the line goes through the center
                    midx = (x1 + x2) / 2 + rand(m)
                    midy = (y1 + y2) / 2 + rand(m)
                    # Draw directed edge (arrow)
                    if directed:
                        plt.plot([x1, midx], [y1, midy], color=edge_color, zorder=3)
                        plt.arrow(midx, midy, x2 - midx, y2 - midy, head_width=0.30, length_includes_head=True, color=edge_color, zorder=4)
                        continue
                    plt.plot([x1, midx, x2], [y1, midy, y2], color=edge_color, zorder=3)
                    continue
                if directed:
                    plt.arrow(x1, y1, x2 - x1, y2 - y1, head_width=0.30, length_includes_head=True, color=edge_color, zorder=4)
                    continue
                plt.plot([x1, x2], [y1, y2], color=edge_color, zorder=3)

    # Set plot limits and hide axes
    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    plt.axis("off")
    plt.show()