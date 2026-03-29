import re
import io
from aztec_code_generator import AztecCode
import datetime


def read_pass_strings(strings_file: io.TextIOBase):
    strings = {}
    for line_idx, line in enumerate(strings_file.readlines()):
        line = line.decode('UTF-8')
        localisation_string_regex = re.search(r'^"(.*)" = "(.*)";$', line)
        if localisation_string_regex:
            if localisation_string_regex.group(1) in strings:
                raise ValueError(
                    f"Localisation string '{localisation_string_regex.group(1)}' duplicated on line {line_idx}"
                )
            strings[localisation_string_regex.group(1)] = (
                localisation_string_regex.group(2)
            )
        else:
            if line != "\n":
                raise ValueError(
                    f"Localisation string on line {line_idx} does not match expected format"
                )
    return strings


def barcode_to_svg(barcode_type, barcode):
    if barcode_type == "PKBarcodeFormatAztec":
        aztec_code = AztecCode(barcode)
        d = ""
        for y, line in enumerate(aztec_code.matrix):
            dx = 0
            x0 = None
            for x, char in enumerate(line):
                if char == 1:
                    dx += 1
                    if x0 is None:
                        x0 = x
                if x0 is not None and (x + 1 >= len(line) or line[x + 1]) == 0:
                    d += f" M{x0} {y} h{dx}"
                    dx = 0
                    x0 = None
        size = len(aztec_code.matrix[0])
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><rect x="0" y="0" width="{size}" height="{size}" fill="white" /><path d="{d[1:]} Z" stroke="black" stroke-width="1" style="transform:translateY(0.5px);" /></svg>'
    elif barcode_type == "PKBarcodeFormatPDF417":
        raise NotImplementedError("PKBarcodeFormatPDF417 not implemented yet")
    elif barcode_type == "PKBarcodeFormatQR":
        raise NotImplementedError("PKBarcodeFormatQR not implemented yet")
    elif barcode_type == "PKBarcodeFormatCode128":
        raise NotImplementedError("PKBarcodeFormatCode128 not implemented yet")
    else:
        raise ValueError('invalid barcode type')


def render_value(pass_field, localisation = {}):
    if "dateStyle" in pass_field or "timeStyle" in pass_field:
        dt_date = None
        dt_time = None
        value_dt = datetime.datetime.fromisoformat(pass_field["value"])
        if "dateStyle" in pass_field:
            if pass_field["dateStyle"] == "PKDateStyleNone":
                pass
            elif pass_field["dateStyle"] == "PKDateStyleShort":
                raise NotImplementedError(
                    "please check how PKDateStyleShort is displayed and remove this raise"
                )
            elif pass_field["dateStyle"] == "PKDateStyleMedium":
                # DD-MM-YYYY
                dt_date = value_dt.strftime("%d-%m-%Y")
            elif pass_field["dateStyle"] == "PKDateStyleLong":
                raise NotImplementedError(
                    "please check how PKDateStyleLong is displayed and remove this raise"
                )
            else:
                raise ValueError(f"unknown dateStyle {pass_field['dateStyle']}")

        if "timeStyle" in pass_field:
            if pass_field["timeStyle"] == "PKDateStyleNone":
                pass
            elif pass_field["timeStyle"] == "PKDateStyleShort":
                dt_time = value_dt.strftime("%H:%M")
            elif pass_field["timeStyle"] == "PKDateStyleMedium":
                raise NotImplementedError(
                    "please check how PKDateStyleMedium is displayed and remove this raise"
                )
            elif pass_field["timeStyle"] == "PKDateStyleLong":
                raise NotImplementedError(
                    "please check how PKDateStyleLong is displayed and remove this raise"
                )
            else:
                raise ValueError(f"unknown timeStyle {pass_field['timeStyle']}")

        if dt_date and dt_time:
            return f"{dt_date} {dt_time}"
        elif dt_date:
            return dt_date
        else:
            return dt_time
    else:
        if pass_field["value"] in localisation:
            return localisation[pass_field["value"]]
        else:
            return pass_field["value"]


def render_label(pass_field, localisation = {}):
    if pass_field["label"] in localisation:
        return localisation[pass_field["label"]]
    else:
        return pass_field["label"]
