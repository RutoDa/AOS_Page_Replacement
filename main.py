import os
from tqdm import *
from pagereplacement.to_csv import ToCSV
from pagereplacement.plot import Plotter
from pagereplacement.reference_str import ReferenceStr
from pagereplacement.simulator import Simulator
from pagereplacement.page_replacement_algorithm.fifo import FIFO
from pagereplacement.page_replacement_algorithm.optimal import Optimal
from pagereplacement.page_replacement_algorithm.esc import ESC
from pagereplacement.page_replacement_algorithm.lfu_da import LFU_DA

RESULT_FOLDER = "results"
IMG_FOLDER = os.path.join(RESULT_FOLDER, "figure")
CSV_FOLDER = os.path.join(RESULT_FOLDER, "csv")

if __name__ == "__main__":

    # Generate Random, Locality, and Hybrid Reference Strings and Dirty Bits.
    rs = ReferenceStr()
    # Random Reference String
    rs.generate_reference_str("random")
    random_ref_str = rs.get_reference_str()
    random_dirty_bits = rs.get_dirty_bits()
    # Locality Reference String
    rs.generate_reference_str("locality")
    locality_ref_str = rs.get_reference_str()
    locality_dirty_bits = rs.get_dirty_bits()
    # Hybrid Reference String
    rs.generate_reference_str("hybrid")
    hybrid_ref_str = rs.get_reference_str()
    hybrid_dirty_bits = rs.get_dirty_bits()

    # Run the simulator for the Random, Locality, and Hybrid Reference Strings.
    # Random Reference String
    tqdm.write("-" * 50)
    tqdm.write("Random Reference String:")
    random_sim = Simulator(random_ref_str, random_dirty_bits)
    random_fifo_result = random_sim.run(FIFO)
    random_optimal_result = random_sim.run(Optimal)
    random_esc_result = random_sim.run(ESC)
    random_lfu_da_result = random_sim.run(LFU_DA)

    # Locality Reference String
    tqdm.write("-" * 50)
    tqdm.write("Locality Reference String:")
    locality_sim = Simulator(locality_ref_str, locality_dirty_bits)
    locality_fifo_result = locality_sim.run(FIFO)
    locality_optimal_result = locality_sim.run(Optimal)
    locality_esc_result = locality_sim.run(ESC)
    locality_lfu_da_result = locality_sim.run(LFU_DA)

    # Hybrid Reference String
    tqdm.write("-" * 50)
    tqdm.write("Hybrid Reference String:")
    hybrid_sim = Simulator(hybrid_ref_str, hybrid_dirty_bits)
    hybrid_fifo_result = hybrid_sim.run(FIFO)
    hybrid_optimal_result = hybrid_sim.run(Optimal)
    hybrid_esc_result = hybrid_sim.run(ESC)
    hybrid_lfu_da_result = hybrid_sim.run(LFU_DA)

    # Save the results to CSV files and plot the results.
    # Random Reference String
    ToCSV(
        [
            random_fifo_result,
            random_optimal_result,
            random_esc_result,
            random_lfu_da_result,
        ]
    ).write(
        col_name=["FIFO", "Optiaml", "ESC", "LFU_DA"],
        path=CSV_FOLDER,
        filename="random.csv",
    )
    Plotter(
        [
            random_fifo_result,
            random_optimal_result,
            random_esc_result,
            random_lfu_da_result,
        ]
    ).plot(
        title="Random Reference String",
        algorithm_name=["FIFO", "Optimal", "ESC", "LFU_DA"],
        path=IMG_FOLDER,
        filenames=[
            "random_page_faults.png",
            "random_interrupts.png",
            "random_disk_writes.png",
        ],
    )

    # Locality Reference String
    ToCSV(
        [
            locality_fifo_result,
            locality_optimal_result,
            locality_esc_result,
            locality_lfu_da_result,
        ]
    ).write(
        col_name=["FIFO", "Optiaml", "ESC", "LFU_DA"],
        path=CSV_FOLDER,
        filename="locality.csv",
    )
    Plotter(
        [
            locality_fifo_result,
            locality_optimal_result,
            locality_esc_result,
            locality_lfu_da_result,
        ]
    ).plot(
        title="Locality Reference String",
        algorithm_name=["FIFO", "Optimal", "ESC", "LFU_DA"],
        path=IMG_FOLDER,
        filenames=[
            "locality_page_faults.png",
            "locality_interrupts.png",
            "locality_disk_writes.png",
        ],
    )

    # Hybrid Reference String
    ToCSV(
        [
            hybrid_fifo_result,
            hybrid_optimal_result,
            hybrid_esc_result,
            hybrid_lfu_da_result,
        ]
    ).write(
        col_name=["FIFO", "Optiaml", "ESC", "LFU_DA"],
        path=CSV_FOLDER,
        filename="hybrid.csv",
    )
    Plotter(
        [
            hybrid_fifo_result,
            hybrid_optimal_result,
            hybrid_esc_result,
            hybrid_lfu_da_result,
        ]
    ).plot(
        title="Hybrid Reference String",
        algorithm_name=["FIFO", "Optimal", "ESC", "LFU_DA"],
        path=IMG_FOLDER,
        filenames=[
            "hybrid_page_faults.png",
            "hybrid_interrupts.png",
            "hybrid_disk_writes.png",
        ],
    )

    tqdm.write("-" * 50)
    tqdm.write("All results saved successfully.")
