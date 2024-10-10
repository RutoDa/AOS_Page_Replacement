class PageReplacementAlgorithm:
    """Page Replacement Algorithm.

    A base class for page replacement algorithms.
    """

    def __init__(self, reference_str, dirty_bits, max_page_num=1200):
        """Constructor.

        Args:
            reference_str (list): A list of page numbers.
            dirty_bits (list): A list of dirty bits.
            max_page_num (int, optional): The maximum number of pages. Defaults to 1200.
        """
        self.reference_str = reference_str
        self.dirty_bits = dirty_bits
        self.page_faults = 0
        self.interrupts = 0
        self.disk_writes = 0
        self.max_page_num = max_page_num

    def reset(self):
        """Reset the counters.
        """
        self.page_faults = 0
        self.interrupts = 0
        self.disk_writes = 0

    def get_results(self):
        """Get the results.

        Returns:
            dict: A dictionary containing the page faults, interrupts, and disk writes.
        """
        return {
            "page_faults": self.page_faults,
            "interrupts": self.interrupts,
            "disk_writes": self.disk_writes,
        }
