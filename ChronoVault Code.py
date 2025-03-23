#ChronoVault_Code
#时盾码
#by nDhnzr6r
#2025/3/24

import hashlib
import os
from datetime import datetime, timedelta

#默认盐值
DEFAULT_SALT = "nDhnzr6rNBYYDS"
TIME_FORMAT = "%Y%m%d%H%M"

def process_time_block(input_time_str):
    try:
        dt = datetime.strptime(input_time_str, TIME_FORMAT)
        adjusted_minute = (dt.minute // 10) * 10
        return dt.replace(minute=adjusted_minute, second=0, microsecond=0)
    except ValueError:
        return None

def time_to_encoding(input_time_str, salt=DEFAULT_SALT):
    dt_processed = process_time_block(input_time_str)
    if not dt_processed:
        return None
    
    timestamp = int(dt_processed.timestamp())
    hasher = hashlib.sha256()
    hasher.update(salt.encode('utf-8'))
    hasher.update(str(timestamp).encode('utf-8'))
    hash_digest = hasher.digest()[:10]
    
    base32_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    binary_str = ''.join(f"{byte:08b}" for byte in hash_digest)
    
    return ''.join([base32_chars[int(binary_str[i:i+5], 2)] for i in range(0, 80, 5)])

def batch_encode_from_file():
    input_file = "time.txt"
    output_file = "ChronoVault_Code_time.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"错误：当前目录下未找到 {input_file}")
        return

    salt = lines[0] if lines and lines[0] else DEFAULT_SALT
    results = [salt]
    
    for time_str in lines[1:]:
        if not time_str:
            results.append("编码无效")
            continue
            
        code = time_to_encoding(time_str, salt)
        results.append(code if code else "编码无效")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        print(f"批量编码完成，结果已保存到 {output_file}")
    except IOError:
        print(f"错误：无法写入 {output_file}，请检查文件权限")

def get_current_time_code(salt=DEFAULT_SALT):
    now = datetime.now().strftime(TIME_FORMAT)
    code = time_to_encoding(now, salt)
    return code if code else "当前时间编码失败"

def single_input_mode(salt=DEFAULT_SALT):
    while True:
        time_str = input("\n输入时间（格式：YYYYMMDDHHMM）或输入 exit、e 退出：")
        if time_str.lower() == 'e':
            break
            
        code = time_to_encoding(time_str, salt)
        print(f"编码结果：{code if code else '无效时间格式'}")

def main_menu():
    print("\n时间编码系统")
    print("1. 批量文件编码（自动读取 time.txt）")
    print("2. 获取当前时间编码")
    print("3. 单次输入编码")
    print("4. 退出系统")
    
    while True:
        choice = input("请选择操作（1-4）：")
        if choice == '1':
            batch_encode_from_file()
        elif choice == '2':
            code = get_current_time_code()
            print(f"\n当前时间编码：{code}")
        elif choice == '3':
            single_input_mode()
        elif choice == '4':
            break
        else:
            print("无效输入，请重新选择")

if __name__ == "__main__":
    main_menu()
