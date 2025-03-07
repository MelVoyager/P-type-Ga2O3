import yaml
import os
import shutil
from datetime import datetime

# projects = ['ga47_1o72_0']
projects = ['ga47_1n_1o72_0']

for project in projects:
    with open(f'{project}/config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)

    for task in cfg['tasks']:
        task_name, task_cfg = task.popitem()
        if task_cfg['run']:
            print('task_name:', task_name)

            task_dir = f'{project}/{task_name}'
            os.makedirs(task_dir, exist_ok=True)  # 创建 task_name 目录（如果不存在）

            for filename in ['INCAR', 'KPOINTS', 'POTCAR', 'POSCAR']:
                shutil.copy2(f'{project}/{task_cfg[filename]}', f'{task_dir}/{filename}')

            device_num = cfg['general']['num']

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            os.system(f'cd {task_dir} && mpirun -np {device_num} vasp_std > log_{timestamp}.txt')
