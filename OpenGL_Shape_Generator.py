import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
import math

class OpenGLShapeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenGL Shape Generator")
        self.root.geometry("1150x750")
        
        # --- Modern Theme Colors ---
        self.colors = {
            "bg": "#2b2d31",           
            "panel": "#313338",        
            "canvas": "#1e1f22",       
            "text": "#f2f3f5",         
            "text_muted": "#b5bac1",   
            "accent": "#5865f2",       
            "accent_hover": "#4752c4", 
            "btn": "#4e5058",          
            "btn_hover": "#6d6f78",    
            "grid": "#3f4147",         
            "axis": "#70737d",         
            "danger": "#da373c",       
            "success": "#23a559"       
        }
        
        self.root.configure(bg=self.colors["bg"])
        
        # --- Application State ---
        self.shapes = []
        self.current_vertices = []
        self.current_color = (88, 101, 242) 
        self.shape_counter = 1
        
        self.current_tool = "Polygon"
        self.is_dragging = False
        self.start_x = 0
        self.start_y = 0
        self.temp_vertices = []
        
        # Canvas constants
        self.canvas_size = 600
        self.half_size = self.canvas_size / 2
        
        self.setup_ui()
        self.redraw_canvas()

    def create_modern_button(self, parent, text, command, bg_color, hover_color, **kwargs):
        btn = tk.Button(parent, text=text, command=command, bg=bg_color, fg=self.colors["text"], 
                        activebackground=hover_color, activeforeground=self.colors["text"], 
                        relief="flat", borderwidth=0, font=("Segoe UI", 10, "bold"), cursor="hand2", **kwargs)
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color) if btn['bg'] != self.colors['accent'] else None)
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg_color) if btn['bg'] != self.colors['accent'] else None)
        return btn

    def setup_ui(self):
        # --- Left Panel: Canvas area ---
        left_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=20)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_border = tk.Frame(left_frame, bg=self.colors["grid"], padx=2, pady=2)
        canvas_border.pack()
        
        self.canvas = tk.Canvas(canvas_border, width=self.canvas_size, height=self.canvas_size, 
                                bg=self.colors["canvas"], highlightthickness=0, cursor="crosshair")
        self.canvas.pack()
        
        # Mouse bindings for click-and-drag
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        self.coord_label = tk.Label(left_frame, text="X: 0.00 | Y: 0.00", bg=self.colors["bg"], 
                                    fg=self.colors["text_muted"], font=("Consolas", 12))
        self.coord_label.pack(pady=10)
        
        # --- Right Panel: Controls ---
        right_frame = tk.Frame(self.root, bg=self.colors["panel"], padx=25, pady=20)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tools Selection
        tk.Label(right_frame, text="SHAPE TOOLS", bg=self.colors["panel"], fg=self.colors["text_muted"], 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0,10))
                 
        tools_frame = tk.Frame(right_frame, bg=self.colors["panel"])
        tools_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.tool_buttons = {}
        tools = [("Polygon", 0, 0), ("Line", 0, 1), 
                 ("Rectangle", 1, 0), ("Square", 1, 1), 
                 ("Triangle", 2, 0), ("Circle", 2, 1)]
                 
        for tool, row, col in tools:
            btn = tk.Button(tools_frame, text=tool, command=lambda t=tool: self.select_tool(t),
                            bg=self.colors["btn"], fg=self.colors["text"], relief="flat", borderwidth=0, 
                            font=("Segoe UI", 9, "bold"), cursor="hand2")
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            tools_frame.grid_columnconfigure(col, weight=1)
            self.tool_buttons[tool] = btn
            
        # Drawing Modifiers
        self.snap_var = tk.BooleanVar(value=False)
        tk.Checkbutton(right_frame, text="Snap to Grid", variable=self.snap_var, 
                                 bg=self.colors["panel"], fg=self.colors["text"], selectcolor=self.colors["btn"],
                                 activebackground=self.colors["panel"], activeforeground=self.colors["text"], font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(5, 5))
        
        self.color_btn = self.create_modern_button(right_frame, "Pick Color", self.pick_color, self.colors["btn"], self.colors["btn_hover"])
        self.color_btn.pack(fill=tk.X, pady=5, ipady=4)
        
        # Create Close Button BEFORE selecting default tool to prevent crash
        self.close_btn = self.create_modern_button(right_frame, "Close Polygon", self.close_polygon, self.colors["success"], "#1d8749")
        
        self.select_tool("Polygon") # Set default tool
        
        # Object Management
        tk.Label(right_frame, text="OBJECT MANAGEMENT", bg=self.colors["panel"], fg=self.colors["text_muted"], 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(25,10))
        
        listbox_frame = tk.Frame(right_frame, bg=self.colors["grid"], padx=1, pady=1)
        listbox_frame.pack(fill=tk.X, pady=(0, 10))
        self.shape_listbox = tk.Listbox(listbox_frame, height=5, bg=self.colors["bg"], fg=self.colors["text"], 
                                        selectbackground=self.colors["accent"], borderwidth=0, highlightthickness=0, font=("Segoe UI", 10))
        self.shape_listbox.pack(fill=tk.X)
        
        btn_frame = tk.Frame(right_frame, bg=self.colors["panel"])
        btn_frame.pack(fill=tk.X)
        self.create_modern_button(btn_frame, "Delete", self.delete_shape, self.colors["danger"], "#a1282c").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,4), ipady=4)
        self.create_modern_button(btn_frame, "Clear", self.clear_canvas, self.colors["btn"], self.colors["btn_hover"]).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(4,0), ipady=4)
        
        # Code Generation
        tk.Label(right_frame, text="EXPORT", bg=self.colors["panel"], fg=self.colors["text_muted"], 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(25,10))
        
        self.create_modern_button(right_frame, "Generate C++ Code", self.generate_code, self.colors["accent"], self.colors["accent_hover"]).pack(fill=tk.X, pady=5, ipady=8)
        
        text_frame = tk.Frame(right_frame, bg=self.colors["grid"], padx=1, pady=1)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.code_text = tk.Text(text_frame, height=8, width=35, bg=self.colors["canvas"], fg=self.colors["text"], 
                                 insertbackground=self.colors["text"], borderwidth=0, highlightthickness=0, font=("Consolas", 10))
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        export_frame = tk.Frame(right_frame, bg=self.colors["panel"])
        export_frame.pack(fill=tk.X, pady=5)
        self.create_modern_button(export_frame, "Copy Code", self.copy_code, self.colors["btn"], self.colors["btn_hover"]).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,4), ipady=4)
        self.create_modern_button(export_frame, "Save .cpp", self.save_code, self.colors["btn"], self.colors["btn_hover"]).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(4,0), ipady=4)

    def select_tool(self, tool):
        self.current_tool = tool
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.configure(bg=self.colors["accent"], fg="white")
            else:
                btn.configure(bg=self.colors["btn"], fg=self.colors["text"])
        
        # Only show "Close Polygon" button if Polygon tool is active
        if tool == "Polygon":
            self.close_btn.pack(fill=tk.X, pady=5, ipady=4)
        else:
            self.close_btn.pack_forget()
            self.current_vertices.clear()
            self.redraw_canvas()

    # --- Coordinate Math ---
    def tk_to_gl(self, x, y):
        gl_x = (x - self.half_size) / self.half_size
        gl_y = (self.half_size - y) / self.half_size
        return gl_x, gl_y

    def gl_to_tk(self, gl_x, gl_y):
        x = (gl_x * self.half_size) + self.half_size
        y = self.half_size - (gl_y * self.half_size)
        return x, y

    def snap_coordinate(self, val):
        return round(val * 10) / 10.0

    def get_snapped_gl(self, x, y):
        gl_x, gl_y = self.tk_to_gl(x, y)
        if self.snap_var.get():
            gl_x = self.snap_coordinate(gl_x)
            gl_y = self.snap_coordinate(gl_y)
        return gl_x, gl_y

    # --- Mouse Interactions ---
    def on_mouse_move(self, event):
        gl_x, gl_y = self.get_snapped_gl(event.x, event.y)
        self.coord_label.config(text=f"X: {gl_x:.2f}  |  Y: {gl_y:.2f}")

    def on_mouse_press(self, event):
        if self.current_tool == "Polygon":
            gl_x, gl_y = self.get_snapped_gl(event.x, event.y)
            self.current_vertices.append((gl_x, gl_y))
            self.redraw_canvas()
        else:
            self.is_dragging = True
            self.start_x, self.start_y = self.get_snapped_gl(event.x, event.y)
            self.temp_vertices = []

    def on_mouse_drag(self, event):
        if not self.is_dragging or self.current_tool == "Polygon": return
        
        gl_x1, gl_y1 = self.start_x, self.start_y
        gl_x2, gl_y2 = self.get_snapped_gl(event.x, event.y)
        
        self.temp_vertices = self.calculate_shape_vertices(self.current_tool, gl_x1, gl_y1, gl_x2, gl_y2)
        self.redraw_canvas()
        self.on_mouse_move(event)

    def on_mouse_release(self, event):
        if not self.is_dragging or self.current_tool == "Polygon": return
        self.is_dragging = False
        
        if len(self.temp_vertices) >= 2:
            self.add_shape_to_list(self.current_tool, self.temp_vertices)
            
        self.temp_vertices = []
        self.redraw_canvas()

    def calculate_shape_vertices(self, tool, x1, y1, x2, y2):
        if tool == "Line":
            return [(x1, y1), (x2, y2)]
            
        elif tool == "Rectangle":
            return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            
        elif tool == "Square":
            dx = x2 - x1
            dy = y2 - y1
            side = max(abs(dx), abs(dy))
            sign_x = 1 if dx >= 0 else -1
            sign_y = 1 if dy >= 0 else -1
            x2 = x1 + (side * sign_x)
            y2 = y1 + (side * sign_y)
            return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            
        elif tool == "Triangle":
            return [((x1 + x2) / 2, y1), (x2, y2), (x1, y2)]
            
        elif tool == "Circle":
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = max(abs(x2 - x1), abs(y2 - y1)) / 2
            verts = []
            for i in range(32):
                angle = i * (2 * math.pi / 32)
                vx = center_x + radius * math.cos(angle)
                vy = center_y + radius * math.sin(angle)
                verts.append((vx, vy))
            return verts
        return []

    # --- Shape Management ---
    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose shape color", color=f'#{self.current_color[0]:02x}{self.current_color[1]:02x}{self.current_color[2]:02x}')
        if color_code[0]: 
            self.current_color = tuple(map(int, color_code[0]))
            self.color_btn.config(text=f"Color: {color_code[1].upper()}")

    def close_polygon(self):
        if len(self.current_vertices) < 3:
            messagebox.showwarning("Warning", "A polygon needs at least 3 vertices!")
            return
        self.add_shape_to_list("Polygon", self.current_vertices)
        self.current_vertices.clear()
        self.redraw_canvas()

    def add_shape_to_list(self, shape_type, vertices):
        shape_name = f"{shape_type} {self.shape_counter}"
        self.shape_counter += 1
        
        self.shapes.append({
            'name': shape_name,
            'type': shape_type,
            'color': self.current_color,
            'vertices': list(vertices)
        })
        self.shape_listbox.insert(tk.END, shape_name)

    def delete_shape(self):
        selection = self.shape_listbox.curselection()
        if selection:
            index = selection[0]
            self.shape_listbox.delete(index)
            del self.shapes[index]
            self.redraw_canvas()

    def clear_canvas(self):
        self.shapes.clear()
        self.current_vertices.clear()
        self.temp_vertices.clear()
        self.shape_listbox.delete(0, tk.END)
        self.shape_counter = 1
        self.redraw_canvas()

    # --- Drawing ---
    def redraw_canvas(self):
        self.canvas.delete("all")
        
        for shape in self.shapes:
            self.draw_tk_shape(shape['vertices'], shape['color'], shape['type'])

        if self.temp_vertices:
            self.draw_tk_shape(self.temp_vertices, self.current_color, self.current_tool)

        if self.current_vertices and self.current_tool == "Polygon":
            for i, (vx, vy) in enumerate(self.current_vertices):
                tx, ty = self.gl_to_tk(vx, vy)
                self.canvas.create_oval(tx-4, ty-4, tx+4, ty+4, fill=self.colors["text"], outline=self.colors["bg"])
                if i > 0:
                    prev_tx, prev_ty = self.gl_to_tk(self.current_vertices[i-1][0], self.current_vertices[i-1][1])
                    self.canvas.create_line(prev_tx, prev_ty, tx, ty, fill=self.colors["text"], width=2, dash=(4,4))

        for i in range(-10, 11):
            val = i / 10.0
            x, _ = self.gl_to_tk(val, 0)
            _, y = self.gl_to_tk(0, val)
            
            color = self.colors["grid"] if i != 0 else self.colors["axis"]
            width = 1 if i != 0 else 2
            dash = (2,4) if i != 0 else None
            
            self.canvas.create_line(x, 0, x, self.canvas_size, fill=color, width=width, dash=dash)
            self.canvas.create_line(0, y, self.canvas_size, y, fill=color, width=width, dash=dash)

    def draw_tk_shape(self, gl_verts, rgb_color, shape_type):
        if not gl_verts: return
        tk_coords = []
        for vx, vy in gl_verts:
            tx, ty = self.gl_to_tk(vx, vy)
            tk_coords.extend([tx, ty])
            
        r, g, b = rgb_color
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        
        if shape_type == "Line":
            self.canvas.create_line(tk_coords, fill=hex_color, width=4)
        else:
            self.canvas.create_polygon(tk_coords, fill=hex_color, outline=self.colors["text"], width=2)

    # --- Code Generation ---
    def generate_code(self):
        code = "#include <GL/glut.h>\n\n"
        code += "void display()\n{\n"
        code += "    glClear(GL_COLOR_BUFFER_BIT);\n\n"
        
        for shape in self.shapes:
            r, g, b = shape['color']
            code += f"    // {shape['name']}\n"
            
            if shape['type'] == 'Line':
                code += "    glBegin(GL_LINES);\n"
            else:
                code += "    glBegin(GL_POLYGON);\n"
                
            code += f"    glColor3ub({r}, {g}, {b});\n"
            for x, y in shape['vertices']:
                code += f"    glVertex2d({x:.2f}, {y:.2f});\n"
            
            code += "    glEnd();\n\n"
            
        code += "    glFlush();\n}\n\n"
        
        code += "int main(int argc, char** argv)\n{\n"
        code += "    glutInit(&argc, argv);\n"
        code += "    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);\n"
        code += "    glutInitWindowSize(600, 600);\n"
        code += "    glutCreateWindow(\"Generated OpenGL Shapes\");\n\n"
        code += "    glClearColor(1.0, 1.0, 1.0, 1.0); // White background\n\n"
        code += "    glutDisplayFunc(display);\n"
        code += "    glutMainLoop();\n"
        code += "    return 0;\n}\n"
        
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, code)

    def copy_code(self):
        code = self.code_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        messagebox.showinfo("Success", "Code copied to clipboard!")

    def save_code(self):
        code = self.code_text.get(1.0, tk.END)
        if len(code.strip()) == 0: return
        file_path = filedialog.asksaveasfilename(defaultextension=".cpp", filetypes=[("C++ Source Files", "*.cpp"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file: file.write(code)
            messagebox.showinfo("Success", f"Code saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenGLShapeGenerator(root)
    root.mainloop()