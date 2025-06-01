import math
import random
import matplotlib.pyplot as plt

random.seed(4206)

def draw_graph(matrix, directed=False, title=None, graph_type=None, steps=None):
    order = 0
    R = 10
    angle_step = 2 * math.pi / (len(matrix) - 1)
    positions = []
    for i in range(len(matrix)):
        if i == 0:
            positions.append((0, 0))
            continue
        angle = i * angle_step
        x = R * math.cos(angle)
        y = R * math.sin(angle)
        positions.append((x, y))

    node_R = 0.8

    def adjust_for_R(x1, y1, x2, y2, offset):
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length == 0:
            return x1, y1, x2, y2
        scale = (length - offset) / length
        return x1 + dx * (1 - scale), y1 + dy * (1 - scale), x2 - dx * (1 - scale), y2 - dy * (1 - scale)

    def draw_step(step, step_index, prev_active_node=None, order=0):
        if len(matrix) > 1:
            visited = step.get("visited", [])
            queue_or_stack = step.get("queue", [])
            active_node = queue_or_stack[0] if queue_or_stack else None
            order += 1
            print(f"{active_node} -> {order}")
            
            levels = step.get("levels", [-1] * len(matrix))
            
            plt.figure(figsize=(8, 8))
            plt.title(f"{title} - Step {step_index + 1}", fontsize=14)

            for i, (x, y) in enumerate(positions):
                if graph_type == "bfs":
                    if i + 1 == prev_active_node:
                        color = "#FF0000" 
                    elif levels[i] >= 0:
                        level_colors = [
                            "#FF0000",
                            "#FF8C00", 
                            "#FFD700", 
                        ]
                        color_index = min(levels[i], len(level_colors) - 1)
                        color = level_colors[color_index]
                    else:
                        color = 'lightgray' 
                else:
                    if i + 1 == active_node:
                        color = "#FF6347" 
                    elif i + 1 in visited:
                        color = "#FFD700" 
                    else:
                        color = 'lightgray' 
                
                plt.scatter(x, y, s=500, color=color, edgecolor="black", linewidth=1, zorder=2)
                plt.text(x, y, str(i + 1), fontsize=12, ha="center", va="center", zorder=4)

            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if matrix[i][j]:
                        x1, y1 = positions[i]
                        x2, y2 = positions[j]
                        x1, y1, x2, y2 = adjust_for_R(x1, y1, x2, y2, node_R)
                        
                        if graph_type == "bfs" and levels[i] >= 0 and levels[j] >= 0:
                            level_diff = abs(levels[i] - levels[j])
                            if level_diff == 1: 
                                edge_color = "#FF6347"
                                edge_width = 2.5
                            elif level_diff == 0:
                                edge_color = "#FFD700"
                                edge_width = 2.0
                            else:
                                edge_color = "gray" 
                                edge_width = 1.0
                        else:
                            is_active_edge = (i+1 == active_node and j+1 in visited) or (j+1 == active_node and i+1 in visited)
                            is_traversed_edge = (i+1 in visited and j+1 in visited)
                            
                            if is_active_edge:
                                edge_color = "#FF6347" 
                                edge_width = 2.5
                            elif is_traversed_edge:
                                edge_color = "#FFD700"
                                edge_width = 2.0
                            else:
                                edge_color = "gray"
                                edge_width = 1.0
                        
                        plt.plot([x1, x2], [y1, y2], color=edge_color, linewidth=edge_width, zorder=1)
                        
                        if directed:
                            plt.arrow(
                                x1, y1, x2 - x1, y2 - y1, 
                                head_width=0.30, length_includes_head=True, 
                                color=edge_color, linewidth=edge_width, zorder=3
                            )

            plt.xlim(-15, 15)
            plt.ylim(-15, 15)
            plt.axis("off")
            plt.show()


    if steps:
        prev_active_node = None
        for step_index, step in enumerate(steps):
            draw_step(step, step_index, prev_active_node, order)
            order += 1
            if graph_type == "bfs":
                prev_active_node = step.get("queue", [None])[0] if step.get("queue") else None
    else:
        plt.figure(figsize=(8, 8))
        for i, (x, y) in enumerate(positions):
            plt.scatter(x, y, s=500, color='lightgray', edgecolor='black', linewidth=1, zorder=2)  # Draw node
            plt.text(x, y, str(i + 1), fontsize=12, ha="center", va="center", zorder=4)  # Label node

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j]:
                    edge_color = (random.randint(0, 235) / 255, random.randint(0, 235) / 255, random.randint(0, 235) / 255)
                    
                    if matrix[i][i]:
                        x, y = positions[i]
                        loop_radius = 1  
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
                    
                    if (length >= 1.5*(R - node_R) and length <= 1.5*(R + node_R)):
                        norm_dx, norm_dy = dx / length, dy / length
                        perp_x, perp_y = -norm_dy, norm_dx
                        curve_factor = 1.5 + random.uniform(-0.5, 0.5)
                        midx = (x1 + x2) / 2 + perp_x * curve_factor
                        midy = (y1 + y2) / 2 + perp_y * curve_factor
                        t_values = [0, 0.25, 0.5, 0.75, 1.0]
                        curve_x = []
                        curve_y = []
                        
                        for t in t_values:
                            bx = (1-t)**2 * x1 + 2*(1-t)*t * midx + t**2 * x2
                            by = (1-t)**2 * y1 + 2*(1-t)*t * midy + t**2 * y2
                            curve_x.append(bx)
                            curve_y.append(by)
                        
                        if directed:
                            plt.plot(curve_x[:-1], curve_y[:-1], color=edge_color, zorder=3)
                            last_segment_x = curve_x[-2]
                            last_segment_y = curve_y[-2]
                            plt.arrow(last_segment_x, last_segment_y, 
                                    curve_x[-1] - last_segment_x, 
                                    curve_y[-1] - last_segment_y, 
                                    head_width=0.30, length_includes_head=True, 
                                    color=edge_color, zorder=4)
                        else:
                            plt.plot(curve_x, curve_y, color=edge_color, zorder=3)
                        continue
                    
                    if directed:
                        plt.arrow(x1, y1, x2 - x1, y2 - y1, head_width=0.30, length_includes_head=True, color=edge_color, zorder=4)
                        continue
                    plt.plot([x1, x2], [y1, y2], color=edge_color, zorder=3)
        plt.xlim(-15, 15)
        plt.ylim(-15, 15)
        plt.axis("off")
        plt.show()