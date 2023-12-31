import os
import sys
import math
import lib.credentials as credentials
from lib.print import print_a6_in_a4, merge_a4

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
	print(f"Usage: python3 {program_name} <plugin> <tier>")
	print("   plugin: \tthe plugin to use from /plugins folder")
	print("   tier: \tthe tier of credential, which matches the \n        \tcredential image name and the names file name")

def progress_bar(progress, total):
	print(f"\r[{'='*int(progress/total*50):50}] {progress}/{total} {int(progress/total*100)}%", end="")
	if progress >= total:
		print("")

def getSize(paths):
	size = 0
	for path in paths:
		size += os.path.getsize(path)

	return size/1024/1024 # convert to MB

def getLines(file):
	with open(file) as f:
		lines = f.readlines()
	
	# ignore #coments and empty lines
	return [line for line in lines if line[0] != "#" and line.strip() != ""]

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

		credentials.Credential.plugin = plugin_name
		credentials.Credential.tier = tier
			
		if not os.path.exists(file):
			print(f"File '{file}' not found.\n")
			showHelp(sys.argv[0])
			return

		credentials_path = f"credentials/{plugin_name}/{tier}"
		# create folders for credentials if they don't exist
		if not os.path.exists(credentials_path):
			os.makedirs(credentials_path)

		print(f"Plugin:   {plugin_name}\nTier:     {tier}\nNames:    {file}")

		print("\nGenerating credentials...")
		# set total credentials to be generated
		credentials.Credential.progress = 0
		
		# run plugin
		plugin.run(
			lambda: credentials.Credential(f"plugins/{plugin_name}/templates/front/{tier}.png"),
			getLines(file),
			tier,
			file,
		)

		# if n_gen exists, print how many credentials were generated
		if credentials.Credential.progress > 0:
			print("Generated credentials\n")
			print(f"Saved:    {credentials.Credential.progress}\nFolder:   {credentials_path}\nSize:     {getSize(credentials.Credential.saved):.2f} MB\n")

		print("")

		# generate print pdfs
		images = [credentials for credentials in credentials.Credential.saved]
		prints = math.ceil(len(images)/4)*3+1 # front, back, merge per credential and merge all
		print(f"Pages: [front, back, merge, merge all]\nGenerating print PDF files...")

		# create folders for print if they don't exist
		path = f"{plugin_name}/{tier}"
		print_path = f"print/{path}"
		if not os.path.exists(print_path):
			os.makedirs(print_path)

		saved_pdfs = []
		progress = 0
		progress_bar(0, prints)
		for i in range(0, len(images), 4):
			index = i//4

			# front
			front = f"{plugin_name}_{tier}_print{index}_front.pdf"
			print_a6_in_a4(images[i:i+4], f"{path}/{front}")
			saved_pdfs.append(f"{print_path}/{front}")
			progress_bar(progress+1, prints)

			# back
			back = f"{plugin_name}_{tier}_print{index}_back.pdf"
			print_a6_in_a4([f"plugins/{plugin_name}/templates/back/{tier}.png"]*4, f"{path}/{back}")
			saved_pdfs.append(f"{print_path}/{back}")
			progress_bar(progress+2, prints)

			# merge front and back
			merge = f"{plugin_name}_{tier}_print{index}_merged.pdf"
			merge_a4([f"{print_path}/{front}", f"{print_path}/{back}"], f"{path}/{merge}")
			saved_pdfs.append(f"{print_path}/{merge}")
			progress_bar(progress+3, prints)

			progress += 3

		# merge all prints
		merge_a4([pdf for pdf in saved_pdfs if "merged" not in pdf], f"{path}/{plugin_name}_{tier}_merged.pdf")
		saved_pdfs.append(f"{print_path}/{plugin_name}_{tier}_merged.pdf")
		progress+=1
		progress_bar(progress, prints)

		print("Generated print PDF files\n")
		print(f"Saved:    {prints}\nFolder:   {print_path}\nSize:     {getSize(saved_pdfs):.2f} MB\n")
		print("\nDone.")

if __name__ == "__main__":
	main()