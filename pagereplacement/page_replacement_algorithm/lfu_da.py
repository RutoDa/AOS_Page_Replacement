from .page_replacement_algorithm import PageReplacementAlgorithm


class Counter:
    """Counter.

    A counter that supports increment and decrement operations.
    """

    def __init__(self):
        self.counter = dict()

    def increment(self, page_num):
        if self.counter.get(page_num, 0):
            self.counter[page_num] += 1
        else:
            self.counter[page_num] = 1

    def decrement(self, page_num, dirty_bit):
        # If the page is dirty, shift the counter to the right by 1 bit.
        if dirty_bit:
            self.counter[page_num] //= 2
        # Otherwise, shift the counter to the right by 2 bits.
        else:
            self.counter[page_num] //= 4

    def get_min(self):
        return min(self.counter, key=self.counter.get)


class MainMemory:
    """Main Memory.

    Main Memory is a set of frames.
    """

    def __init__(self, num_of_frames):
        self.frames = set()
        self.num_of_frames = num_of_frames
        self.dirty = dict()
        self.counter = Counter()

    def is_full(self):
        return len(self.frames) == self.num_of_frames

    def swap_in(self, page_num, dirty_bit):
        self.frames.add(page_num)
        self.dirty[page_num] = dirty_bit
        self.counter.increment(page_num)

    def swap_out(self, page_num):
        is_dirty = True if self.dirty[page_num] == 1 else False
        del self.dirty[page_num]
        self.frames.remove(page_num)
        del self.counter.counter[page_num]
        return is_dirty

    def decrease_count(self):
        # Decrease the counter for each page according to the dirty bit.
        for page_num in self.counter.counter:
            self.counter.decrement(page_num=page_num, dirty_bit=self.dirty[page_num])


class LFU_DA(PageReplacementAlgorithm):
    """Least Frequently Used with Dirty-Aware Aging Algorithm.

    LFU-DA, designed by me, is a page replacement algorithm that replaces the least frequently used page.
    And it uses a counter to keep track of the frequency of use of each page.
    It is different from LFU in that it considers the dirty bit when aging the counter.
    If the page is dirty, the counter is shifted to the right by 1 bit.
    Otherwise, the counter is shifted to the right by 2 bits.
    """

    def __init__(self, reference_str, dirty_bits, max_page_num=1200):
        """Constructor for LFU_DA.

        Args:
            reference_str (list): A list of page numbers.
            dirty_bits (list): A list of dirty bits.
            max_page_num (int, optional): The maximum number of pages. Defaults to 1200.
        """
        super().__init__(reference_str, dirty_bits, max_page_num)

    def find_page_to_replace(self, counter):
        """Find the page to replace.

        Args:
            counter (object): Counter object.

        Returns:
            int: The page number to replace.
        """
        return counter.get_min()

    def compute(self, num_of_frames):
        """Compute the number of page faults, interrupts, and disk writes.

        Args:
            num_of_frames (int): The number of frames in memory.
        """
        super().reset()

        memory = MainMemory(num_of_frames)

        # Simulate the process of page replacement.
        for index, ref_page_num in enumerate(self.reference_str):
            dirty_bit = self.dirty_bits[index]
            # If the page is not in memory, page fault occurs.
            if ref_page_num not in memory.frames:
                self.page_faults += 1
                self.interrupts += 1
                # If the memory is full, replace the page.
                if memory.is_full():
                    victim_page_num = self.find_page_to_replace(memory.counter)
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
                # Increment the counter for the page.
                memory.counter.increment(ref_page_num)

            # Aging the counter.
            if index % 100 == 0:
                # Timmer interrupt.
                self.interrupts += 1
                # Decrease the counter for each page.
                memory.decrease_count()
