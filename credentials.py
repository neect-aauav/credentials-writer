from PIL import Image, ImageFont, ImageDraw

FONT = "assets/Panton-Black.ttf"
FONT_SIZE = 105
CREDENTIAL = "credencial_empty.png"
COLOR = "#f9a31c"
UPPER_OFFSET = 875

def getNames(file):
	with open(file) as f:
		names = f.readlines()
	return names

def writeCredential(name):
	I=Image.open(CREDENTIAL)
	W, H = I.size
	font = ImageFont.truetype(FONT, FONT_SIZE)

	draw = ImageDraw.Draw(I)
	text_length = draw.textlength(name, font=font)
	draw.text(((W-text_length)/2, UPPER_OFFSET), name, fill=COLOR, font=font)
	I.save(name.lower().replace(" ", "_")+"-credential.png")

def main():
	for name in getNames("names.txt"):
		name = name.strip()
		writeCredential(name)

if __name__ == "__main__":
	main()