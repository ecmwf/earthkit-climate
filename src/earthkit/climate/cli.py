# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import click


@click.command()
@click.argument("source-file", type=click.Path(exists=True, dir_okay=False))
@click.argument("target-file", type=click.Path(exists=False, dir_okay=False))
@click.option("--tasmax", type=str, required=False, help="Name of the maximum temperature variable.")
@click.option("--thresh", type=str, required=False, help="Treshold temperature.")
@click.option("--freq", type=str, required=False, help="Resampling frequency.")
def tx_days_above(source_file, target_file, **kwargs):
    """Number of days with maximum temperature above a given threshold."""
    import earthkit.data as ekd

    import earthkit.climate as ekc

    # Fall back to indicator defaults, don't duplicate here
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    in_data = ekd.from_source("file", source_file).to_xarray()
    out_data = ekc.indicators.tx_days_above(ds=in_data, **kwargs)
    ekd.to_target("file", target_file, data=out_data)


COMMANDS = {
    "tx-days-above": tx_days_above,
}
