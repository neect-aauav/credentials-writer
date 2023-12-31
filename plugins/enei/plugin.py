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

def compactName(name):
	# handle names with more than two words
	if len(name.split()) > 2:
		name = name.split()[0] + " " + name.split()[-1]
	return name

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

def onlyTierCredential(new, tier, times):
	# set total credentials to be generated
	new().set_total(times)

	for i in range(times):
		credential = writeCredential(new(), "", tier.upper())
		credential.save(f"{tier.lower().replace(' ', '_')}-credential-{i}")

def regularCredential(new, names, tier):
	# set total credentials to be generated
	new().set_total(len(names))

	for i, name in enumerate(names):
		name = compactName(name).upper().strip()
		credential = writeCredential(new(), name, tier.upper())
		credential.save(f"{name.lower().replace(' ', '_')}-credential-{i}")

def empresaCredencial(new, lines):
	# count number of credentials to be generated
	new().set_total(len([line for line in lines if line[0] != "-"]))

	empresa = ""
	for i, line in enumerate(lines):
		if line[0] == "-":
			empresa = line[1:].upper().strip()
			continue

		name = compactName(line).upper().strip()
		credential = writeCredential(new(), name, empresa)
		credential.save(f"{empresa.lower().replace(' ', '_')}-{name.lower().replace(' ', '_')}-credential-{i}")

def run(new, names, tier, file):
	if names[0].startswith("type=") and 'generic' in names[0].replace("type=", ""):
		times = int(names[1].replace("times=", ""))
		onlyTierCredential(new, tier, times)
		return

	if tier != "empresa":
		if tier == "participante":
			del NAME_STYLE['shadow']
			del TIER_STYLE['shadow']

			TIER_STYLE["color"] = "#000000"

		regularCredential(new, names, tier)
	
	else:
		empresaCredencial(new, names)