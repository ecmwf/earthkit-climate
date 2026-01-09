# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from pytest_mock import MockerFixture

from earthkit.climate.indicators import temperature


class MockEarthkitData:
    """Mock object for Earthkit input."""

    pass


def test_daily_temperature_range(mocker: MockerFixture, common_mocks):
    """Test daily_temperature_range calls wrapper with merged dataset."""
    # Mock the wrapper creator and the wrapped function
    mock_wrapper_factory = mocker.patch("earthkit.climate.indicators.temperature.wrap_xclim_indicator")
    mock_wrapped_fn = mocker.MagicMock()
    mock_wrapper_factory.return_value = mock_wrapped_fn

    # Call function with single dataset
    ds_in = MockEarthkitData()
    temperature.daily_temperature_range(ds_in, arg="val")

    # Verify wrapper created with correct xclim function
    import xclim.indicators.atmos

    mock_wrapper_factory.assert_called_once_with(xclim.indicators.atmos.daily_temperature_range)

    # Verify wrapped function called with the dataset
    call_args = mock_wrapped_fn.call_args
    assert call_args is not None
    ds_arg = call_args[0][0]
    # The wrapper receives the raw input, conversion happens inside the wrapper (which is mocked)
    assert ds_arg is ds_in
    assert call_args.kwargs["arg"] == "val"


def test_heating_degree_days(mocker: MockerFixture, common_mocks):
    """Test heating_degree_days calls wrapper with merged dataset."""
    mock_wrapper_factory = mocker.patch("earthkit.climate.indicators.temperature.wrap_xclim_indicator")
    mock_wrapped_fn = mocker.MagicMock()
    mock_wrapper_factory.return_value = mock_wrapped_fn

    ds_in = MockEarthkitData()

    temperature.heating_degree_days(ds_in, thresh="18 degC")

    import xclim.indicators.atmos

    mock_wrapper_factory.assert_called_once_with(xclim.indicators.atmos.heating_degree_days)

    call_args = mock_wrapped_fn.call_args
    ds_arg = call_args[0][0]
    assert ds_arg is ds_in
    assert call_args.kwargs["thresh"] == "18 degC"


def test_warm_spell_duration_index(mocker: MockerFixture, common_mocks):
    """Test warm_spell_duration_index passes merged dataset (tasmax + tasmax_per)."""
    # Mock wrapper factory
    mock_wrapper_factory = mocker.patch("earthkit.climate.indicators.temperature.wrap_xclim_indicator")
    mock_wrapped_fn = mocker.MagicMock()
    mock_wrapper_factory.return_value = mock_wrapped_fn

    # Create a dummy input that represents a merged dataset
    ds_merged_in = MockEarthkitData()

    # Call with single merged input
    temperature.warm_spell_duration_index(ds_merged_in, window=10)

    import xclim.indicators.atmos

    mock_wrapper_factory.assert_called_once_with(xclim.indicators.atmos.warm_spell_duration_index)

    # Verify call args
    mock_wrapped_fn.assert_called_once()
    call_kwargs = mock_wrapped_fn.call_args.kwargs

    # We assume the first positional arg is handled by the wrapper as 'earthkit_input'
    # Check positional args first
    if mock_wrapped_fn.call_args.args:
        assert mock_wrapped_fn.call_args.args[0] is ds_merged_in
    else:
        # Fallback if passed as keyword
        # (though wrapper signature might not support it yet, test logic verifies call)
        # In this test we called it positionally.
        pass

    assert call_kwargs["window"] == 10
    # Ensure reference_data is NOT passed
    assert "reference_data" not in call_kwargs
