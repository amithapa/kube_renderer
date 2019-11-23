#!/usr/bin/env python3.8

__author__ = "Amit Thapa <amithapa1994@gmail.com>"

from jinja2 import Environment, FileSystemLoader
import os
import yaml
import argparse


class KubeRenderer(object):
    INIT_FILE = 'init.yaml'
    CONSTANTS_FILE = 'deploy_files/files/constants.yaml'

    def __init__(self, base_directory: str = None):
        self.__base_directory = base_directory
        self.__env = None
        self.__output: str = ""
        self.__instance_status = ""
        self.__docker_image_version = ""
        self.__constants: dict = {}
        self.__setup()


    def __setup(self):
        # Setup args
        self.__setup_args()
        # Set the file loader
        file_loader = FileSystemLoader(f'{self.__base_directory}/deploy_files')
        # Setting the environment from where to load the file
        self.__env = Environment(loader=file_loader)
        # Removing the extra whitespaces.
        self.__env.trim_blocks = True
        self.__env.lstrip_blocks = True
        self.__env.rstrip_blocks = True
        self.__read_constants()


    def __setup_args(self):
        parser = argparse.ArgumentParser(description='Generate Kubernetes Deployment Files.')
        parser.add_argument('--instance_status', type=str, choices=["production", "staging"], help='Instance Status.',
                            required=True)
        parser.add_argument('--docker_image_version', type=str, help='Docker Image version.',
                            required=True)
        parser.add_argument('--base_dir', type=str, help='Base directory where your deploy_files exist',
                            required=True)

        args = parser.parse_args()
        self.__instance_status = args.instance_status
        self.__docker_image_version = args.docker_image_version
        self.__base_directory = args.base_dir

    def __read_constants(self):
        with open(f"{self.__base_directory}/{KubeRenderer.CONSTANTS_FILE}") as constants:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.__constants = yaml.load(constants, Loader=yaml.FullLoader)
        self.__constants.update(
            {
                "deploy_env_status": self.__instance_status,
                "docker_image_version": self.__docker_image_version,
            }
        )

    def __render(self):
        # Rendering the template
        template = self.__env.get_template(KubeRenderer.INIT_FILE)
        self.__output = template.render(constants=self.__constants)
        print(self.__output)

    def run(self):
        self.__render()

def main():
    KubeRenderer().run()

if __name__ == "__main__":
    main()
