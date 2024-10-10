from .page_replacement_algorithm import PageReplacementAlgorithm


class Queue:
    """First In First Out Queue.

    A simple queue that supports FIFO operations.
    """

    def __init__(self, max_size):
        self.items = []
        self.max_size = max_size
        self.dirty = dict()

    def is_full(self):
        return len(self.items) == self.max_size

    def push(self, item, dirty_bit):
        self.items.append(item)
        self.dirty[item] = dirty_bit

    def pop(self):
        is_dirty = True if self.dirty[self.items[0]] == 1 else False
        del self.dirty[self.items[0]]
        return self.items.pop(0), is_dirty

    def size(self):
        return len(self.items)


class FIFO(PageReplacementAlgorithm):
    """First In First Out Page Replacement Algorithm.

    FIFO is a simple page replacement algorithm that replaces the oldest page in memory.
    """

    def __init__(self, reference_str, dirty_bits, max_page_num=1200):
        """Constructor for FIFO.

        Args:
            reference_str (list): A list of page numbers.
            dirty_bits (list): A list of dirty bits.
            max_page_num (int, optional): The maximum number of pages. Defaults to 1200.
        """
        super().__init__(reference_str, dirty_bits, max_page_num)

    def compute(self, num_of_frames):
        """Compute the number of page faults, interrupts, and disk writes.

        Args:
            num_of_frames (int): The number of frames in memory.
        """
        super().reset()

        queue = Queue(max_size=num_of_frames)

        # Simulate the process of page replacement.
        for index, ref_page_num in enumerate(self.reference_str):
            dirty_bit = self.dirty_bits[index]
            # If the page is not in memory, page fault occurs.
            if ref_page_num not in queue.items:
                self.page_faults += 1
                self.interrupts += 1
                # If the memory is full, replace the oldest page.
                if queue.is_full():
                    _, is_dirty = queue.pop()
                    # If the page is dirty, write it to disk.
                    if is_dirty:
                        self.disk_writes += 1
                        self.interrupts += 1
                # Add the new page to memory.
                queue.push(ref_page_num, dirty_bit)
            else:
                # Update the dirty bit of the page.
                if dirty_bit != queue.dirty[ref_page_num]:
                    queue.dirty[ref_page_num] = dirty_bit
