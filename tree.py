import os

# 定义需要显示但不展开的文件夹和文件
NO_EXPAND_ITEMS = {'.git', '__pycache__', '.idea', 'images', 'static'}

def print_directory_structure(root_dir, prefix=""):
    # 获取目录中所有的文件和文件夹
    items = os.listdir(root_dir)
    for index, item in enumerate(items):
        # 构造当前项目的完整路径
        item_path = os.path.join(root_dir, item)
        is_last = (index == len(items) - 1)

        # 使用不同的符号来表示最后一个项目
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item}")

        # 如果是文件夹且不在 NO_EXPAND_ITEMS 中，则递归调用此函数
        if os.path.isdir(item_path) and item not in NO_EXPAND_ITEMS:
            new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            print_directory_structure(item_path, new_prefix)

if __name__ == "__main__":
    root_directory = "."  # 当前目录
    print_directory_structure(root_directory)
