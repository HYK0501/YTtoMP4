import yt_dlp
import os
import re


def sanitize_filename(filename):
    """清理檔案名稱，移除不合法字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename[:200]  # 限制檔名長度


def download_youtube_video(url, output_path='./downloads/jpk'):
    """
    下載 YouTube 影片為 MP4 格式

    Args:
        url (str): YouTube 影片網址
        output_path (str): 下載路徑，預設為 './downloads'
    """
    try:
        # 確保輸出目錄存在
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # 設定 yt-dlp 選項
        ydl_opts = {
            'format': 'best[ext=mp4][height<=1080]/best[ext=mp4]/best',  # 優先選擇720p MP4
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # 輸出檔名格式
            'restrictfilenames': True,  # 限制檔名字符
        }

        # 下載影片
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"開始下載: {url}")

            # 獲取影片資訊
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)

            print(f"影片標題: {title}")
            print(f"影片長度: {duration // 60}分{duration % 60}秒")

            # 下載影片
            ydl.download([url])
            print("下載完成！")

    except Exception as e:
        print(f"下載失敗: {str(e)}")


def download_multiple_videos(urls, output_path='./downloads'):
    """
    批量下載多個 YouTube 影片

    Args:
        urls (list): YouTube 影片網址列表
        output_path (str): 下載路徑
    """
    for i, url in enumerate(urls, 1):
        print(f"\n正在下載第 {i}/{len(urls)} 個影片...")
        download_youtube_video(url, output_path)


def main():
    """主程式"""
    print("YouTube 影片下載器")
    print("=" * 30)

    while True:
        print("\n請選擇操作:")
        print("1. 下載單個影片")
        print("2. 批量下載影片")
        print("3. 退出")

        choice = input("請輸入選項 (1-3): ").strip()

        if choice == '1':
            url = input("請輸入 YouTube 網址: ").strip()
            if url:
                output_path = input("請輸入下載路徑 (直接按 Enter 使用預設路徑 './downloads'): ").strip()
                if not output_path:
                    output_path = './downloads'
                download_youtube_video(url, output_path)
            else:
                print("網址不能為空!")

        elif choice == '2':
            print("請輸入多個 YouTube 網址，每行一個，輸入空行結束:")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)

            if urls:
                output_path = input("請輸入下載路徑 (直接按 Enter 使用預設路徑 './downloads'): ").strip()
                if not output_path:
                    output_path = './downloads'
                download_multiple_videos(urls, output_path)
            else:
                print("沒有輸入任何網址!")

        elif choice == '3':
            print("感謝使用！")
            break

        else:
            print("無效選項，請重新選擇!")


if __name__ == "__main__":
    download_youtube_video("https://www.youtube.com/watch?v=WCDLyXJgbIo")