import os
from tqdm import * 
from pagereplacement.to_csv import ToCSV
from pagereplacement.plot import Plotter
from pagereplacement.reference_str import ReferenceStr
from pagereplacement.simulator import Simulator
from pagereplacement.page_replacement_algorithm.fifo import FIFO
from pagereplacement.page_replacement_algorithm.optimal import Optimal
from pagereplacement.page_replacement_algorithm.esc import ESC

RESULT_FOLDER = "results"
IMG_FOLDER = os.path.join(RESULT_FOLDER, "figure")
CSV_FOLDER = os.path.join(RESULT_FOLDER, "csv")

if __name__ == "__main__":
    rs = ReferenceStr()
    rs.generate_reference_str("random")
    random_ref_str = rs.get_reference_str()
    random_dirty_bits = rs.get_dirty_bits()

    rs.generate_reference_str("locality")
    locality_ref_str = rs.get_reference_str()
    locality_dirty_bits = rs.get_dirty_bits()

    tqdm.write('-'*50)
    tqdm.write("Random Reference String:")
    random_sim = Simulator(random_ref_str, random_dirty_bits)
    random_fifo_result = random_sim.run(FIFO)
    random_optimal_result = random_sim.run(Optimal)
    #random_optimal_result = random_sim.run(FIFO)
    random_esc_result = random_sim.run(ESC)

    ToCSV([random_fifo_result, random_optimal_result, random_esc_result]).write(
        col_name= ['FIFO','Optiaml','ESC'],
        path=CSV_FOLDER, 
        filename="random.csv", 
    )
    
    Plotter([random_fifo_result, random_optimal_result, random_esc_result]).plot(
        title="Random Reference String",
        algorithm_name=['FIFO','Optimal','ESC'],
        path=IMG_FOLDER,
        filenames=["random_page_faults.png", "random_interrupts.png", "random_disk_writes.png"],
    )


    
