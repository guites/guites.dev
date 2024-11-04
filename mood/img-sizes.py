from PIL import Image
import cv2


def get_target_height(filename, target_width):
    with Image.open(filename) as img:
        # Get the original width and height
        original_width, original_height = img.size

        # Calculate the new height to maintain the aspect ratio
        aspect_ratio = original_height / original_width
        return int(target_width * aspect_ratio)


files = [
    "./cooking-soul-whateva-vol-2.webp",
    "./willhelm-screamer.webp",
    "./arrombadores.mp4",
    "./pharmacy.webp",
    "./face-to-face-band-pic.webp",
    "./face-to-face-sweaty-bass-man.mp4",
    "./meets-basket.webp",
    "./spooky-catita.webp",
    "./tree-way.webp",
    "./statue.webp",
    "./window-view.webp",
    "./black-princess.webp",
    "./2024-08-16-zzzmaninha.webp",
    "./sleepy-bu.webp",
    "./bathroom-or-whatever.mp4",
    "./streets-of-poa.webp",
    "./sinatra.webp",
    "./whomst.webp",
    "./shaky-tower.mp4",
    "./birb.webp",
    "./flower-of-pasta.webp",
    "./tiao-bock.webp",
    "./wizz-snoop.mp4",
    "./meet-amyl.webp",
    "./sun-go-down.webp",
    "./chaos-floripa.webp",
]

img_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
video_extensions = (".mp4",)
target_width = 300

for idx, filename in enumerate(files):
    loading = "lazy"
    if idx == 0:
        loading = "eager"

    if filename.lower().endswith(img_extensions):
        min_height = get_target_height(filename, target_width)

        # Print the img html element
        print(
            f"""<img style="min-height: {min_height}px" loading="{loading}" src="{filename}">"""
        )
        continue

    if filename.lower().endswith(video_extensions):

        cap = cv2.VideoCapture(filename)
        # read the first frame
        success, frame = cap.read()
        if not success:
            raise ValueError(
                f"Couldn't generate video thumbnail for {filename} (ノ°益°)ノ"
            )
        video_poster = f"{filename}.webp"
        cv2.imwrite(video_poster, frame)
        cap.release()

        min_height = get_target_height(video_poster, target_width)
        print(
            f"""
<video loop controls preload="none" style="min-height: {min_height}" poster="{video_poster}">
    <source src="{filename}" type="video/mp4">
</video>"""
        )
        continue
