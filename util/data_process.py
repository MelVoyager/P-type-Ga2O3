from pymatgen.io.vasp.outputs import Oszicar, Outcar, Locpot
from pymatgen.core import Structure
import os

from post_process import Post_process

# Define parameters
vbm = 1.5457
e_r = [[10.2, 0, -0.1399],[0, 10.21, 0],[-0.1399, 0, 13.12]]
chem_pot_O = -7.88246
chem_pot_Ga = -8.14132
chem_pot_P = -5.36
chem_pot_N = -1.10773E+01
correction_type = 'ko'
gap_range_0 = 0 + vbm
gap_range_1 = 4.5 + vbm
    
chemical_potentials = {'O': chem_pot_O, 'Ga': chem_pot_Ga, 'N':chem_pot_N}

# post_dir = os.path.join("calc_new", "Gallium_Oxide")
post_dir = '/home/bingxing2/ailab/xiazeyu_p/Programs/post'
postprocess = Post_process(post_dir)
postprocess.calculate_formation_energy_system(post_dir, correction_type, True, vbm, e_r, chemical_potentials)

# Calculate transition levels
postprocess.calculate_transition_level_system(post_dir, correction_type, True, vbm, e_r, chemical_potentials, (gap_range_0, gap_range_1))
print("Post process completed!")


