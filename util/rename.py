import os
import sys

def rename_files_and_folders(root_dir):
    """
    递归处理目录下的文件夹和文件，重命名符合规则的项
    """
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # 处理文件夹重命名
        for dir_name in dirs:
            basename = os.path.basename(dir_name)
            new_basename = None
            
            # 文件夹重命名规则
            if basename == "hse06_scf_-1":
                new_basename = "hse06_scf_-1_0.35"
            elif basename == "hse06_scf_0":
                new_basename = "hse06_scf_0_0.35"
                
            if new_basename:
                _rename_item(root, dir_name, new_basename, is_folder=True)

        # 处理文件重命名
        for file_name in files:
            basename = os.path.basename(file_name)
            new_basename = None
            
            # 文件重命名规则
            if basename == "INCAR_hse06_scf_-1":
                new_basename = "INCAR_hse06_scf_-1_0.35"
            elif basename == "INCAR_hse06_scf_0":
                new_basename = "INCAR_hse06_scf_0_0.35"
                
            if new_basename:
                _rename_item(root, file_name, new_basename, is_folder=False)

def _rename_item(root, old_name, new_name, is_folder=True):
    """统一的重命名处理函数"""
    item_type = "文件夹" if is_folder else "文件"
    old_path = os.path.join(root, old_name)
    new_path = os.path.join(root, new_name)
    
    if os.path.exists(new_path):
        print(f"⛔ 目标{item_type}已存在，跳过: {new_path}")
        return
    
    try:
        os.rename(old_path, new_path)
        print(f"✅ {item_type}重命名成功: {old_path} → {new_path}")
    except Exception as e:
        print(f"❌ {item_type}重命名失败: {old_path}")
        print(f"错误详情: {str(e)}")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "/home/bingxing2/ailab/xiazeyu_p/Programs/P-type-Ga2O3"
    
    if not os.path.isdir(target_dir):
        print(f"错误：目录不存在或不可访问 → {target_dir}")
        sys.exit(1)
    
    print(f"开始处理目录: {target_dir}")
    rename_files_and_folders(target_dir)
    print("处理完成")