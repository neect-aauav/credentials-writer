from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas
from PIL import Image
from PyPDF2 import PdfMerger
import os

A4_WIDTH, A4_HEIGHT = A4

def merge_a4(files, output):
	merger = PdfMerger()
	for file in files:
		merger.append(file)

	merger.write(f"print/{output}")
	merger.close()

def print_a6_in_a4(images, output):
	# create folder print if it doesn't exist
	if not os.path.exists("print"):
		os.makedirs("print")

	# Create a canvas for the PDF file
	c = canvas.Canvas(f"print/{output}", pagesize=portrait(A4))

	# Calculate the positions and sizes of A6 images on the A4 canvas
	margin = 10
	image_width = (A4_WIDTH - 3 * margin) / 2
	image_height = (A4_HEIGHT - 2 * margin) / 2

	# Loop through the image files and add them to the A4 canvas
	for i, image_file in enumerate(images):
		if i % 2 == 0:
			x = margin
		else:
			x = margin + image_width
		if i < 2:
			y = A4_HEIGHT - margin - image_height
		else:
			y = margin

		# Open and resize the image to fit the A6 size
		image = Image.open(image_file)
		image.thumbnail((image_width, image_height), Image.Resampling.LANCZOS)
		
		# Add the resized image to the PDF canvas
		c.drawImage(image_file, x, y, width=image_width, height=image_height, preserveAspectRatio=True, mask='auto')

	# Save the PDF
	c.save()