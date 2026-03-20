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

from typing import Any, Literal

import xarray
import xclim.indicators.atmos
from earthkit.utils.decorators.format_handlers import format_handler

# from earthkit.climate.utils.decorators import metadata_handler

{functions_code}
"""

FUNCTION_TEMPLATE = """
@format_handler()
# @metadata_handler({xclim_obj_ref})
def {func_name}(
{signature_params}
) -> Any:
    \"\"\"
    {docstring}
    \"\"\"
    return {xclim_obj_ref}({call_params})
"""


def simplify_type(type_obj: Any) -> str:
    """Simplify complex types to strings that can be used in the generated code."""
    if type_obj == inspect.Parameter.empty:
        return "Any"

    type_str = str(type_obj)

    # Common replacements
    replacements = {
        "xarray.core.dataarray.DataArray": "xarray.DataArray",
        "xarray.core.dataset.Dataset": "xarray.Dataset",
        "xarray.core.datatree.DataTree": "Any",
        "Quantified": "Any",  # xclim specific, hard to import reliably
        "DayOfYearStr": "str",
        "Indexer": "Any",
    }

    for old, new in replacements.items():
        type_str = type_str.replace(old, new)

    # Remove quotes
    type_str = type_str.strip("'")

    return type_str


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

    link_prefix = f"This function wraps `xclim.indicators.atmos.{xclim_func_name}"
    link_url = (
        f"<https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.{xclim_func_name}>`_."
    )
    sections.append(f"{link_prefix}\n    {link_url}")

    # Parameters section
    params_lines = [
        "Parameters",
        "----------",
    ]

    try:
        sig = inspect.signature(indicator)
        for name, param in sig.parameters.items():
            if name == "ds":
                continue

            # Skip VAR parameters as they are handled by docstring **kwargs
            if param.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                continue

            # Try to get description from indicator.parameters
            param_meta = indicator.parameters.get(name)
            description = getattr(param_meta, "description", "") if param_meta else ""

            type_hint = simplify_type(param.annotation)

            params_lines.append(f"{name} : {type_hint}")
            if description:
                # Wrap description with hanging indent
                wrapped_description = textwrap.fill(
                    description, width=88, initial_indent="    ", subsequent_indent="    "
                )
                params_lines.append(wrapped_description)
    except Exception:
        pass

    params_lines.append("ds : xarray.Dataset | Any")
    params_lines.append("    Input dataset.")
    params_lines.append("**kwargs : Any")
    params_lines.append("    Additional keyword arguments.")

    sections.append("\n".join(params_lines))

    # Returns section
    returns_section = inspect.cleandoc("""
        Returns
        -------
        Any
            The computed index.
    """)
    sections.append(returns_section)

    return "\n\n".join(sections)


def format_signature_params(indicator: Any) -> str:
    """Format the parameters for the function signature."""
    params = []

    try:
        sig = inspect.signature(indicator)

        sig_params = list(sig.parameters.values())

        pos_no_default = []
        pos_with_default = []
        kw_only = []

        for p in sig_params:
            if p.name == "ds":
                continue

            if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY):
                if p.default == inspect.Parameter.empty:
                    pos_no_default.append(p)
                else:
                    pos_with_default.append(p)
            elif p.kind == inspect.Parameter.KEYWORD_ONLY:
                kw_only.append(p)
            # Skip VAR_KEYWORD and VAR_POSITIONAL as we add our own **kwargs

        for p in pos_no_default:
            type_hint = simplify_type(p.annotation)
            params.append(f"    {p.name}: {type_hint},")

        for p in pos_with_default:
            type_hint = simplify_type(p.annotation)
            default_val = repr(p.default)
            params.append(f"    {p.name}: {type_hint} = {default_val},")

        # Add ds here
        params.append("    ds: xarray.Dataset | Any = None,")

        if kw_only:
            params.append("    *,")
            for p in kw_only:
                type_hint = simplify_type(p.annotation)
                if p.default != inspect.Parameter.empty:
                    default_val = repr(p.default)
                    params.append(f"    {p.name}: {type_hint} = {default_val},")
                else:
                    params.append(f"    {p.name}: {type_hint},")

    except Exception:
        pass

    params.append("    **kwargs: Any,")

    return "\n".join(params)


def format_call_params(indicator: Any) -> str:
    """Format the parameters for the xclim call."""
    try:
        sig = inspect.signature(indicator)
        call_args = []
        for name, param in sig.parameters.items():
            if name == "ds":
                call_args.append("ds=ds")
            elif param.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                continue  # Skip VAR parameters, they are covered by **kwargs
            else:
                call_args.append(f"{name}={name}")
        call_args.append("**kwargs")

        # If the total length is likely to exceed 88 chars (indent=4 + total), or many parameters
        total_len = sum(len(arg) for arg in call_args) + 2 * len(call_args) + 30  # 30 for the 'return xclim...' part
        if len(call_args) > 3 or total_len > 80:
            return "\n        " + ",\n        ".join(call_args) + ",\n    "

        return ", ".join(call_args)
    except Exception:
        return "ds=ds, **kwargs"


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

        signature_params = format_signature_params(ind)
        call_params = format_call_params(ind)
        xclim_obj_ref = f"xclim.indicators.atmos.{xclim_func_name}"

        code = FUNCTION_TEMPLATE.format(
            func_name=func_name,
            signature_params=signature_params,
            call_params=call_params,
            xclim_obj_ref=xclim_obj_ref,
            docstring=indented_doc,
        )
        functions_code.append(code)

    return (
        MODULE_TEMPLATE.format(category_title=category.capitalize(), functions_code="\n".join(functions_code)).rstrip()
        + "\n"
    )


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
