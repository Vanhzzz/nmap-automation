# nmap-automation
Script1: Giám sát thiết bị lạ kết nối vào mạng nội bộ
Script tự động chạy trong 5p. Nếu có thiết bị nào khác với địa chỉ MAC đã lưu sẽ cảnh bảo thiết bị lạ

`sudo python3 s1.py`

Script2: Tự động tìm kiếm lỗ hổng, sử dụng Cronjob để tự động chạy script vào khung thời gian nhất định
#### 1. Cấu hình tự động với Cronjob
`crontab -e`

**Chạy vào 2h sáng mỗi ngày :**
```cron
0 2 * * * /usr/bin/python3 /home/kali/script2.py >> /home/kali/reports/cron_log.log 2>&1

