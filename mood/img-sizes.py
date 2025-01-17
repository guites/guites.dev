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
    "./A-Grande-Onda-de-Kanagawa.webp",
    "./akira-tape-br-distrib.webp",
    "./carlos-bakery-pistache.webp",
    "./colonias-japonesas-30-teatro.webp",
    "./rotating-burgor-mp4-res.mp4",
    "./cow-red.webp",
    "./cyberpunk-tokyo-dave-murray.webp",
    "./era-isso-mesmo-que-eu-procurava-bleach.webp",
    "./hercilio-luz-fln.webp",
    "./steve-harris-fucking-it-up-mp4-res.mp4",
    "./hidden-girl-kitkat.webp",
    "./igreja-sto-antonio-lisboa.webp",
    "./LEPRECHAUN-sto-antonio-lisboa.webp",
    "./maiden-hands.webp",
    "./the-beautiful-hercilio-luz-mp4-res.mp4",
    "./mamba-wota.webp",
    "./not-sure-painting-reminds-of-samurai-shamploo.webp",
    "./old-asf-kimono.webp",
    "./view-of-the-beiramar-mp4-res.mp4",
    "./poa-ccmq-natal.webp",
    "./slam-dunk-manga-34-90.webp",
    "./push.webp",
    "./rosa-e-azul-1881-renoir.webp",
    "./samurai-gear.webp",
    "./sculpted-lion-santo-antonio-lisboa.webp",
    "./what-is-the-absurd-human-nature-mp4-res.mp4",
    "./potato-balls.webp",
    "./some-crossing-in-fln.webp",
    "./some-kickass-painting-angels-goth.webp",
    "./tea-coffee-options-machine.webp",
    "./trensurb-bench.webp",
    "./two-juice.webp",
    "./viados-atraves-grade-zoo.webp",
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
    "./alan-turing-i-support-ai.mp4",
    "./black-princess.webp",
    "./2024-08-16-zzzmaninha.webp",
    "./sleepy-bu.webp",
    "./bathroom-or-whatever.mp4",
    "./streets-of-poa.webp",
    "./sinatra.webp",
    "./jupy-aside.webp",
    "./whomst.webp",
    "./creature-glow.mp4",
    "./shaky-tower.mp4",
    "./birb.webp",
    "./flower-of-pasta.webp",
    "./tiao-bock.webp",
    "./wizz-snoop.mp4",
    "./meet-amyl.webp",
    "./chaos-floripa.webp",
    "./dizzy.webp",
    "./jupy-fades.mp4",
    "./structure-and-interpretation.webp",
    "./sun-go-down.webp",
]

img_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
video_extensions = (".mp4",)
target_width = (
    300 / 2
)  # smallest supported screen size (320px - 10px of padding on each side of the screen)
columns = ["<div class='left'>", "<div class='right'>"]

for idx, filename in enumerate(files):
    loading = "lazy"
    if idx == 0:
        loading = "eager"

    if filename.lower().endswith(img_extensions):
        min_height = get_target_height(filename, target_width)

        # Print the img html element
        media = f"""<img style="min-height: {min_height}px" loading="{loading}" src="{filename}">"""

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
        media = f"""
<video loop controls preload="none" style="min-height: {min_height}" poster="{video_poster}">
    <source src="{filename}" type="video/mp4">
</video>"""

    columns[idx % 2] += f"{media}\n"

print(
    """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mood | 🦝 guites webpage</title>

    <style>
        main {
            max-width: 100vw;
        }

        main img {
            max-width: 100%;
            object-fit: contain;
            margin-bottom: 4px;
        }

        main video {
            max-width: 100%;
            margin-bottom: 4px;
        }

        #gallery {
            max-width: 750px;
            margin: 0 auto;
        }

        h1,
        p {
            text-align: center;
        }
        .left, .right {
            width: calc(50% - 2px);
            float: left;
            display: flex;
            flex-direction: column;
        }
        .left {
            margin-right: 4px;
            align-items: flex-end;
        }
        .right {
            align-items: flex-start;
        }
    </style>
</head>

<body>
    <header>
        <nav>
            <ul>
                <li>
                    <a href="/">Index</a>
                </li>
            </ul>
        </nav>
        <hr>
    </header>
    <main>
        <h1>guites' mood board</h1>
        <p>doing wall sits because I've got weak knees and strong ambitions</p>
        <section id="gallery">
"""
)
for column in columns:
    print(f"{column}</div>\n")

print(
    """
      </section>
    </main>
</body>


</html>"""
)
