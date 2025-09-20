import yt_dlp
import os
import re
import sys

# 設定環境變數解決編碼問題
os.environ['PYTHONIOENCODING'] = 'utf-8'


def sanitize_filename(filename):
    """清理檔案名稱，移除不合法字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename[:200]  # 限制檔名長度


def detect_platform(url):
    """檢測影片平台"""
    if 'bilibili.com' in url or 'b23.tv' in url:
        return 'bilibili'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    else:
        return 'unknown'


def download_video(url, output_path='./downloads/jpk'):
    """
    下載 YouTube 或 Bilibili 影片為 MP4 格式

    Args:
        url (str): YouTube 或 Bilibili 影片網址
        output_path (str): 下載路徑，預設為 './downloads/jpk'
    """
    try:
        # 確保輸出目錄存在
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # 檢測平台並設定相應選項
        platform = detect_platform(url)

        # 設定 yt-dlp 選項
        if platform == 'bilibili':
            # B站只下載影片，不下載聲音
            ydl_opts = {
                'format': '30127/30126/30125/30121/30120/30112/30080/30077/30064/30032/30016/best',  # 只下載影片
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'no_warnings': True,
            }
        else:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'no_warnings': True,
            }

        # 下載影片
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"開始下載: {url}")

            # 直接下載影片
            ydl.download([url])
            print("下載完成！")

    except Exception as e:
        print(f"下載失敗: {str(e)}")


def download_multiple_videos(urls, output_path='./downloads'):
    """
    批量下載多個 YouTube 或 Bilibili 影片

    Args:
        urls (list): YouTube 或 Bilibili 影片網址列表
        output_path (str): 下載路徑
    """
    for i, url in enumerate(urls, 1):
        print(f"\n正在下載第 {i}/{len(urls)} 個影片...")
        download_video(url, output_path)


def main():
    """主程式"""
    print("YouTube & Bilibili 影片下載器")
    print("=" * 30)

    while True:
        print("\n請選擇操作:")
        print("1. 下載單個影片")
        print("2. 批量下載影片")
        print("3. 退出")

        choice = input("請輸入選項 (1-3): ").strip()

        if choice == '1':
            url = input("請輸入 YouTube 或 Bilibili 網址: ").strip()
            if url:
                output_path = input("請輸入下載路徑 (直接按 Enter 使用預設路徑 './downloads/jpk'): ").strip()
                if not output_path:
                    output_path = './downloads/jpk'
                download_video(url, output_path)
            else:
                print("網址不能為空!")

        elif choice == '2':
            print("請輸入多個 YouTube 或 Bilibili 網址，每行一個，輸入空行結束:")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)

            if urls:
                output_path = input("請輸入下載路徑 (直接按 Enter 使用預設路徑 './downloads/jpk'): ").strip()
                if not output_path:
                    output_path = './downloads/jpk'
                download_multiple_videos(urls, output_path)
            else:
                print("沒有輸入任何網址!")

        elif choice == '3':
            print("感謝使用！")
            break

        else:
            print("無效選項，請重新選擇!")


if __name__ == "__main__":
    download_video("https://www.bilibili.com/video/BV1rrTCzfEWz/?spm_id_from=333.337.search-card.all.click&vd_source=4c8efeb752a121aeaec792dabbde38b6")