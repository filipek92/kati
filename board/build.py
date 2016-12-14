#!/usr/bin/env python3

import click
from glob import glob
from shutil import rmtree
from os import mkdir, rename, remove

@click.command()
def main():
	for name in glob("*.*i"):
		print("Removing "+name)
		remove(name)

	for name in glob("*.gbr")+glob("*.exc"):
		print("Moving {} to {}".format(name, "gerber/"+name));
		rename(name, 'gerber/'+name)



	for name in glob("*.[sb]#[0-9]"):
		print("Removing "+name)
		remove(name)

if __name__ == '__main__':
	main()