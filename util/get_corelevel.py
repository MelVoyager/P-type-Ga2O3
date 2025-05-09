import re

def extract_1s_energies(file_path):
    energies = []

    with open(file_path, 'r') as f:
        for line in f:
            # 使用正则表达式提取形如 '1s   -xxxx.xxxx' 的数据
            match = re.search(r'1s\s+(-?\d+\.\d+)', line)
            if match:
                energy = float(match.group(1))
                energies.append(energy)

    return energies

path = "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3"
suffix = [
    "Cu_{Ga(I)}"
    # , "Cu_{Ga(I)}-N_{O(I)}", "Cu_{Ga(I)}-N_{O(II)}", "Cu_{Ga(I)}-N_{O(III)}", "Cu_{Ga(II)}", "Cu_{Ga(II)}-N_{O(I)}", "Cu_{Ga(II)}-N_{O(II)}", "Cu_{Ga(II)}-N_{O(III)}","Fe_{Ga(I)}", "Fe_{Ga(I)}-N_{O(I)}", "Fe_{Ga(I)}-N_{O(II)}", "Fe_{Ga(I)}-N_{O(III)}", "Fe_{Ga(II)}", "Fe_{Ga(II)}-N_{O(I)}", "Fe_{Ga(II)}-N_{O(II)}", "Fe_{Ga(II)}-N_{O(III)}" 
]

bulk_reference = extract_1s_energies("/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o72/hse06_scf_0_0.32_new/OUTCAR")

for s in suffix:
    core_1s_energies = extract_1s_energies(f"{path}/{s}/hse06_scf_0_0.32/OUTCAR")
    subtract = [x - y for x, y in zip(bulk_reference, core_1s_energies)]
    print(subtract)
# 打印前10个能级作为示例
# for i, energy in enumerate(core_1s_energies, 1):
#     print(f'{i:3d}: 1s = {energy:.4f}')
