import tkinter as tk
import time


# Represents a memory block with a specific size and allocation status
class MemoryBlock:
    def __init__(self, size):
        # Size of the memory block in KB
        self.size = size
        # Flag to indicate if the block is currently allocated
        self.allocated = False

    def __str__(self):
        # String representation of the memory block
        status = "Allocated" if self.allocated else "Free"
        return f"Block(size={self.size}, {status})"


# Implements Best Fit memory allocation strategy
class BestFitMemoryManager:
    def __init__(self, total_memory_size):
        # Initialize with a single memory block of total memory size
        self.memory_blocks = [MemoryBlock(total_memory_size)]

    def allocate(self, request_size):
        """
        Allocate memory using Best Fit strategy

        Args:
            request_size (int): Size of memory to allocate in KB

        Returns:
            int or None: Index of allocated block, or None if allocation fails
        """
        best_fit_index = None
        # Track the smallest difference between block size and request size
        min_size_difference = float('inf')

        # Find the best fitting block
        for i, block in enumerate(self.memory_blocks):
            # Check if block is free and large enough
            if not block.allocated and block.size >= request_size:
                # Calculate size difference
                size_difference = block.size - request_size
                # Update best fit if current block is closer to request size
                if size_difference < min_size_difference:
                    min_size_difference = size_difference
                    best_fit_index = i

        # Perform allocation if suitable block found
        if best_fit_index is not None:
            best_fit_block = self.memory_blocks[best_fit_index]

            # Split block if it's larger than requested size
            if best_fit_block.size > request_size:
                remaining_size = best_fit_block.size - request_size
                # Insert remaining free block after the allocated block
                self.memory_blocks.insert(best_fit_index + 1, MemoryBlock(remaining_size))

            # Resize and mark block as allocated
            best_fit_block.size = request_size
            best_fit_block.allocated = True
            return best_fit_index
        else:
            return None

    def deallocate(self, request_size):
        """
        Deallocate a memory block of specified size

        Args:
            request_size (int): Size of memory to deallocate in KB

        Returns:
            int or None: Index of deallocated block, or None if deallocation fails
        """
        # Find and deallocate the block
        for i, block in enumerate(self.memory_blocks):
            if block.size == request_size and block.allocated:
                block.allocated = False
                # Merge adjacent free blocks
                self.merge_free_blocks()
                return i
        return None

    def merge_free_blocks(self):
        """
        Merge adjacent free memory blocks to reduce fragmentation
        """
        i = 0
        while i < len(self.memory_blocks) - 1:
            current_block = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]

            # Merge two consecutive free blocks
            if not current_block.allocated and not next_block.allocated:
                current_block.size += next_block.size
                # Remove the second block after merging
                self.memory_blocks.pop(i + 1)
            else:
                i += 1

    def display_memory(self):
        """
        Generate a string representation of current memory state

        Returns:
            list: List of string representations of memory blocks
        """
        return [str(block) for block in self.memory_blocks]


class MemoryManagerGUI:
    def __init__(self, root):
        """
        Initialize the Memory Manager GUI

        Args:
            root (tk.Tk): Main Tkinter window
        """
        self.root = root
        self.root.title("Best Fit Memory Management")

        # Initialize memory manager with 1000 KB total memory
        self.memory_manager = BestFitMemoryManager(1000)

        # Create GUI widgets and initial display
        self.create_widgets()
        self.update_memory_display()

    def create_widgets(self):
        """
        Create and layout GUI widgets for memory allocation and deallocation
        """
        # Allocation frame
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=5)

        self.allocate_label = tk.Label(frame1, text="Allocate Memory Size (KB):")
        self.allocate_label.pack(side="left", padx=5)

        self.allocate_entry = tk.Entry(frame1)
        self.allocate_entry.pack(side="left", padx=5)

        self.allocate_button = tk.Button(frame1, text="Allocate", command=self.allocate_memory)
        self.allocate_button.pack(side="left", padx=5)

        # Deallocation frame
        frame2 = tk.Frame(self.root)
        frame2.pack(pady=5)

        self.deallocate_label = tk.Label(frame2, text="Deallocate Memory Size (KB):")
        self.deallocate_label.pack(side="left", padx=5)

        self.deallocate_entry = tk.Entry(frame2)
        self.deallocate_entry.pack(side="left", padx=5)

        self.deallocate_button = tk.Button(frame2, text="Deallocate", command=self.deallocate_memory)
        self.deallocate_button.pack(side="left", padx=5)

        # Memory visualization canvas
        self.canvas = tk.Canvas(self.root, width=1000, height=55, bg="white")
        self.canvas.pack(pady=(20, 5))

        # Error message display
        self.error_display = tk.Label(self.root, text="", fg="red")
        self.error_display.pack(pady=(0, 5))

        # Center align widgets
        for widget in [frame1, frame2, self.canvas, self.error_display]:
            widget.pack_configure(anchor="center")

    def animate_allocation(self, block_index):
        """
        Animate the allocation of a memory block

        Args:
            block_index (int): Index of the block being allocated
        """
        total_width = 1000
        total_memory = sum(b.size for b in self.memory_manager.memory_blocks)

        # Calculate starting x position of the block
        x = sum((b.size / total_memory) * total_width for b in self.memory_manager.memory_blocks[:block_index])

        # Color transition animation
        start_color = "lightgrey"
        end_color = "green"

        # Smooth color transition over 21 steps
        for i in range(21):
            ratio = i / 20
            r_start, g_start, b_start = self.get_rgb_from_color(start_color)
            r_end, g_end, b_end = self.get_rgb_from_color(end_color)

            # Interpolate RGB values
            r = int(r_start + (r_end - r_start) * ratio)
            g = int(g_start + (g_end - g_start) * ratio)
            b = int(b_start + (b_end - b_start) * ratio)

            # Convert to hex color
            intermediate_color = f'#{r:02x}{g:02x}{b:02x}'

            # Redraw entire canvas with transitioning color
            self.canvas.delete("all")
            x_pos = 0
            for j, block in enumerate(self.memory_manager.memory_blocks):
                block_curr_width = (block.size / total_memory) * total_width
                # Apply color transition to specific block
                block_color = (
                    intermediate_color if j == block_index and i < 20
                    else ("green" if block.allocated else "lightgrey")
                )

                # Draw block rectangle
                self.canvas.create_rectangle(
                    x_pos, 5, x_pos + block_curr_width - 1, 55,
                    fill=block_color, outline=""
                )
                # Add size label
                self.canvas.create_text(
                    x_pos + block_curr_width / 2, 30,
                    text=f"{block.size} KB", fill="black"
                )
                x_pos += block_curr_width

            # Update display and pause
            self.root.update()
            time.sleep(0.05)

    def animate_deallocation(self, block_index):
        """
        Animate the deallocation of a memory block

        Args:
            block_index (int): Index of the block being deallocated
        """
        total_width = 1000
        total_memory = sum(b.size for b in self.memory_manager.memory_blocks)

        # Color transition animation
        start_color = "green"
        end_color = "lightgrey"

        # Smooth color transition over 21 steps
        for i in range(21):
            ratio = i / 20
            r_start, g_start, b_start = self.get_rgb_from_color(start_color)
            r_end, g_end, b_end = self.get_rgb_from_color(end_color)

            # Interpolate RGB values
            r = int(r_start + (r_end - r_start) * ratio)
            g = int(g_start + (g_end - g_start) * ratio)
            b = int(b_start + (b_end - b_start) * ratio)

            # Convert to hex color
            intermediate_color = f'#{r:02x}{g:02x}{b:02x}'

            # Redraw entire canvas with transitioning color
            self.canvas.delete("all")
            x_pos = 0
            for j, block in enumerate(self.memory_manager.memory_blocks):
                block_curr_width = (block.size / total_memory) * total_width
                # Apply color transition to specific block
                block_color = (
                    intermediate_color if j == block_index and i < 20
                    else ("green" if block.allocated else "lightgrey")
                )

                # Draw block rectangle
                self.canvas.create_rectangle(
                    x_pos, 5, x_pos + block_curr_width - 1, 55,
                    fill=block_color, outline=""
                )
                # Add size label
                self.canvas.create_text(
                    x_pos + block_curr_width / 2, 30,
                    text=f"{block.size} KB", fill="black"
                )
                x_pos += block_curr_width

            # Update display and pause
            self.root.update()
            time.sleep(0.05)

        # Update display after deallocation
        self.update_memory_display()

    def get_rgb_from_color(self, color):
        """
        Convert color names to RGB values

        Args:
            color (str): Color name

        Returns:
            tuple: RGB values for the given color
        """
        # Mapping of color names to RGB values
        color_map = {
            "lightgrey": (211, 211, 211),
            "green": (0, 128, 0)
        }
        return color_map.get(color, (0, 0, 0))

    def allocate_memory(self):
        """
        Handle memory allocation from user input
        """
        try:
            # Get allocation size from entry
            size = int(self.allocate_entry.get())

            # Attempt to allocate memory
            block_index = self.memory_manager.allocate(size)

            if block_index is not None:
                # Clear any previous error messages
                self.error_display.config(text="")
                # Animate the allocation
                self.animate_allocation(block_index)
            else:
                # Display error if allocation fails
                self.error_display.config(text=f"No suitable block found for allocation of size {size}")
        except ValueError:
            # Handle invalid input
            self.error_display.config(text="Invalid size entered for allocation.")

    def deallocate_memory(self):
        """
        Handle memory deallocation from user input
        """
        try:
            # Get deallocation size from entry
            size = int(self.deallocate_entry.get())

            # Attempt to deallocate memory
            block_index = self.memory_manager.deallocate(size)

            if block_index is not None:
                # Clear any previous error messages
                self.error_display.config(text="")
                # Animate the deallocation
                self.animate_deallocation(block_index)
            else:
                # Display error if deallocation fails
                self.error_display.config(text=f"No allocated block of size {size} found to deallocate.")
        except ValueError:
            # Handle invalid input
            self.error_display.config(text="Invalid size entered for deallocation.")

    def update_memory_display(self):
        """
        Update the visual representation of memory blocks
        """
        # Clear previous canvas content
        self.canvas.delete("all")

        total_width = 1000
        total_memory = sum(block.size for block in self.memory_manager.memory_blocks)
        x = 0
        y_offset = 5
        height = 50

        # Draw each memory block
        for block in self.memory_manager.memory_blocks:
            # Calculate block width proportional to its size
            block_width = (block.size / total_memory) * total_width

            # Determine block color based on allocation status
            color = "green" if block.allocated else "lightgrey"

            # Draw block rectangle
            self.canvas.create_rectangle(
                x, y_offset, x + block_width - 1, y_offset + height,
                fill=color, outline=""
            )
            # Add size label
            self.canvas.create_text(
                x + block_width / 2, y_offset + height / 2,
                text=f"{block.size} KB", fill="black"
            )
            x += block_width


if __name__ == "__main__":
    # Create main application window
    root = tk.Tk()
    # Initialize Memory Manager GUI
    app = MemoryManagerGUI(root)
    # Start the main event loop
    root.mainloop()