from pagereplacement.reference_str import ReferenceStr
from pagereplacement.simulator import Simulator
from pagereplacement.page_replacement_algorithm.fifo import FIFO
from pagereplacement.page_replacement_algorithm.optimal import Optimal
from pagereplacement.page_replacement_algorithm.esc import ESC


if __name__ == '__main__':
    rs = ReferenceStr()
    rs.generate_reference_str('random')
    random_ref_str = rs.get_reference_str()
    random_dirty_bits = rs.get_dirty_bits()
    # random_reference_bits = rs.get_reference_bits()
    
    rs.generate_reference_str('locality')
    locality_ref_str = rs.get_reference_str()
    locality_dirty_bits = rs.get_dirty_bits()
    # locality_reference_bits = rs.get_reference_bits()
    
    random_sim = Simulator(random_ref_str, random_dirty_bits)
    random_sim.run(FIFO)
    random_sim.run(ESC)
    #random_sim.run(Optimal)
    locality_sim = Simulator(locality_ref_str, locality_dirty_bits)
    locality_sim.run(FIFO)
    locality_sim.run(ESC)
    
    
    
    
    # print(random_ref_str, len(random_ref_str), max(random_ref_str), min(random_ref_str))
    # print(locality_ref_str, len(locality_ref_str), max(locality_ref_str), min(locality_ref_str))
    
    # print(random_dirty_bits, len(random_dirty_bits), max(random_dirty_bits), min(random_dirty_bits))
    # print(locality_dirty_bits, len(locality_dirty_bits), max(locality_dirty_bits), min(locality_dirty_bits))    
    # print(random_dirty_bits == locality_dirty_bits)
    
    
    