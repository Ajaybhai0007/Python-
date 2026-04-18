
import yt_dlp
import sys

def get_direct_video_url(video_url: str) -> str:
    """
    Kisi bhi supported video link se highest quality ka direct stream URL nikaalta hai.
    Supported sites: YouTube, Instagram, TikTok, Facebook, Twitter, Vimeo aur bohot saare.
    
    :param video_url: Video ka share link (jaise https://www.youtube.com/watch?v=...)
    :return: Direct playable/downloadable video URL (string)
    :raises: Exception agar URL supported nahi ya error aaye
    """
    # yt-dlp options: Download nahi karna, sirf info extract karna
    ydl_opts = {
        'quiet': True,                  # Console spam avoid karne ke liye
        'no_warnings': True,
        'format': 'bestvideo+bestaudio/best',  # Best possible quality (progressive prefer)
        'merge_output_format': 'mp4',   # Agar merge karna pade to MP4
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Sirf info extract karo, download mat karo
            info = ydl.extract_info(video_url, download=False)
            
            # Direct URL nikaalo (already merged ya best format)
            direct_url = info.get('url')
            if not direct_url:
                # Agar formats list mein hai to best wala choose karo
                formats = info.get('formats', [])
                # Highest resolution + audio wala prefer
                best_format = max(
                    formats,
                    key=lambda f: (
                        f.get('height', 0) or 0,
                        f.get('fps', 0) or 0,
                        f.get('filesize', 0) or 0
                    ),
                    default=None
                )
                if best_format:
                    direct_url = best_format.get('url')
            
            if not direct_url:
                raise ValueError("Direct URL nahi mil paya video ke liye.")
            
            return direct_url
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        raise

# Example usage
if __name__ == "__main__":
    url = input("Video ka link daalo: ").strip()
    try:
        direct_link = get_direct_video_url(url)
        print("\nDirect Video URL:")
        print(direct_link)
        print("\nIse browser mein kholo ya wget/curl se download kar sakte ho!")
    except:
        print("Koi issue aaya, shayad link supported nahi ya network problem.")
