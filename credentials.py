import os

from PIL import Image, ImageFont, ImageDraw, ImageFilter

def setShadow(I, text, position, style):
	font = ImageFont.truetype(style["font"], style["font_size"])

	# Create a shadow text image with RGBA mode
	shadow_text_image = Image.new("RGBA", I.size, (0, 0, 0, 0))  # Transparent black
	shadow_text_draw = ImageDraw.Draw(shadow_text_image)
	shadow_text_draw.text(position, text, fill=(0, 0, 0, style["shadow"]["opacity"]), font=font)

	# Apply a blur filter to the shadow text
	shadow_text_image = shadow_text_image.filter(ImageFilter.GaussianBlur(radius=10))

	# Paste the shadow text onto the original image using alpha mask
	I.paste(shadow_text_image, (0, 0), shadow_text_image)

def writeCredential(name, credential, style, output_path):
	I=Image.open(credential)
	W, H = I.size
	font = ImageFont.truetype(style["font"], style["font_size"])

	name = name.upper()
	draw = ImageDraw.Draw(I)
	text_length = draw.textlength(name, font=font)

	shadow_position = ((W-text_length)/2, style["upper_offset"] + 10)
	name_position = ((W-text_length)/2, style["upper_offset"])

	if "shadow" in style:
		setShadow(I, name, shadow_position, style)
	draw.text(name_position, name, fill=style["color"], font=font)

	# check if output path exists
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	output = output_path+"/"+name.lower().replace(" ", "_")+"-credential.png"
	I.save(output)