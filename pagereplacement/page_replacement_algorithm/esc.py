from .page_replacement_algorithm import PageReplacementAlgorithm


class CircularQueue:
    """Circular Queue for ESC.(Not a true circular queue structure.)"""

    def __init__(self, size):
        self.max_size = size
        self.queue = []
        self.ref_dirty_pair = dict()

    def is_full(self):
        return len(self.queue) == self.max_size

    def push(self, page_num, dirty_bit):
        self.queue.append(page_num)
        self.ref_dirty_pair[page_num] = {"ref_bit": 1, "dirty_bit": dirty_bit}

    def pop(self, page_num):
        is_dirty = True if self.ref_dirty_pair[page_num]["dirty_bit"] == 1 else False
        del self.ref_dirty_pair[page_num]
        self.queue.pop(self.queue.index(page_num))
        return is_dirty


class ESC(PageReplacementAlgorithm):
    """Enhanced Second Chance Algorithm.

    The enhanced second chance algorithm uses reference bit and dirty bit for each page.
    (reference bit, dirty bit) pair:
    1. (0,0): Best page to replace.
    2. (0,1): Need to write the page to disk.
    3. (1,0): Probably it will be used again.
    4. (1,1): Worst page to replace.

    Step:
    (1) Cycle through the buffer looking for (0,0). If one is found, use that page.
    (2) Cycle through the buffer looking for (0,1). Set the reference bit to 0 for all pages bypassed.
    (3) If step 2 faild, all reference bits will now be zero and repetition of step (1) and (2) will find a frame for replacement.
    """

    def __init__(self, reference_str, dirty_bits, max_page_num=1200):
        """Constructor for ESC.

        Args:
            reference_str (list): A list of page numbers.
            dirty_bits (list): A list of dirty bits.
            max_page_num (int, optional): The maximum number of pages. Defaults to 1200.
        """
        super().__init__(reference_str, dirty_bits, max_page_num)

    def find_page_to_replace(self, cqueue):
        """Find the page to replace.

        Args:
            cqueue (object): CircularQueue object.

        Returns:
            int: The page number to replace.
        """
        while True:
            interrupt_cost = 0
            # Step (1) Cycle through the buffer looking for (0,0). If one is found, use that page.
            for page_num in cqueue.queue:
                ref_dirty_pair = cqueue.ref_dirty_pair[page_num]
                if ref_dirty_pair["ref_bit"] == 0 and ref_dirty_pair["dirty_bit"] == 0:
                    victim_page = page_num
                    return victim_page, interrupt_cost

            # Step (2) Cycle through the buffer looking for (0,1). Set the reference bit to 0 for all pages bypassed.
            for page_num in cqueue.queue:
                ref_dirty_pair = cqueue.ref_dirty_pair[page_num]
                if ref_dirty_pair["ref_bit"] == 0 and ref_dirty_pair["dirty_bit"] == 1:
                    victim_page = page_num
                    return victim_page, interrupt_cost
                else:
                    cqueue.ref_dirty_pair[page_num]["ref_bit"] = 0
                    interrupt_cost += 1

    def compute(self, num_of_frames):
        """Compute the number of page faults, interrupts, and disk writes.

        Args:
            num_of_frames (int): The number of frames in memory.
        """
        super().reset()

        cqueue = CircularQueue(size=num_of_frames)

        # Simulate the process of page replacement.
        for index, ref_page_num in enumerate(self.reference_str):
            dirty_bit = self.dirty_bits[index]
            # If the page is not in memory, page fault occurs.
            if ref_page_num not in cqueue.queue:
                self.page_faults += 1
                self.interrupts += 1
                # If the memory is full, replace the page.
                if cqueue.is_full():
                    victim_page_num, interrupt_cost = self.find_page_to_replace(cqueue)
                    self.interrupts += interrupt_cost
                    is_dirty = cqueue.pop(victim_page_num)
                    # If the page is dirty, write it to disk.
                    if is_dirty:
                        self.disk_writes += 1
                        self.interrupts += 1
                # Add the new page to memory.
                cqueue.push(ref_page_num, dirty_bit)
            else:
                # Update the reference bit.
                if dirty_bit != cqueue.ref_dirty_pair[ref_page_num]["dirty_bit"]:
                    cqueue.ref_dirty_pair[ref_page_num]["dirty_bit"] = dirty_bit
