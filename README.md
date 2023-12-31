# credentials-writer

A small python program to write centered text into credential templates.  
The script uses the following external libraries:
- [Pillow](https://pillow.readthedocs.io/en/stable/), to generate the text for the credentials
- [ReportLab](https://docs.reportlab.com/reportlab/userguide/ch1_intro/), to generate the PDFs for printing.
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/), to merge the PDFs for printing.

It uses an approach with plugins, so you can easily add your own templates, and write any text you want into them.

## Table of contents

- [Plugins](#plugins)
  - [plugin.py](#pluginpy)
- [Credential instance](#credential-instance)
- [PDF for printing](#pdf-for-printing)
- [Usage](#usage)
- [Example](#example)

## Plugins

Plugins are located in the `/plugins` directory.  
You must provide a plugin to run the program. The folder of the plugin must have the following structure:

```
<plugin_name>
├── /templates
│   ├── front
│   └── back
├── /fonts
├── /names
└── plugin.py
```

Every plugin must have a `/templates` folder, which contains the image templates of the credentials for both the `/front` and `/back`, without any of the text you want to generate. A `/fonts` folder, which contains the fonts you want to use. And a `/names` folder, which contains the names you want to generate.  
The program has a Tier approach (for example Staff, Participant, etc.), so each **template** and **names** file must be named according to the Tier they belong to. For the Staff, you would have staff.png and staff.txt.  
The **fonts** folder must contain all the fonts you want to use inside the plugin. The fonts must be in `.ttf` format.  
The **plugin.py** file must have the code and the logic of what you want to write.

### plugin.py

The plugin file must have the function `run()`, which will be called by the program. This function is called with 3 arguments:
- `instanciator`: function that creates a new instance of a credential
- `names`: the list of names to be written in the credential
- `tier`: the tier of the credential
- `file`: the file with the list of names from a tier

Each text to be written need styling, so you have to create dicts with the styles you want to use. The dicts should have the following structure:

```python
{
	'font_size': 105, 			# size of the font in pixels
	'font': "plugins/enei/fonts/...", 	# path to the font
	'color': "#f9a31c", 			# color of the text in hex
	'upper_offset': 875, 			# offset from the top of the image in pixels
	'shadow': { 				# include if you want a shadow
		'opacity': 190 			# opacity of the shadow
	}
}
```

⚠️ The path context inside the plugin file is the root of the project. For example, to reference the fonts folder, you would use `plugins/<plugin>/fonts/...`  

An example of a plugin file can be the following, with the only requirement being the `run()` function:

```python
# definition of the styles
NAME_STYLE = {
	'font_size': 105,
	...
}

...

# any auxiliary functions you may want to use
def aux_function():
	...

...

# the function that will be called by the program
def run(new, names, tier, file):
	# maybe iterate over the names or get the lines from the file
	...

	# set the total number of credentials to be generated (for progress printing purposes)
	# here you can create a dummy instance of a credential just to set the total
	new().set_total(...)

	# create a new instance of a credential (maybe inside a loop)
	credential = new()

	# apply functions to the credential
	credential.write(text, NAME_STYLE)
	credential.save(...)
	...
```

## Credential instance

The program provides a `Credential` class, which is a wrapper of several Pillow functions that are convenient to this use case.  
An instance of this class is created with the `instanciator` function, which is passed as an argument to the `run()` function inside the plugin file (function `new()` in the example above).  
The credentials are always saved to the `/credentials/<plugin>/<tier>` folder.  
The `Credential` class has the following class methods that you can use:
- `save(filename)`: saves the credential image to credentials folder with the name provided.
- `set_total(total)`: sets the total number of credentials to be generated. This is used to calculate the progress of the program. (this is a class method that behaves like a static method)
- `shadow(text, position, style)`: writes te text as a shadow. The position is a tuple with the x and y coordinates of the text.
- `size()`: returns a typle with the width and height of the credential image.
- `text_length(text, style)`: returns the length of the text in pixels.
- `write(text, style)`: writes the text with the style provided. The position of the text is calculated automatically to be centered. If style has shadow, it will be written with a shadow.

## PDF for printing

The program allows for the generation of PDFs for printing, for both the front and back of the credential.  
The PDF files are always saved to the `/print/<plugin>/<tier>` folder.  
For each credential, three PDFs are generated:
- `<plugin>_<tier>_print<i>_front.pdf`: the front of the credential
- `<plugin>_<tier>_print<i>_back.pdf`: the back of the credential
- `<plugin>_<tier>_print<i>_merged.pdf`: both the front and back of the credential in the same file

After all credentials PDF files are generated, the program will generate a PDF file with all the credentials (front and back) in the same file, `<plugin>_<tier>_merged.pdf`.  

## Usage

1. Install the requirements:

```bash
$ pip install -r requirements.txt
```
2. Add your plugin to the `/plugins` folder

3. Run the program:

```bash
$ python3 run.py <plugin> <tier>

   plugin: 	the plugin to use from /plugins folder
   tier: 	the tier of credential, which matches the 
        	credential image name and the names file name
```

Plugin and tier arguments are mandatory. If you don't provide a file, the program will use the file with the same name as the tier.

## Example

In the plugins folder, there is an [example plugin](plugins/example), with all the files needed to run the program and generate credentials.  
The example plugin.py file has the following code:

```python
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
```

In the code above, I defined the styles for the two types of text I wanted to write, and created a simple run function that iterates over the names and generates a credential for each name. Remember that the `run()` function is mandatory, since it is the function that will be called by the program.  
To run the example plugin, you would do the following [(after installing the requirements)](#usage):

```bash
$ python3 run.py example staff
$ python3 run.py example general
```