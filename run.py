import os
import sys
import credentials as credentials

def load_plugin(plugin_name):
	# check if plugin exists
	if not os.path.exists("plugins/"+plugin_name+".py"):
		print(f"Plugin '{plugin_name}' not found.\n")
		showHelp(sys.argv[0])
		return

	# import plugin
	import importlib.util
	spec = importlib.util.spec_from_file_location(plugin_name, "plugins/"+plugin_name+".py")
	plugin = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(plugin)

	return plugin

def showHelp(program_name):
	print(f"Usage: python3 {program_name} <plugin> <type> [file]")
	print("   plugin: \tthe plugin to use from /plugins folder")
	print("   type: \tthe type of credential, which matches the \n        \tcredential image name and the names file name")
	print("   file: \tpath to file with names (optional)")

def main():
	args = sys.argv[1:]

	# display help
	if len(args) == 0 or (len(args) == 1 and (args[0].startswith("-") or args[0].startswith("--"))):
		showHelp(sys.argv[0])	
		return

	# handle arguments
	if len(args) > 0:
		plugin_name = args[0]
		type = args[1]
		file = "names/"+type+".txt"
		if len(args) == 3:
			file = args[2]
		
	print(f"Generating credentials for '{type}' from file '{file}'...")

	if not os.path.exists(file):
		print(f"File '{file}' not found.\n")
		showHelp(sys.argv[0])
		return

	# run plugin
	plugin = load_plugin(plugin_name)
	n_gen = plugin.run(credentials, file, type)

	# if n_gen exists, print how many credentials were generated
	if n_gen:
		print(f"Generated {n_gen} credentials.")

if __name__ == "__main__":
	main()