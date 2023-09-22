from PIL import Image, ImageFont, ImageDraw, ImageFilter
import sys
import os

FONT = "assets/fonts/Panton-Black.ttf"
FONT_SIZE = 105
COLOR = "#f9a31c"
UPPER_OFFSET = 875

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

def writeCredential(name, credential, output_path):
	I=Image.open(credential)
	W, H = I.size
	font = ImageFont.truetype(FONT, FONT_SIZE)

	name = name.upper()
	draw = ImageDraw.Draw(I)
	text_length = draw.textlength(name, font=font)

	shadow_position = ((W-text_length)/2, UPPER_OFFSET + 10)
	name_position = ((W-text_length)/2, UPPER_OFFSET)

	setShadow(I, name, shadow_position, 190)
	draw.text(name_position, name, fill=COLOR, font=font)

	# check if output path exists
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	output = output_path+"/"+name.lower().replace(" ", "_")+"-credential.png"
	I.save(output)

def getNames(file):
	with open(file) as f:
		names = f.readlines()
	return names

def showHelp(program_name):
	print(f"Usage: python3 {program_name} <type> [file]")
	print("   type: \tthe type of credential, which matches the \n        \tcredential image name and the names file name \n        \t(default: participante)")
	print("   file: \tpath to file with names (optional)")

def main():
	args = sys.argv[1:]

	# display help
	if len(args) == 1 and (args[0].startswith("-") or args[0].startswith("--")):
		showHelp(sys.argv[0])	
		return

	# handle arguments
	type = "participante"
	file = "names/participantes.txt"
	if len(args) > 0:
		type = args[0]
		file = "names/"+type+".txt"
		if len(args) == 2:
			file = args[1]
		
	print(f"Generating credentials for '{type}' from file '{file}'...")

	if not os.path.exists(file):
		print(f"File '{file}' not found.\n")
		showHelp(sys.argv[0])
		return

	for name in getNames(file):
		writeCredential(name.strip(), f"assets/credentials/{type}.png", f"credentials/{type}")

	print(f"Generated {len(getNames(file))} credentials for '{type}' in folder 'credentials/{type}/'")

if __name__ == "__main__":
	main()