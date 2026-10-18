import os, sys, shutil
import fitz
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

B = "."
OUT = "../outputs/JNA_submission/Figures"
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

SOURCES = {
    "Figure 1": (os.path.join(B, "_prisma", "prisma_76.pdf"), fitz.Rect(38, 50, 802, 496)),
    "Figure 2": (os.path.join(B, "figs", "jna_fig2_evidence_map.pdf"), None),
    "Figure 3": (os.path.join(B, "figs", "jna_fig3_two_hit.pdf"), None),
}

def to_tiff(pix, path):
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.save(path, compression="tiff_lzw", dpi=(pix.xres or 1200, pix.yres or 1200))

for name, (src, clip) in SOURCES.items():
    doc = fitz.open(src)
    page = doc[0]
    if clip is not None:
        page.set_cropbox(clip)
    rect = page.rect
    doc.save(os.path.join(OUT, name + ".pdf"))
    for dpi, ext in ((600, "png"), (1200, "tif")):
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        path = os.path.join(OUT, "%s.%s" % (name, ext))
        if ext == "png":
            pix.save(path)
        else:
            to_tiff(pix, path)
    doc.close()
    print(name, [os.path.getsize(os.path.join(OUT, name + e)) // 1024 for e in (".pdf", ".png", ".tif")], "KB")
