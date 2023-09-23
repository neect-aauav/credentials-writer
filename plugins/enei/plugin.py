NAME_STYLE = {
	'font_size': 105,
	'font': "plugins/enei/fonts/Panton-Black.ttf",
	'color': "#f9a31c",
	'upper_offset': 875,
	'shadow': {
		'opacity': 190
	}
}

TIER_STYLE = {
	'font_size': 85,
	'font': "plugins/enei/fonts/Panton-Black.ttf",
	'color': "#ffffff",
	'upper_offset': 1050,
	'shadow': {
		'opacity': 190
	}
}

NAME_MARGIN = 100

def getLines(file):
	with open(file) as f:
		lines = f.readlines()
	return lines

def compactName(name):
	# handle names with more than two words
	if len(name.split()) > 2:
		name = name.split()[0] + " " + name.split()[-1]
	return name

def saveCredential(credential, file_name):
	output_path = "credentials/enei"
	output = f"{output_path}/{file_name}.png"
	credential.save(output)

def writeCredential(credential, name, title):
	w, h = credential.size()

	# WRITE NAME
	name_length = credential.text_length(name, NAME_STYLE)
	name_style = NAME_STYLE.copy()
	title_style = TIER_STYLE.copy()
	# if name is too long, break it into two lines
	long_name = name_length > w-NAME_MARGIN*2
	if long_name:
		splitted = name.split()
		
		credential.write(splitted[0], name_style) # write first name
		name_style['upper_offset'] += 100
		credential.write(splitted[1], name_style) # write second name

		title_style['upper_offset'] += 100
	else:
		credential.write(name, name_style) # write name

	# WRITE TITLE
	credential.write(title, title_style) # write tier

	return credential

def regularCredential(new, file, tier):
	names = getLines(file)

	# set total credentials to be generated
	new().set_total(len(names))

	for name in names:
		name = compactName(name).upper().strip()
		credential = writeCredential(new(), name, tier.upper())
		saveCredential(credential, f"{tier}/{name.lower().replace(' ', '_')}-credential")

def empresaCredencial(new, file, tier):
	lines = getLines(file)

	# count number of credentials to be generated
	new().set_total(len([line for line in lines if line[0] != "-"]))

	empresa = ""
	for line in lines:
		if line[0] == "-":
			empresa = line[1:].strip().upper()
			continue

		name = compactName(line).upper().strip()
		credential = writeCredential(new(), name, empresa)
		saveCredential(credential, f"{tier}/{empresa.lower().replace(' ', '_')}-{name.lower().replace(' ', '_')}-credential")

def run(new, file, tier):
	if tier != "empresa":
		if tier == "participante":
			del NAME_STYLE['shadow']
			del TIER_STYLE['shadow']

			TIER_STYLE["color"] = "#000000"

		regularCredential(new, file, tier)
	
	else:
		empresaCredencial(new, file, tier)