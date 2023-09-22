from PIL import Image, ImageFont, ImageDraw, ImageFilter

FONT = "assets/Panton-Black.ttf"
FONT_SIZE = 105
CREDENTIAL = "credencial_empty.png"
COLOR = "#f9a31c"
UPPER_OFFSET = 875

def getNames(file):
	with open(file) as f:
		names = f.readlines()
	return names

def setShadow(I, text, position, opacity):
	font = ImageFont.truetype(FONT, FONT_SIZE)

	# Create a shadow text image with RGBA mode
	shadow_text_image = Image.new("RGBA", I.size, (0, 0, 0, 0))  # Transparent black
	shadow_text_draw = ImageDraw.Draw(shadow_text_image)
	shadow_text_draw.text(position, text, fill=(0, 0, 0, opacity), font=font)

	# Apply a blur filter to the shadow text
	shadow_text_image = shadow_text_image.filter(ImageFilter.GaussianBlur(radius=10))

	# Paste the shadow text onto the original image using alpha mask
	I.paste(shadow_text_image, (0, 0), shadow_text_image)

def writeCredential(name):
	I=Image.open(CREDENTIAL)
	W, H = I.size
	font = ImageFont.truetype(FONT, FONT_SIZE)

	name = name.upper()
	draw = ImageDraw.Draw(I)
	text_length = draw.textlength(name, font=font)

	shadow_position = ((W-text_length)/2, UPPER_OFFSET + 10)
	name_position = ((W-text_length)/2, UPPER_OFFSET)

	setShadow(I, name, shadow_position, 190)
	draw.text(name_position, name, fill=COLOR, font=font)

	I.save(name.lower().replace(" ", "_")+"-credential.png")

def main():
	for name in getNames("names.txt"):
		name = name.strip()
		writeCredential(name)

if __name__ == "__main__":
	main()