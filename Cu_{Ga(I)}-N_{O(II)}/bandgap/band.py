import os
os.environ["PMG_VASP_PSP_DIR"] = "/home/bingxing2/ailab/xiazeyu_p/Programs/POTCAR"
import shutil
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPStaticSet, MPNonSCFSet
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter
import matplotlib.pyplot as plt

# 设置 POTCAR 路径
  # 修改为你的路径

# 读取结构
structure = Structure.from_file("../POSCAR")

# ========== 1. 生成 SCF 输入 ==========
scf_dir = "PBE_SCF"
scf_set = MPStaticSet(structure)
scf_set.write_input(scf_dir)
print(f"[✓] SCF 输入已写入：{scf_dir}/")

# ========== 2. 生成 NSCF 输入（高对称路径） ==========
band_dir = "PBE_BAND"
kpath = HighSymmKpath(structure)
nscf_incar = {
    "ICHARG": 11,
    "ISMEAR": 0,
    "SIGMA": 0.05,
    "LWAVE": True,
    "LCHARG": False
}
band_set = MPNonSCFSet(
    structure,
    mode="line",
    kpoints_line_density=20,
    user_incar_settings=nscf_incar
)
band_set.write_input(band_dir)
print(f"[✓] BAND 输入已写入：{band_dir}/")

# ========== 3. 拷贝 CHGCAR ==========
src_chgcar = os.path.join(scf_dir, "CHGCAR")
dst_chgcar = os.path.join(band_dir, "CHGCAR")

if os.path.exists(src_chgcar):
    shutil.copy(src_chgcar, dst_chgcar)
    print(f"[✓] CHGCAR 拷贝成功：{dst_chgcar}")
else:
    print(f"[!] 未找到 CHGCAR，请先运行 SCF 计算后再运行 BAND。")

# ========== 4. 可选：分析结果 ==========
vasprun_path = os.path.join(band_dir, "vasprun.xml")
if os.path.exists(vasprun_path):

  # 读取 vasprun
    vasprun = Vasprun("PBE_BAND/vasprun.xml", parse_projected_eigen=False)
    bs = vasprun.get_band_structure(line_mode=True)

    plotter = BSPlotter(bs)
    ax = plotter.get_plot()
    plt.tight_layout()
    plt.show()
    plt.savefig('band.png')
else:
    print("[!] 还未生成 vasprun.xml，跳过能带图绘制。")
