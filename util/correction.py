import os
os.environ["PMG_VASP_PSP_DIR"] = "/home/bingxing2/ailab/xiazeyu_p/Programs/POTCAR"

from pathlib import Path
from doped.analysis import DefectsParser

# 基础参数
dielectric = 9.9
base_dir = "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3"
bulk_path = "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o72/hse06_scf_0_0.32"

# 收集目标文件夹
target_folders = [
    '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga47_1o71p_1/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71n_2/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71n_3/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71n_1/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71n_2/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71n_3/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71p_1/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71p_2/hse06_scf_-1_0.32',
    # '/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga48o71p_3/hse06_scf_-1_0.32'
                  ]
# for root, dirs, _ in os.walk(base_dir):
#     for dir_name in dirs:
#         if "hse06" in dir_name and "0.32" in dir_name and "ga48o72" not in root:
#             target_folders.append(os.path.join(root, dir_name))

# 将所有输出写入 correction.txt
with open("correction.txt", "w") as f:
    for output_path in target_folders:
        # 写入分隔线和当前处理的目录
        print(f"\n{'='*50}\nProcessing: {output_path}\n{'='*50}\n")
        f.write(f"\n{'='*50}\nProcessing: {output_path}\n{'='*50}\n")
        f.flush()  # 确保实时写入
        
        try:
            dp = DefectsParser(
                output_path=output_path,
                dielectric=dielectric,
                bulk_path=bulk_path,
                processes=1
            )
            
            # 遍历缺陷条目并写入文件
            for name, defect_entry in dp.defect_dict.items():
                f.write(f"name: {name}\n")
                f.write(f"defect: {defect_entry.defect}\n\n")
                
                if defect_entry.charge_state != 0:
                    correction = list(defect_entry.corrections.values())[0]
                    f.write(f"Charge = {defect_entry.charge_state:+} with correction: {correction:+.5f} eV\n\n")
                
                f.write(f"Supercell site: {defect_entry.defect_supercell_site.frac_coords.round(3)}\n\n")
                f.write(f"Corrected energy: {defect_entry.corrected_energy:+.5f}\n\n")
                f.flush()
                
        except Exception as e:
            # 错误信息也写入文件
            f.write(f"Error processing {output_path}: {str(e)}\n")
            f.flush()
            continue