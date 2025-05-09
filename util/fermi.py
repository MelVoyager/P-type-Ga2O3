from pymatgen.io.vasp import Vasprun


path = "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3"
suffix = [
    "Cu_{Ga(I)}", "Cu_{Ga(I)}-N_{O(I)}", "Cu_{Ga(I)}-N_{O(II)}", "Cu_{Ga(I)}-N_{O(III)}", "Cu_{Ga(II)}", "Cu_{Ga(II)}-N_{O(I)}", "Cu_{Ga(II)}-N_{O(II)}", "Cu_{Ga(II)}-N_{O(III)}","Fe_{Ga(I)}", "Fe_{Ga(I)}-N_{O(I)}", "Fe_{Ga(I)}-N_{O(II)}", "Fe_{Ga(I)}-N_{O(III)}", "Fe_{Ga(II)}", "Fe_{Ga(II)}-N_{O(I)}", "Fe_{Ga(II)}-N_{O(II)}", "Fe_{Ga(II)}-N_{O(III)}" 
]

for s in suffix:
    vasprun = Vasprun(f"{path}/{s}/hse06_scf_0_0.32/vasprun.xml")
    fermi_level = vasprun.efermi

    print(f"{s} Fermi level (eV):", fermi_level)
