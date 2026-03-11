import subprocess
from datetime import datetime
import os

# Cấu hình chính xác IP mục tiêu
TARGET = "192.168.30.137"
REPORT_DIR = "/home/kali/reports" # Nên dùng đường dẫn tuyệt đối khi chạy cron

def scan_vulnerabilities():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M")
    report_path = os.path.join(REPORT_DIR, f"vuln_report_{date_str}.txt")
    
    print(f"[{now}] 🚀 Bắt đầu quét mục tiêu: {TARGET}...")
    
    # Nmap command
    command = ["nmap", "-sV", "--script", "vuln", TARGET, "-oN", report_path]
    
    try:
        # Chạy lệnh và ghi đè log
        subprocess.run(command, check=True)
        print(f"[{datetime.now()}] ✅ Hoàn thành! Báo cáo lưu tại: {report_path}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Lỗi: {e}")

if __name__ == "__main__":
    scan_vulnerabilities()