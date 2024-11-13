import json
import os
from docx import Document
from docx.shared import Cm, Mm, Inches, Pt
import shutil

from services.mistake import Mistake


def get_json_spec(style_name: str) -> dict:
    with open(f"specifications/{style_name.lower()}.json", "r") as file:
        data = json.load(file)
    return data


def convert_to_emu(value_str):
    try:
        value = float(value_str[:-2])
        unit = value_str[-2:].lower()
    except ValueError:
        raise ValueError("Invalid format. Please provide a value with units like '12cm', '5inch', or '10mm'.")

    if unit == "cm":
        emu_value = Cm(value)
    elif unit == "mm":
        emu_value = Mm(value)
    elif unit == "in":
        emu_value = Inches(value)
    elif unit == "pt":
        emu_value = Pt(value)
    else:
        raise ValueError("Unsupported unit. Use 'cm', 'mm', or 'in'.")

    return emu_value


def convert_to_emu_dict(dictionary: dict):
    for key, value in dictionary.items():
        dct_value = value

        if type(value) == str and any(value.endswith(unit) for unit in ["cm", "mm", "in", "pt"]):
            dct_value = convert_to_emu(value)

        dictionary[key] = dct_value

    return dictionary


def catch_section_mistakes(doc: Document, spec: dict):
    mistakes = {}
    spec = spec["document"]["layout"]

    for number, section in enumerate(doc.sections):
        margins = convert_to_emu_dict(spec)
        mistakes_section = []

        for margin in margins.keys():
            word_margin = getattr(section, margin)
            if word_margin != margins[margin]:
                mistakes_section.append(
                    Mistake(margin, margins[margin], word_margin).to_dict()
                )

        if mistakes_section:
            mistakes[number] = mistakes_section

    return mistakes


def catch_style_mistakes(doc: Document, spec: dict):
    mistakes = {}
    spec = spec["document"]["styles"]

    for number, style in enumerate(doc.styles):
        if style.name not in spec.keys():
            continue

        mistakes_style = {}
        spec_style = spec[style.name]

        for target in spec_style.keys():
            style_deep = getattr(style, target)
            spec_style_target = convert_to_emu_dict(spec_style[target])

            for parameter in spec_style_target:
                doc_parameter = getattr(style_deep, parameter)

                if doc_parameter != spec_style_target[parameter]:
                    mistakes_style[target] = Mistake(parameter, spec_style_target[parameter], doc_parameter).to_dict()

        if mistakes_style:
            mistakes[number] = mistakes_style

    return mistakes


def catch_format_mistakes(file_path: str, style_spec: str) -> dict:
    doc = Document(file_path)
    spec = get_json_spec(style_spec)
    mistakes = {}

    mistakes_sections = catch_section_mistakes(doc, spec)

    if mistakes_sections:
        mistakes["sections"] = mistakes_sections

    mistakes_styles = catch_style_mistakes(doc, spec)

    if mistakes_styles:
        mistakes["styles"] = mistakes_styles

    return mistakes


def create_word_file_mistakes(file_path: str, word_style: str = "APA") -> dict:
    directory, filename = os.path.split(file_path)
    base_name, ext = os.path.splitext(filename)

    json_name = base_name + "-mst" + ".json"
    json_path = os.path.join(directory, json_name)

    mistakes = catch_format_mistakes(file_path, word_style)

    mistakes["file_path"] = file_path
    mistakes["word_style"] = word_style

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(mistakes, file, ensure_ascii=False, indent=4)

    return {"filename": json_name, "file_path": json_path}


def copy_file(file_path):
    directory, filename = os.path.split(file_path)
    base_name, ext = os.path.splitext(filename)
    new_name = base_name + "-new" + ext

    copy_path = os.path.join(directory, new_name)

    print(copy_path)

    shutil.copy(file_path, copy_path)

    return {
        "original_path": file_path,
        "copy_path": copy_path
    }


def fix_section_mistakes(doc: Document, mistakes: dict):
    sections = doc.sections

    for number in mistakes.keys():
        mistakes_section = mistakes[number]
        section = sections[int(number)]

        for mistake in mistakes_section:
            setattr(section, mistake["parameter"], mistake["correct"])


def fix_style_mistakes(doc: Document, mistakes: dict):
    styles = list(doc.styles)

    for number in mistakes.keys():
        style = styles[int(number)]

        for target, mistake in mistakes[number].items():
            style_target = getattr(style, target)
            setattr(style_target, mistake["parameter"], mistake["correct"])


def fix_format_mistakes(file_path: str, mistakes: dict):
    doc = Document(file_path)

    mistakes_section = mistakes["sections"]
    mistakes_style = mistakes["styles"]

    fix_section_mistakes(doc, mistakes_section)
    fix_style_mistakes(doc, mistakes_style)

    doc.save(file_path)
