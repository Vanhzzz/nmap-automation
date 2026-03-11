import os
import subprocess
import xml.etree.ElementTree as ET
import sys
import time

# CẤU HÌNH
TARGET = "192.168.1.0/24"
WHITELIST_FILE = "known_devices.txt"
STRANGERS_LOG = "strangers_log.txt"
OUTPUT_XML = "scan_results.xml"
INTERVAL = 300  # 300 giây = 5 phút

def get_whitelist():
    # Kiểm tra file có tồn tại không
    if not os.path.exists(WHITELIST_FILE):
        print(f"❌ LỖI NGHIÊM TRỌNG: Không tìm thấy file danh sách trắng '{WHITELIST_FILE}'.")
        print("Vui lòng tạo file này và thêm các địa chỉ MAC tin cậy trước khi chạy.")
        sys.exit(1) # Dừng chương trình ngay lập tức
    
    with open(WHITELIST_FILE, "r") as f:
        # Đọc và làm sạch dữ liệu
        lines = [line.strip().lower() for line in f if line.strip()]
        
    if not lines:
        print(f"⚠️ CẢNH BÁO: File '{WHITELIST_FILE}' đang trống. Mọi thiết bị quét được sẽ bị coi là LẠ.")
    
    return lines

def run_nmap():
    print(f"[*] Đang quét dải IP: {TARGET}...")
    try:
        cmd = ["sudo", "nmap", "-sn", TARGET, "-oX", OUTPUT_XML]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"❌ Lỗi Nmap: Hãy đảm bảo bạn chạy script bằng 'sudo python3 ...'")
        return False
    return True

def analyze():
    if not os.path.exists(OUTPUT_XML):
        return

    whitelist = get_whitelist()
    tree = ET.parse(OUTPUT_XML)
    root = tree.getroot()
    
    found_unknown = False
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    for host in root.findall('host'):
        status = host.find('status').get('state')
        if status != 'up': continue
        
        ip = host.find("./address[@addrtype='ipv4']").get('addr')
        mac_node = host.find("./address[@addrtype='mac']")
        
        if mac_node is not None:
            mac = mac_node.get('addr').lower()
            vendor = mac_node.get('vendor', 'Unknown Vendor')
            
            if mac not in whitelist:
                msg = f"⚠️ [{timestamp}] THIẾT BỊ LẠ! IP: {ip} | MAC: {mac} ({vendor})"
                print(msg)
                with open(STRANGERS_LOG, "a") as f:
                    f.write(msg + "\n")
                found_unknown = True
        else:
            # Bỏ qua chính máy đang chạy quét (vì nmap thường không hiện MAC của chính nó)
            pass
    
    if not found_unknown:
        print("✅ Quét xong: Mạng an toàn.")

if __name__ == "__main__":
    # Kiểm tra quyền Root
    if os.getuid() != 0:
        print("❌ LỖI: Script này bắt buộc phải chạy bằng quyền ROOT.")
        print("Sử dụng: sudo python3 <tên_file>.py")
        sys.exit(1)

    # Kiểm tra file whitelist lần đầu trước khi vào vòng lặp
    get_whitelist()

    print(f"🚀 Hệ thống bắt đầu giám sát mạng {TARGET}")
    print(f"🕒 Chu kỳ: {INTERVAL/60} phút/lần. Nhấn Ctrl+C để dừng.")
    
    try:
        while True:
            print(f"\n--- Kiểm tra lúc {time.strftime('%H:%M:%S')} ---")
            if run_nmap():
                analyze()
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n👋 Đã dừng giám sát.")
        if os.path.exists(OUTPUT_XML): os.remove(OUTPUT_XML)
        sys.exit(0)