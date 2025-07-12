import numpy as np
from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from effmass.inputs import DataVasprun, Settings
from effmass.extrema import generate_segments

def format_kpoint(vec, label=None):
    formatted = "[" + ", ".join(f"{v:.3f}" for v in vec) + "]"
    return f"{formatted} ({label})" if label else formatted

def format_vector(vec):
    return "[" + ", ".join(f"{v:.3f}" for v in vec) + "]"

# 加载结构并标准化
structure = Structure.from_file("../POSCAR")
sga = SpacegroupAnalyzer(structure, symprec=0.01)
standard_structure = sga.get_conventional_standard_structure()

# 获取高对称点信息
kpath = HighSymmKpath(standard_structure)
kpoints_dict = kpath.kpath["kpoints"]
tolerance = 1e-2

# 加载 vasprun 数据
data = DataVasprun('PBE_BAND/vasprun.xml')
settings = Settings(
    energy_range=0.5,
    extrema_search_depth=0.05,
    conduction_band=True,
    valence_band=True
)
segments = generate_segments(settings, data)

# 输出标题
print(f"{'起始点':<40} {'终止点':<40} {'方向向量':<15} {'带类型':<15} {'有效质量 (mₑ)':<10}")
print("-" * 135)

# 遍历段
for segment in segments:
    m_eff = segment.finite_difference_effmass()
    start_kpt = segment.kpoints[0]
    end_kpt = segment.kpoints[-1]
    direction = segment.direction

    # 匹配高对称点标签
    start_label = next((lbl for lbl, val in kpoints_dict.items() if np.allclose(start_kpt, val, atol=tolerance)), None)
    end_label = next((lbl for lbl, val in kpoints_dict.items() if np.allclose(end_kpt, val, atol=tolerance)), None)

    # 格式化输出
    start_kpt_str = format_kpoint(start_kpt, start_label)
    end_kpt_str = format_kpoint(end_kpt, end_label)
    direction_str = format_vector(direction)

    print(f"{start_kpt_str:<40} {end_kpt_str:<40} {direction_str:<25} {segment.band_type:<15} {m_eff:<10.3f}")
