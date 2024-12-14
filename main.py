import tkinter as tk


class MemoryBlock:
    def __init__(self, size):
        self.size = size
        self.allocated = False

    def __str__(self):
        status = "Allocated" if self.allocated else "Free"
        return f"Block(size={self.size}, {status})"


class BestFitMemoryManager:
    def __init__(self, total_memory_size):
        self.memory_blocks = [MemoryBlock(total_memory_size)]

    def allocate(self, request_size):
        best_fit_index = None
        min_size_difference = float('inf')

        for i, block in enumerate(self.memory_blocks):
            if not block.allocated and block.size >= request_size:
                size_difference = block.size - request_size
                if size_difference < min_size_difference:
                    min_size_difference = size_difference
                    best_fit_index = i

        if best_fit_index is not None:
            best_fit_block = self.memory_blocks[best_fit_index]
            if best_fit_block.size > request_size:
                remaining_size = best_fit_block.size - request_size
                self.memory_blocks.insert(best_fit_index + 1, MemoryBlock(remaining_size))
            best_fit_block.size = request_size
            best_fit_block.allocated = True
        else:
            return "No suitable block found for allocation of size " + str(request_size)

    def deallocate(self, request_size):
        for i, block in enumerate(self.memory_blocks):
            if block.size == request_size and block.allocated:
                block.allocated = False
                self.merge_free_blocks()
                return
        return "No allocated block of size " + str(request_size) + " found to deallocate."

    def merge_free_blocks(self):
        i = 0
        while i < len(self.memory_blocks) - 1:
            current_block = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]

            if not current_block.allocated and not next_block.allocated:
                current_block.size += next_block.size
                self.memory_blocks.pop(i + 1)
            else:
                i += 1

    def display_memory(self):
        memory_state = []
        for block in self.memory_blocks:
            memory_state.append(str(block))
        return memory_state


class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Best Fit Memory Management")

        self.memory_manager = BestFitMemoryManager(1000)

        self.create_widgets()
        self.update_memory_display()

    def create_widgets(self):
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=5)

        self.allocate_label = tk.Label(frame1, text="Allocate Memory Size (KB):")
        self.allocate_label.pack(side="left", padx=5)

        self.allocate_entry = tk.Entry(frame1)
        self.allocate_entry.pack(side="left", padx=5)

        self.allocate_button = tk.Button(frame1, text="Allocate", command=self.allocate_memory)
        self.allocate_button.pack(side="left", padx=5)

        frame2 = tk.Frame(self.root)
        frame2.pack(pady=5)

        self.deallocate_label = tk.Label(frame2, text="Deallocate Memory Size (KB):")
        self.deallocate_label.pack(side="left", padx=5)

        self.deallocate_entry = tk.Entry(frame2)
        self.deallocate_entry.pack(side="left", padx=5)

        self.deallocate_button = tk.Button(frame2, text="Deallocate", command=self.deallocate_memory)
        self.deallocate_button.pack(side="left", padx=5)

        self.canvas = tk.Canvas(self.root, width=1000, height=55, bg="white")
        self.canvas.pack(pady=(0, 5))

        self.error_display = tk.Label(self.root, text="", fg="red")
        self.error_display.pack(pady=(0, 5))

        for widget in [frame1, frame2, self.canvas, self.error_display]:
            widget.pack_configure(anchor="center")

    def allocate_memory(self):
        try:
            size = int(self.allocate_entry.get())
            error_message = self.memory_manager.allocate(size)
            if error_message:
                self.error_display.config(text=error_message)
            else:
                self.error_display.config(text="")
            self.update_memory_display()
        except ValueError:
            self.error_display.config(text="Invalid size entered for allocation.")

    def deallocate_memory(self):
        try:
            size = int(self.deallocate_entry.get())
            error_message = self.memory_manager.deallocate(size)
            if error_message:
                self.error_display.config(text=error_message)
            else:
                self.error_display.config(text="")
            self.update_memory_display()
        except ValueError:
            self.error_display.config(text="Invalid size entered for deallocation.")

    def update_memory_display(self):
        self.canvas.delete("all")
        total_width = 1000
        total_memory = sum(block.size for block in self.memory_manager.memory_blocks)
        x = 0
        y_offset = 5
        height = 50

        for block in self.memory_manager.memory_blocks:
            block_width = (block.size / total_memory) * total_width
            color = "green" if block.allocated else "lightgrey"
            self.canvas.create_rectangle(x, y_offset, x + block_width - 1, y_offset + height, fill=color, outline="")
            self.canvas.create_text(x + block_width / 2, y_offset + height / 2, text=f"{block.size} KB", fill="black")
            x += block_width


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()
