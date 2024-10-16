import pandas as pd

def check_and_convert_to_csv(file_path, processed_file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Lỗi khi đọc tệp Excel: {e}")
        return

    df.to_csv(processed_file_path, index=False, sep=',', decimal='.')

    print("Đã chuyển đổi tệp {a} thành {b} thành công!".format(a=file_path, b=processed_file_path))
    