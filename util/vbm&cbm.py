from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.bandstructure import BandStructure

# 加载 vasprun.xml 文件（可用.gz版本）
path = "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o72/hse06_scf_0_0.32"
vasprun = Vasprun(f"{path}/vasprun.xml", parse_projected_eigen=True)
bandstructure = vasprun.get_band_structure(kpoints_filename=f"{path}/KPOINTS", line_mode=True)

# 获取 VBM 和 CBM 信息
vbm = bandstructure.get_vbm()
cbm = bandstructure.get_cbm()

print("VBM energy (eV):", vbm["energy"])
print("CBM energy (eV):", cbm["energy"])
print("Band gap (eV):", bandstructure.get_band_gap()["energy"])
print("Direct gap?:", bandstructure.get_band_gap()["direct"])
