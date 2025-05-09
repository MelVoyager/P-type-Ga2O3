import os
import shutil

# 设置原始目录 a 和目标目录 b
a = "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3"
b = "/home/bingxing2/ailab/xiazeyu_p/Programs/trash/5.9"

# 要匹配的目标文件夹名
target_dirs = {"hse06_scf_-1_0.32", "hse06_scf_0_0.32", "str_opt_-1", "str_opt_0"}

# 遍历目录 a
for root, dirs, files in os.walk(a):
    for d in dirs:
        if d in target_dirs:
            full_src_path = os.path.join(root, d)
            rel_path = os.path.relpath(full_src_path, a)  # 获取相对路径
            full_dst_path = os.path.join(b, rel_path)

            os.makedirs(os.path.dirname(full_dst_path), exist_ok=True)
            shutil.move(full_src_path, full_dst_path)
            print(f"Moved: {full_src_path} -> {full_dst_path}")
