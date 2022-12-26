from yaml.loader import BaseLoader
from dotenv import load_dotenv
from deepl import Translator
import yaml
import os


def main():
    with open("./input.yml", "r") as input_file:
        data = yaml.load(input_file, Loader=BaseLoader)

    destruct_and_translate(data)
    first_key = list(data.items())[0][0]
    data[language_key] = data.pop(first_key)

    with open("./output.yml", "w") as output_file:
        recursive_write(data, output_file)


def recursive_write(data: dict, file: any, indentation_level: int = 0) -> None:
    indent = " " * indentation_level
    for key, value in data.items():
        if isinstance(value, str):
            file.write(f"{indent}{key}: {value}\n")
        else:
            file.write(f"{indent}{key}:\n")
            recursive_write(value, file, indentation_level + 2)


def destruct_and_translate(data: dict) -> None:
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = translator.translate_text(value, target_lang=deepl_target).text
        else:
            destruct_and_translate(value)


if __name__ == '__main__':
    load_dotenv()
    translator = Translator(os.getenv("AUTH_KEY"))
    language_key = input("Language key for the translated yml ")
    deepl_target = input("Target lang for deepl. Leave blank to use language key above ") or language_key

    main()
