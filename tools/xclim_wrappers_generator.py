#!/usr/bin/env python3

# (C) Copyright 2025 - ECMWF and individual contributors.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import importlib
import inspect
import textwrap
from typing import Any, List

import xclim.indicators.atmos

MODULE_TEMPLATE = """# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

\"\"\"{category_title} indices.\"\"\"

from typing import Any

import xarray
import xclim.indicators.atmos

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator

{functions_code}
"""

FUNCTION_TEMPLATE = """
def {func_name}(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    \"\"\"
    {docstring}
    \"\"\"
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.{xclim_func_name})
    return wrapper(ds, **kwargs)
"""


def generate_docstring(indicator: Any, xclim_func_name: str) -> str:
    """Generate a docstring for the wrapper function based on the xclim indicator.

    Parameters
    ----------
    indicator : xclim.core.indicator.Indicator
        The xclim indicator object.
    xclim_func_name : str
         The name of the function in xclim.indicators.atmos.

    Returns
    -------
    str
        The generated docstring for the wrapper function.
    """
    identifier = indicator.identifier.capitalize()

    # Extract metadata
    # Use title as the summary if available, otherwise fallback to docstring or identifier
    summary = getattr(indicator, "title", "").strip().capitalize()
    if not summary:
        summary = (indicator.__doc__ or "").split("\n")[0].strip()

    if not summary:
        summary = f"Compute {identifier}."

    if not summary.endswith("."):
        summary += "."

    description = getattr(indicator, "abstract", "") or getattr(indicator, "description", "")
    units = getattr(indicator, "units", "")
    outputs = getattr(indicator, "var_name", None)

    sections = [summary]

    if description:
        # Wrap the description to avoid long lines
        # We target a width of 88 to allow for indentation (4 spaces) and staying well under 110
        sections.append(textwrap.fill(description, width=88))

    # Units handling
    units_list = []
    if isinstance(units, str):
        units = units.strip()
        if not units:
            units_list = ["dimensionless"]
        else:
            units_list = [units]
    elif isinstance(units, (list, tuple)):
        units_list = [u.strip() if u else "dimensionless" for u in units]
    else:
        units_list = ["dimensionless"]

    outputs_list = []
    if isinstance(outputs, str):
        outputs_list = [outputs.strip()]
    elif isinstance(outputs, (list, tuple)):
        outputs_list = [o.strip() for o in outputs]

    units_section = ""
    lines = ["**Units:**", ""]
    for out, unit in zip(outputs_list, units_list):
        lines.append(f"- {out}: {unit}")
    units_section = "\n".join(lines)

    if units_section:
        sections.append(units_section)

    sections.append(
        f"This function wraps `xclim.indicators.atmos.{xclim_func_name} "
        f"<https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.{xclim_func_name}>`_."
    )

    # Static footer
    footer = inspect.cleandoc(f"""
        Parameters
        ----------
        ds : conversions.EarthkitData | xarray.Dataset
            Input dataset. See xclim documentation for required variables.
        **kwargs : Any
            Additional keyword arguments forwarded to
            :func:`xclim.indicators.atmos.{xclim_func_name}`.

        Returns
        -------
        conversions.EarthkitData
            The computed index as an Earthkit-compatible field.
    """)
    sections.append(footer)

    return "\n\n".join(sections)


def generate_module_content(category: str, indicators: List[Any]) -> str:
    """Generate the content for a python module containing wrapper functions.

    Parameters
    ----------
    category : str
        The category of indicators (e.g. 'precipitation', 'temperature').
    indicators : list
        List of xclim indicator objects to generate wrappers for.

    Returns
    -------
    str
        The complete source code for the module.
    """
    functions_code = []

    # Sort indicators by name for consistent output
    indicators.sort(key=lambda x: x.identifier)

    for ind in indicators:
        # We need the name of the attribute in xclim.indicators.atmos to generate the call
        xclim_func_name = None
        for name, obj in inspect.getmembers(xclim.indicators.atmos):
            if obj is ind:
                xclim_func_name = name
                break

        if not xclim_func_name:
            # Fallback
            xclim_func_name = ind.identifier

        # Use the xclim variable name as the function name to match existing conventions
        func_name = xclim_func_name

        docstring = generate_docstring(ind, xclim_func_name)

        # Indent the docstring correctly
        lines = docstring.split("\n")
        indented_doc = lines[0] + "\n" + "\n".join([("    " + line if line.strip() else "") for line in lines[1:]])

        code = FUNCTION_TEMPLATE.format(func_name=func_name, xclim_func_name=xclim_func_name, docstring=indented_doc)
        functions_code.append(code)

    return MODULE_TEMPLATE.format(category_title=category.capitalize(), functions_code="".join(functions_code))


def main():
    output_dir = importlib.resources.files("earthkit.climate.indicators")
    # Discovery
    module = xclim.indicators.atmos

    # Get all potential indicators from __all__ if present
    if hasattr(module, "__all__"):
        names = module.__all__
    else:
        # Fallback to public members
        names = [n for n, o in inspect.getmembers(module) if not n.startswith("_")]

    # Map internal xclim module names to our category names
    module_to_category = {
        "_precip": "precipitation",
        "_temperature": "temperature",
        # "_wind": "wind",
        # "_synoptic": "synoptic",
    }

    indicators_map = {cat: [] for cat in module_to_category.values()}

    for name in names:
        # We need the object to check type/attributes and pass to generation
        try:
            obj = getattr(module, name)
        except AttributeError:
            continue

        # Basic check if it is likely an indicator (has identifier)
        if not hasattr(obj, "identifier"):
            continue

        # Check which module it comes from
        # e.g. xclim.indicators.atmos._precip
        obj_module = getattr(obj, "__module__", "")
        # Extract the last part of the module path
        module_name = obj_module.split(".")[-1]

        if module_name in module_to_category:
            category = module_to_category[module_name]
            indicators_map[category].append(obj)
        else:
            print(f"Skipping {name} from unknown module {module_name}")
            continue

    for category, indicators in indicators_map.items():
        if not indicators:
            continue

        filename = f"{category}.py"
        filepath = output_dir / filename

        print(f"Generating {filepath} with {len(indicators)} indicators...")
        content = generate_module_content(category, indicators)

        with open(filepath, "w") as f:
            f.write(content)
        print(f"Written {filepath}")


if __name__ == "__main__":
    main()
