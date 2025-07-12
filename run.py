import yaml
import os
import shutil
import subprocess
from datetime import datetime

# projects = [ 'Fe_{Ga(I)}', 'Fe_{Ga(I)}-N_{O(I)}', 'Fe_{Ga(I)}-N_{O(II)}', 'Fe_{Ga(I)}-N_{O(III)}']
# projects = ['Fe_{Ga(II)}', 'Fe_{Ga(II)}-N_{O(I)}', 'Fe_{Ga(II)}-N_{O(II)}', 'Fe_{Ga(II)}-N_{O(III)}']
# projects = ['Fe_{Ga(II)}-N_{O(II)}', 'Fe_{Ga(I)}-N_{O(II)}', 'Fe_{Ga(I)}-N_{O(III)}']
projects = ['Mg']

os.environ["OMPI_MCA_btl_openib_warn_no_device_params_found"] = "0"
os.environ["OMPI_MCA_btl"] = "^openib"

for project in projects:
    with open(f'{project}/config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)
        print(f'path:{project}')
        
    for task in cfg['tasks']:
        task_name, task_cfg = task.popitem()
        
        # print(f'task_name:{task_name}')
        if task_cfg['run']:
            print('task_name:', task_name)

            task_dir = f'{project}/{task_name}'
            os.makedirs(task_dir, exist_ok=True)  # 创建 task_name 目录（如果不存在）

            for filename in ['INCAR', 'KPOINTS', 'POTCAR', 'POSCAR', 'CHGCAR', 'WAVECAR', 'CHG']:
                    # 构建源文件和目标文件路径
                    if filename not in task_cfg:
                        # print(f"Warning: {filename} 未配置，已跳过。")
                        continue

                    src = os.path.join(project, task_cfg[filename])
                    dst = os.path.join(task_dir, filename)
                    
                    # 检查源文件是否存在
                    if os.path.isfile(src):  # 确保是文件，而非目录
                        shutil.copy2(src, dst)
                    else:
                        print(f"Warning: {src} 不存在，已跳过。") 

            device_num = cfg['general']['num']
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            # 检查 task_dir 中是否已有 log_***.txt 文件
            existing_logs = [f for f in os.listdir(task_dir) if f.startswith("log_") and f.endswith(".txt")]
            if existing_logs:
                # 如果已存在 log_***.txt，则使用最新的日志文件
                existing_logs.sort()  # 确保按时间顺序排序
                log_file = existing_logs[-1]  # 选择最新的日志文件
            else:
                # 如果没有 log_***.txt，则创建新的
                log_file = f"log_{timestamp}.txt"

            # 生成 `run_vasp.sh` 脚本
            run_script = f"""
#!/bin/bash
module purge
module load nvhpc/23.3_cuda11.0-11.8-12.0/nvhpc/23.3
export PATH=/home/bingxing2/ailab/xiazeyu_p/soft/vasp.6.4.2-nvhpc/bin:$PATH
mpirun -n {device_num} vasp_std >> {log_file} 2>&1
"""
            script_path = os.path.join(task_dir, "run_vasp.sh")

            with open(script_path, "w") as script_file:
                # print(script_path)
                script_file.write(run_script)

            # 给予执行权限
            os.chmod(script_path, 0o755)
            # print(f"task_dir:{task_dir}")
            # 运行脚本
            subprocess.run(["bash", "run_vasp.sh"], cwd=task_dir)
