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
    "./arrombadores.mp4",
    "./willhelm-screamer.jpg",
    "./pharmacy.jpg",
    "./face-to-face-band-pic.jpg",
    "./face-to-face-sweaty-bass-man.mp4",
    "./meets-basket.jpg",
    "./spooky-catita.jpg",
    "./tree-way.jpeg",
    "./statue.jpg",
    "./window-view.jpg",
    "./black-princess.jpg",
    "./2024-08-16-zzzmaninha.png",
    "./sleepy-bu.jpg",
    "./bathroom-or-whatever.mp4",
    "./streets-of-poa.jpg",
    "./sinatra.jpg",
    "./whomst.jpg",
    "./shaky-tower.mp4",
    "./birb.jpg",
    "./flower-of-pasta.jpeg",
    "./tiao-bock.jpg",
    "./wizz-snoop.mp4",
    "./meet-amyl.jpg",
    "./sun-go-down.jpg",
    "./chaos-floripa.jpg",
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
        video_poster = f"{filename}.jpg"
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
