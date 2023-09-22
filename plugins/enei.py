NAME_STYLE = {
	'font_size': 105,
	'font': "fonts/Panton-Black.ttf",
	'color': "#f9a31c",
	'upper_offset': 875,
	'shadow': {
		'opacity': 190
	}
}

TIER_STYLE = {
	'font_size': 85,
	'font': "fonts/Panton-Black.ttf",
	'color': "#ffffff",
	'upper_offset': 1050,
	'shadow': {
		'opacity': 190
	}
}

def getNames(file):
	with open(file) as f:
		names = f.readlines()
	return names

def run(new, file, type):
	names = getNames(file)
	for name in names:
		name = name.upper().strip()

		# handle names with more than two words
		if len(name.split()) > 2:
			name = name.split()[0] + " " + name.split()[-1]

		# instantiate new credential
		credential = new()
		w, h = credential.imageSize()

		# WRITE NAME
		name_length = credential.textLength(name, NAME_STYLE)
		# if name is too long, break it into two lines
		if name_length > w:
			slitted = name.split()
			credential.writeCredential(slitted[0], NAME_STYLE) # write first name
			NAME_STYLE['upper_offset'] += 100
			credential.writeCredential(slitted[1], NAME_STYLE) # write second name
		else:
			credential.writeCredential(name, NAME_STYLE) # write name

		# WRITE TIER
		if name_length > w:
			TIER_STYLE['upper_offset'] += 100

		credential.writeCredential(type.upper(), TIER_STYLE) # write tier

		output_path = f"credentials/enei/{type}"
		output = output_path+"/"+name.lower().replace(" ", "_")+"-credential.png"
		credential.saveImage(output)
	
	return len(names)