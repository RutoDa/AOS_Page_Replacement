import pandas as pd
from tqdm import *


class Simulator:
    """Simulator class to run the page replacement algorithms."""

    def __init__(self, reference_str, dirty_bits):
        """Constructor for Simulator.

        Args:
            reference_str (list): A list of page numbers.
            dirty_bits (list): A list of dirty bits.
        """
        self.reference_str = reference_str
        self.dirty_bits = dirty_bits

    def run(self, algorithm, max_frame_count=100, interval=10, max_page_num=1200):
        """Run the page replacement algorithm.

        Args:
            algorithm (class): The page replacement algorithm class.
            max_frame_count (int, optional): Maximum number of frames. Defaults to 100.
            interval (int, optional): Interval between frame counts. Defaults to 10.
            max_page_num (int, optional): Maximum number of pages. Defaults to 1200.

        Returns:
            DataFrame: A pandas DataFrame containing the results.
        """

        evaluator = algorithm(
            reference_str=self.reference_str,
            dirty_bits=self.dirty_bits,
            max_page_num=max_page_num,
        )

        frame_counts = []
        page_faults = []
        interrupts = []
        disk_writes = []

        # Run the algorithm for different frame counts.
        tqdm.write(f"Running {algorithm.__name__} algorithm...")
        for frame_count in tqdm(range(10, max_frame_count + 1, interval)):
            evaluator.compute(num_of_frames=frame_count)
            # Get the results.
            result = evaluator.get_results()
            frame_counts.append(frame_count)
            page_faults.append(result["page_faults"])
            interrupts.append(result["interrupts"])
            disk_writes.append(result["disk_writes"])

        data = {
            "Frame Count": frame_counts,
            "Page Faults": page_faults,
            "Interrupts": interrupts,
            "Disk Writes": disk_writes,
        }
        df = pd.DataFrame.from_dict(data).set_index("Frame Count")
        # print(df)
        return df
