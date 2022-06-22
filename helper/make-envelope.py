import PIL.Image
import PIL.ImageDraw
import PIL.ImageOps

im = PIL.Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
imDraw = PIL.ImageDraw.ImageDraw(im)
# Draw first rectangle.
imDraw.rectangle(((52, 277), (971, 746)), fill = (255, 233, 204, 255), outline = (0, 0, 0, 255), width = 20)
# Draw lines for bottom of envelope.
imDraw.line(((52, 746), (750, 277)), fill = (0, 0, 0, 255), width = 20)

# Draw top of envelope.
#imDraw.polygon(((52, 277), (511.5, 511.5), (971, 277)), fill = (255, 220, 173, 255), outline = (0, 0, 0, 255), width = 20)
#imDraw.polygon(((30, 277), (511.5, 511.5), (993, 277)), fill = (255, 220, 173, 255), outline = (0, 0, 0, 255), width = 20)
imDraw.polygon(((30, 277), (512, 512), (993, 277)), fill = (255, 220, 173, 255), outline = (0, 0, 0, 255), width = 20)

# Cut the lines out of the edge.
imDraw.rectangle(((12, 237), (1011, 786)), outline = (0, 0, 0, 0), width = 40)


# Okay, so we are actually doing something dump to compensate for PIL issues. So
# what we are doing is grabbing 1/2 of the image, mirroring it, then pasting it
# back in.
cop = PIL.ImageOps.mirror(im.copy().crop((0, 0, 512, 1024)))
im.paste(cop, (512, 0))

im.save('envelope_1024.png')
