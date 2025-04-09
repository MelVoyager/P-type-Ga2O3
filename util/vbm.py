import re

def find_vbm(outcar_path):
    # 初始化全局价带顶
    global_vbm = -float('inf')
    
    # 正则表达式匹配模式
    # kpoint_pattern = re.compile(r"k-point\s+\d+ :")      # 匹配k-point行
    band_pattern = re.compile(r"\s*(\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)")  # 匹配能带行
    
    with open(outcar_path, 'r') as f:
        lines = f.readlines()
        total = len(lines)
        i = 0
        
        while i < total:
            line = lines[i]
            if 'E-fermi' in line:
                e_fermi = float(line.split()[2])
            # 检测k-point行
            if 'k-point' in line:
                current_vbm = -float('inf')
                i += 2  # 跳过k-point行和表头行
                
                # 处理当前k点的所有能带
                while i < total:
                    match = band_pattern.match(lines[i])
                    if not match:
                        break  # 能带部分结束
                    
                    band_idx = int(match.group(1))
                    energy = float(match.group(2))
                    occupation = float(match.group(3))
                    
                    # 检查占据数是否接近2.0（考虑浮点误差）
                    if abs(occupation - 2.0) < 1e-4:
                        current_vbm = max(current_vbm, energy)
                    else:
                        break  # 遇到未占据能带，停止当前k点处理
                    
                    i += 1
                
                # 更新全局价带顶
                global_vbm = max(global_vbm, current_vbm)
            else:
                i += 1

    return global_vbm, e_fermi

if __name__ == "__main__":
    vbm_energy, e_fermi = find_vbm("/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3/ga47_1o71p_1/hse06_scf_-1_0.32/OUTCAR")
    print(f'费米能:{e_fermi:.4f} eV')
    print(f"价带顶 (VBM) 能量: {vbm_energy:.4f} eV")