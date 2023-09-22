NAME_STYLE = {
	'font_size': 105,
	'font': "assets/fonts/Panton-Black.ttf",
	'color': "#f9a31c",
	'upper_offset': 875,
	'shadow': {
		'opacity': 190
	}
}

def getNames(file):
	with open(file) as f:
		names = f.readlines()
	return names

def run(credentials, file, type):
	names = getNames(file)
	for name in names:
		name = name.strip()

		# handle names with more than two words
		if len(name.split()) > 2:
			name = name.split()[0] + " " + name.split()[-1]

		# write name
		credentials.writeCredential(name, f"assets/credentials/{type}.png", NAME_STYLE, f"credentials/{type}")
	
	return len(names)