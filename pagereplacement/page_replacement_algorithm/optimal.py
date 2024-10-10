from .page_replacement_algorithm import PageReplacementAlgorithm


class MainMemory:
    """Main Memory.

    Main Memory is a set of frames.
    """

    def __init__(self, num_of_frames):
        self.frames = set()
        self.num_of_frames = num_of_frames
        self.dirty = dict()

    def is_full(self):
        return len(self.frames) == self.num_of_frames

    def swap_in(self, page_num, dirty_bit):
        self.frames.add(page_num)
        self.dirty[page_num] = dirty_bit

    def swap_out(self, page_num):
        is_dirty = True if self.dirty[page_num] == 1 else False
        del self.dirty[page_num]
        self.frames.remove(page_num)
        return is_dirty


class Optimal(PageReplacementAlgorithm):
    """Optimal Page Replacement Algorithm.

    Optimal is a page replacement algorithm that replaces the page that will not be used for the longest period.
    """

    def __init__(self, reference_str, dirty_bits, max_page_num=1200):
        """Constructor for Optimal.

        Args:
            reference_str (list): A list of page numbers.
            dirty_bits (list): A list of dirty bits.
            max_page_num (int, optional): The maximum number of pages. Defaults to 1200.
        """
        super().__init__(reference_str, dirty_bits, max_page_num)

    def find_page_to_replace(self, current_index, frames):
        """Find the page to replace.

        Args:
            current_index (int): The current index of the reference string.
            frames (set): The set of page numbers in memory.

        Returns:
            int: The page number to replace.
        """
        # Get the reference string from the current index.
        ref_str = self.reference_str[current_index + 1 :]
        # Record each page_num in memory and the time it is next referenced.
        next_reference_time = dict()
        # Find the page to replace.
        for page_num in frames:
            if page_num not in ref_str:
                # Return the page_num that are no longer referenced.
                return page_num
            else:
                next_reference_time[page_num] = ref_str.index(page_num)
        # Or return the page_num that will not be used for the longest period.
        return max(next_reference_time, key=lambda key: next_reference_time[key])

    def compute(self, num_of_frames):
        """Compute the number of page faults, interrupts, and disk writes.

        Args:
            num_of_frames (int): The number of frames in memory.
        """
        super().reset()

        memory = MainMemory(num_of_frames=num_of_frames)

        # Simulate the process of page replacement.
        for index, ref_page_num in enumerate(self.reference_str):
            dirty_bit = self.dirty_bits[index]
            # If the page is not in memory, page fault occurs.
            if ref_page_num not in memory.frames:
                self.page_faults += 1
                self.interrupts += 1
                # If the memory is full, replace the page.
                if memory.is_full():
                    victim_page_num = self.find_page_to_replace(index, memory.frames)
                    is_dirty = memory.swap_out(victim_page_num)
                    # If the page is dirty, write it to disk.
                    if is_dirty:
                        self.disk_writes += 1
                        self.interrupts += 1
                # Add the new page to memory.
                memory.swap_in(ref_page_num, dirty_bit)
            else:
                # Update the dirty bit.
                if dirty_bit != memory.dirty[ref_page_num]:
                    memory.dirty[ref_page_num] = dirty_bit
