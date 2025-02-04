const canvasEl = document.getElementById("canvas");
const canvas = new fabric.Canvas(canvasEl);
const colorPicker = document.getElementById("color");
const fontSize = document.getElementById("fontSize");
const fontFamily = document.getElementById("fontFamily");

const downloadBtn = document.getElementById("download");

const comicSans = new FontFace("ComicSans", "url(comic-webfont.woff2)", {
  style: "normal",
  weight: "normal",
});

const gillSansBold = new FontFace(
  "GillSansBold",
  "url(gill-sans-bold-webfont.woff2)",
  {
    style: "normal",
    weight: "700",
  }
);

const textbox = new fabric.Textbox(
  "> make tshirt\n> feel like a real human beign",
  {
    fontFamily: "ComicSans",
    fill: "#789922",
    width: 258,
    originX: "center",
    originY: "center",
    left: 235.95132,
    top: 112.009,
    fontSize: 17,
  }
);

Promise.all([comicSans.load(), gillSansBold.load()]).then(() => {
  document.fonts.add(comicSans);
  document.fonts.add(gillSansBold);
  fabric.Image.fromURL("./black-shirt-res.png").then((img) => {
    img.set({
      lockMovementX: true,
      lockMovementY: true,
      lockScalingX: true,
      lockScalingY: true,
      lockRotation: true,
      selectable: false,
    });
    canvas.add(img);
    canvas.add(textbox);
  });

  colorPicker.addEventListener("input", (e) => {
    textbox.set("fill", e.target.value);
    canvas.requestRenderAll();
  });

  fontSize.addEventListener("input", (e) => {
    textbox.set("fontSize", parseInt(e.target.value));
    canvas.requestRenderAll();
  });

  fontFamily.addEventListener("input", (e) => {
    textbox.set("fontFamily", e.target.value);
    canvas.requestRenderAll();
  });
});

// prevent textbox from being larger than 258px on resize
canvas.on("object:scaling", (e) => {
  const obj = e.target;
  console.log(obj);
  if (obj.type === "textbox" && obj.width * obj.scaleX > 258) {
    obj.set("scaleX", 258 / obj.width);
    obj.set("scaleY", 258 / obj.width);
  }
});

// downloads current canvas as image on button press
downloadBtn.addEventListener("click", () => {
  const dataURL = canvas.toDataURL({
    format: "png",
    quality: 1,
  });
  // creates a link element and clicks it
  const newDownloadLink = document.createElement("a");
  newDownloadLink.href = dataURL;
  newDownloadLink.download = "tshirt.png";
  newDownloadLink.click();
});
