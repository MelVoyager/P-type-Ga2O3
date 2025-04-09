from spinney.structures.pointdefect import PointDefect
import ase.io
from spinney.io.vasp import extract_potential_at_core_vasp

# DEFECT_PATH = '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga47_1o71p_1/hse06_scf_-1_0.32/OUTCAR'
DEFECT_PATH = '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71n_1/hse06_scf_-1_0.32/OUTCAR'
REF_PATH = '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o72/hse06_scf_0_0.32/OUTCAR'
# use ASE to read the OUTCAR file of the defective system
outcar = ase.io.read(DEFECT_PATH, format='vasp-out')
# initialize a Spinney PointDefect object
pd = PointDefect(outcar)

ase_pristine = ase.io.read(REF_PATH, format='vasp-out')
pd.set_pristine_system(ase_pristine)

q = -1
def_position = ( -0.0007939989134090,  0.1666666666666643,  0.3697145032265322)
# def_position =  (-0.0487949788618904,  0.1666666666666643,  0.3738801813083105)
vbm = 1.5457
e_r = [[10.2, 0, -0.1399],[0, 10.21, 0],[-0.1399, 0, 13.12]]
chem_pot_O = -7.88246
chem_pot_Ga = -8.14132
chem_pot_P = -5.36
correction_type = 'ko'
gap_range_0 = 0 + vbm
gap_range_1 = 4.5 + vbm
    
chemical_potentials = {'O': chem_pot_O, 'Ga': chem_pot_Ga, 'P':chem_pot_P}

pd.set_chemical_potential_values(chemical_potentials)
pd.set_vbm(vbm)
pd.set_fermi_level_value_from_vbm(0)
pd.set_defect_charge(q)
pd.set_defect_position(def_position)
pd.set_dielectric_tensor(e_r)

pd.set_finite_size_correction_scheme('ko')


potential_pristine = extract_potential_at_core_vasp(DEFECT_PATH)
potential_defective = extract_potential_at_core_vasp(REF_PATH)
pd.add_correction_scheme_data(potential_pristine=potential_pristine,
                              potential_defective=potential_defective)

# energy without adding corrections for electrostatic finite-size effects
uncorrected_energy = pd.get_defect_formation_energy()
# corrected energy
corrected_energy = pd.get_defect_formation_energy(True)

print(f'uncorrected:{uncorrected_energy}')
print(f'corrected:{corrected_energy}')
print(f'correction:{corrected_energy - uncorrected_energy}')