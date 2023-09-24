NAME_STYLE = {
	'font_size': 105,
	'font': "plugins/example/fonts/Panton-Black.ttf",
	'color': "#ffffff",
	'upper_offset': 400,
	'shadow': {
		'opacity': 190
	}
}

TIER_STYLE = {
	'font_size': 85,
	'font': "plugins/example/fonts/Montserrat-Regular.ttf",
	'color': "#ffffff",
	'upper_offset': 600,
}


def run(new, names, tier, file):
	# set total credentials to be generated
	new().set_total(len(names))

	# change the style of the name depending on the tier
	if tier == "staff":
		NAME_STYLE['color'] = "#343deb"

	# iterate over the names and generate credentials
	for i, name in enumerate(names):
		name = name.upper().strip()
		
		credential = new()
		credential.write(name, NAME_STYLE) # write the name
		credential.write(tier, TIER_STYLE) # write the tier
		credential.save(f"{name.lower().replace(' ', '_')}-credential-{i}")