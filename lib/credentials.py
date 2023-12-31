import os
from PIL import Image, ImageFont, ImageDraw, ImageFilter

class Credential:
	progress = 0
	total = 0
	plugin = None
	tier = None
	saved = []

	def __init__(self, template):
		if not template:
			print("No template specified.")
			return
		
		self.image = self.open(template)
		self.draw = ImageDraw.Draw(self.image)


	def size(self):
		return self.image.size

	def open(self, path):
		if not os.path.exists(path):
			print(f"Image '{path}' not found.")
			return

		return Image.open(path)

	def save(self, filename):
		path = f"credentials/{Credential.plugin}/{Credential.tier}"
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))

		self.image.save(f"{path}/{filename}.png")
		Credential.saved.append(f"{path}/{filename}.png")

		Credential.progress += 1
		if Credential.total > 0:
			progress_bar(Credential.progress, Credential.total)

	def text_length(self, text, style):
		font = ImageFont.truetype(style["font"], style["font_size"])
		return self.draw.textlength(text, font=font)

	def shadow(self, text, position, style):
		font = ImageFont.truetype(style["font"], style["font_size"])

		# Create a shadow text image with RGBA mode
		shadow_text_image = Image.new("RGBA", self.size(), (0, 0, 0, 0))  # Transparent black
		shadow_text_draw = ImageDraw.Draw(shadow_text_image)
		shadow_text_draw.text(position, text, fill=(0, 0, 0, style["shadow"]["opacity"]), font=font)

		# Apply a blur filter to the shadow text
		shadow_text_image = shadow_text_image.filter(ImageFilter.GaussianBlur(radius=10))

		# Paste the shadow text onto the original image using alpha mask
		self.image.paste(shadow_text_image, (0, 0), shadow_text_image)

	def write(self, text, style):
		W, H = self.size()
		font = ImageFont.truetype(style["font"], style["font_size"])

		text_length = self.draw.textlength(text, font=font)
		name_position = ((W-text_length)/2, style["upper_offset"])

		if "shadow" in style:
			shadow_position = ((W-text_length)/2, style["upper_offset"] + 10)
			self.shadow(text, shadow_position, style)

		self.draw.text(name_position, text, fill=style["color"], font=font)

	def set_total(self, total):
		Credential.total = total


def progress_bar(progress, total):
	print(f"\r[{'='*int(progress/total*50):50}] {progress}/{total} {int(progress/total*100)}%", end="")
	if progress == total:
		print("")