import os
import sys
import credentials
from print import print_a6_in_a4

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

def progress_bar(progress, total):
	print(f"\r[{'='*int(progress/total*50):50}] {progress}/{total} {int(progress/total*100)}%", end="")
	if progress == total:
		print("")

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

		print(f"Plugin: {plugin_name}\nTier: '{tier}'\nFile: '{file}'\nGenerating credentials...")

		# set total credentials to be generated
		credentials.Credential.progress = 0

		# run plugin
		plugin.run(
			lambda: credentials.Credential(f"plugins/{plugin_name}/templates/{tier}.png"),
			file,
			tier
		)

		# if n_gen exists, print how many credentials were generated
		if credentials.Credential.progress > 0:
			print(f"Generated {credentials.Credential.progress} credentials.")

		print("\n")

		# generate print pdfs
		images = [f"credentials/{plugin_name}/{tier}/{file}" for file in os.listdir(f"credentials/{plugin_name}/{tier}") if file.endswith(".png")]
		prints = len(images)//4
		print(f"Generating print PDF files...")

		# create folder print if it doesn't exist
		if not os.path.exists(f"print/{plugin_name}/{tier}"):
			os.makedirs(f"print/{plugin_name}/{tier}")

		for i in range(0, len(images), 4):
			print_a6_in_a4(images[i:i+4], f"{plugin_name}/{tier}/{plugin_name}_{tier}_print{i//4}.pdf")
			progress_bar((i+4)//4, prints)

		print(f"Generated {prints} print PDF files.\n")
		print("Done.")

if __name__ == "__main__":
	main()