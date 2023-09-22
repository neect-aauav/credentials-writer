import os
import sys
import credentials

def load_plugin(plugin_name):
	# check if plugin exists
	if not os.path.exists(f"plugins/{plugin_name}/plugin.py"):
		print(f"Plugin '{plugin_name}' not found.\n")
		return

	# import plugin
	import importlib.util
	spec = importlib.util.spec_from_file_location(plugin_name, f"plugins/{plugin_name}/plugin.py")
	plugin = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(plugin)

	return plugin

def showHelp(program_name):
	print(f"Usage: python3 {program_name} <plugin> <tier> [file]")
	print("   plugin: \tthe plugin to use from /plugins folder")
	print("   tier: \tthe tier of credential, which matches the \n        \tcredential image name and the names file name")
	print("   file: \tpath to file with names (optional)")

def main():
	args = sys.argv[1:]

	# display help
	if len(args) <= 1 or (len(args) == 1 and (args[0].startswith("-") or args[0].startswith("--"))):
		showHelp(sys.argv[0])	
		return

	if len(args) > 0:
		plugin_name = args[0]
		plugin = load_plugin(plugin_name)
		if not plugin:
			showHelp(sys.argv[0])
			return

		tier = args[1]
		file = f"plugins/{plugin_name}/names/{tier}.txt"
		if len(args) == 3:
			file = args[2]
			
		if not os.path.exists(file):
			print(f"File '{file}' not found.\n")
			showHelp(sys.argv[0])
			return

		print(f"Generating credentials for '{tier}' from file '{file}'...")

		# run plugin
		n_gen = plugin.run(
			lambda: credentials.Credential(f"plugins/{plugin_name}/templates/{tier}.png"),
			file,
			tier
		)

		# if n_gen exists, print how many credentials were generated
		if n_gen:
			print(f"Generated {n_gen} credentials.")

if __name__ == "__main__":
	main()