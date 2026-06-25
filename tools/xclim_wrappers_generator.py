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

import xclim.indicators

MODULE_TEMPLATE = """# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

\"\"\"{category_title} indices.\"\"\"

from typing import Any, Literal

import xarray
import xclim.indicators.{module_name}
from earthkit.utils.decorators import format_handler

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
    """Simplify complex types to strings that can be used in the generated code.

    Parameters
    ----------
    type_obj : Any
        The type object to simplify.

    Returns
    -------
    str
        The simplified type representation as a string.
    """
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
        "DateStr": "str",
        "rv_continuous": "Any",
        "Indexer": "Any",
    }

    for old, new in replacements.items():
        type_str = type_str.replace(old, new)

    # Remove quotes
    type_str = type_str.strip("'")

    return type_str


def generate_docstring(indicator: Any, module_name: str, xclim_func_name: str) -> str:
    """Generate a docstring for the wrapper function based on the xclim indicator.

    Parameters
    ----------
    indicator : xclim.core.indicator.Indicator
        The xclim indicator object.
    module_name : str
        The xclim module name (e.g. 'atmos', 'land').
    xclim_func_name : str
         The name of the function in xclim.indicators.<module_name>.

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

    link_text = f"xclim.indicators.{module_name}.{xclim_func_name}"
    link_url = f"https://xclim.readthedocs.io/en/stable/api_indicators.html#{link_text}"
    sections.append(f"This function wraps `{link_text} <{link_url}>`_.")

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
    """Format the parameters for the function signature.

    Parameters
    ----------
    indicator : Any
        The xclim indicator object.

    Returns
    -------
    str
        The formatted signature parameters.
    """
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
            if isinstance(p.default, str) and "'" in default_val and '"' not in default_val:
                default_val = f'"{p.default}"'
            params.append(f"    {p.name}: {type_hint} = {default_val},")

        # Add ds here
        params.append("    ds: xarray.Dataset | Any = None,")

        if kw_only:
            params.append("    *,")
            for p in kw_only:
                type_hint = simplify_type(p.annotation)
                if p.default != inspect.Parameter.empty:
                    default_val = repr(p.default)
                    if isinstance(p.default, str) and "'" in default_val and '"' not in default_val:
                        default_val = f'"{p.default}"'
                    params.append(f"    {p.name}: {type_hint} = {default_val},")
                else:
                    params.append(f"    {p.name}: {type_hint},")

    except Exception:
        pass

    params.append("    **kwargs: Any,")

    return "\n".join(params)


def format_call_params(indicator: Any) -> str:
    """Format the parameters for the xclim call.

    Parameters
    ----------
    indicator : Any
        The xclim indicator object.

    Returns
    -------
    str
        The formatted call parameters.
    """
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


def generate_module_content(category: str, module_name: str, indicators: List[Any]) -> str:
    """Generate the content for a python module containing wrapper functions.

    Parameters
    ----------
    category : str
        The category of indicators (e.g. 'precipitation', 'temperature').
    module_name : str
        The xclim module name (e.g. 'atmos', 'land').
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

    # Get the xclim module to find function names
    xclim_module = getattr(xclim.indicators, module_name)

    for ind in indicators:
        # We need the name of the attribute in xclim.indicators.<module_name> to generate the call
        xclim_func_name = None
        for name, obj in inspect.getmembers(xclim_module):
            if obj is ind:
                xclim_func_name = name
                break

        if not xclim_func_name:
            # Fallback
            xclim_func_name = ind.identifier

        # Use the xclim variable name as the function name to match existing conventions
        func_name = xclim_func_name

        docstring = generate_docstring(ind, module_name, xclim_func_name)

        # Indent the docstring correctly
        lines = docstring.split("\n")
        indented_doc = lines[0] + "\n" + "\n".join([("    " + line if line.strip() else "") for line in lines[1:]])

        signature_params = format_signature_params(ind)
        call_params = format_call_params(ind)
        xclim_obj_ref = f"xclim.indicators.{module_name}.{xclim_func_name}"

        code = FUNCTION_TEMPLATE.format(
            func_name=func_name,
            signature_params=signature_params,
            call_params=call_params,
            xclim_obj_ref=xclim_obj_ref,
            docstring=indented_doc,
        )
        functions_code.append(code)

    return (
        MODULE_TEMPLATE.format(
            category_title=category.capitalize(),
            module_name=module_name,
            functions_code="\n".join(functions_code),
        ).rstrip()
        + "\n"
    )


def _collect_categories(module_name: str) -> dict[str, list[Any]]:
    """Collect indicators by category from an xclim indicator module.

    Parameters
    ----------
    module_name : str
        The xclim module name (e.g. 'atmos', 'land', 'seaIce').

    Returns
    -------
    dict[str, list[Any]]
        Mapping from category name to list of xclim indicator objects.
    """
    try:
        module = importlib.import_module(f"xclim.indicators.{module_name}")
    except ImportError:
        print(f"Skipping xclim.indicators.{module_name} (not found)")
        return {}

    if hasattr(module, "__all__"):
        names = module.__all__
    else:
        names = [n for n, o in inspect.getmembers(module) if not n.startswith("_")]

    module_to_category = {
        "_precip": "precipitation",
        "_temperature": "temperature",
        "_wind": "wind",
        "_synoptic": "synoptic",
        "_conversion": "precipitation",
        "_snow": "snow",
        "_streamflow": "hydrology",
        "_seaice": "sea_ice",
    }

    indicators_map: dict[str, list[Any]] = {}

    for name in names:
        try:
            obj = getattr(module, name)
        except AttributeError:
            continue

        if not hasattr(obj, "identifier"):
            continue

        obj_module = getattr(obj, "__module__", "")
        submodule_name = obj_module.split(".")[-1]

        if submodule_name in module_to_category:
            category = module_to_category[submodule_name]
        else:
            keywords = getattr(obj, "keywords", "")
            if "precipitation" in keywords or "snow" in keywords or "rain" in keywords:
                category = "precipitation"
            elif "temperature" in keywords or "heat" in keywords or "cold" in keywords:
                category = "temperature"
            else:
                category = module_name

        if category not in indicators_map:
            indicators_map[category] = []
        indicators_map[category].append(obj)

    return indicators_map


def generate_for_module(
    module_name: str, output_dir: Any, all_categories: set[str] | None = None
) -> set[str]:
    """Generate category .py files in a single indicators directory.

    Parameters
    ----------
    module_name : str
        The xclim module name (e.g. 'atmos', 'land', 'seaIce').
    output_dir : Any
        The path-like directory where category .py files are written.
    all_categories : set[str] | None
        Accumulator for all categories generated across modules.

    Returns
    -------
    set[str]
        Updated set of all category names produced.
    """
    if all_categories is None:
        all_categories = set()

    indicators_map = _collect_categories(module_name)
    if not indicators_map:
        return all_categories

    for category, indicators in indicators_map.items():
        all_categories.add(category)

        filename = f"{category}.py"
        filepath = output_dir / filename

        print(f"Generating {filepath} with {len(indicators)} indicators...")
        content = generate_module_content(category, module_name, indicators)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Written {filepath}")

    return all_categories


def main() -> None:
    """Run the wrapper generator to generate climate index modules.

    This function locates the target indicators package directory using
    pathlib and triggers the generation for atmos, land, and seaIce
    indicators, writing everything flat into indicators/.

    Returns
    -------
    None
    """
    import pathlib

    output_dir = pathlib.Path(__file__).parent.parent / "src" / "earthkit" / "climate" / "indicators"
    output_dir.mkdir(exist_ok=True, parents=True)

    xclim_modules = ["atmos", "land", "seaIce"]

    all_categories: set[str] = set()
    for module_name in xclim_modules:
        all_categories = generate_for_module(module_name, output_dir, all_categories)

    # Generate single __init__.py that imports all category modules
    init_path = output_dir / "__init__.py"
    categories = sorted(all_categories)
    init_content = "# (C) Copyright 2025 - ECMWF and individual contributors.\n\n"
    init_content += '"""Climate indicators."""\n\n'
    for cat in categories:
        init_content += f"from earthkit.climate.indicators.{cat} import *  # noqa\n"

    with open(init_path, "w") as f:
        f.write(init_content)
    print(f"Generated {init_path} with {len(categories)} modules")


if __name__ == "__main__":
    main()
