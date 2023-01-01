"""
Test generalized adjoint source generation for each type
"""
import pytest
import numpy as np
from pyadjoint import calculate_adjoint_source, get_config
from pyadjoint import get_example_data

path = "/Users/chow/Work/pyadjoint/new_images"  # deleteme


@pytest.fixture
def example_data():
    """Return example data to be used to test adjoint sources"""
    obs, syn = get_example_data()
    obs = obs.select(component="Z")[0]
    syn = syn.select(component="Z")[0]

    return obs, syn


@pytest.fixture
def example_dd_data():
    """Return example data to be used to test adjoint sources"""
    obs, syn = get_example_data()
    obs = obs.select(component="R")[0]
    syn = syn.select(component="R")[0]

    return obs, syn


@pytest.fixture
def example_window():
    """Defines an example window where misfit can be quantified"""
    return [[2076., 2418.0]]


def test_waveform_misfit(example_data, example_window):
    """
    Test the waveform misfit function
    """
    obs, syn = example_data
    cfg = get_config(adjsrc_type="waveform_misfit", min_period=30.,
                     max_period=75.)
    adjsrc = calculate_adjoint_source(
        adj_src_type="waveform_misfit", observed=obs, synthetic=syn, config=cfg,
        windows=example_window, adjoint_src=True, plot=True,
        plot_filename=f"{path}/waveform_misfit.png"
    )
    assert adjsrc.adjoint_source.any()
    assert adjsrc.misfit >= 0.0
    assert len(adjsrc.windows) == 1
    assert isinstance(adjsrc.adjoint_source, np.ndarray)


def test_waveform_dd_misfit(example_data, example_dd_data, example_window):
    """
    Test the waveform misfit function
    """
    obs, syn = example_data
    obs_dd, syn_dd = example_dd_data
    cfg = get_config(adjsrc_type="waveform_misfit", min_period=30.,
                     max_period=75.)
    adjsrcs = calculate_adjoint_source(
        adj_src_type="waveform_misfit", observed=obs, synthetic=syn, config=cfg,
        windows=example_window, adjoint_src=True, plot=True,
        plot_filename=f"{path}/waveform_dd_misfit.png", double_difference=True,
        observed_dd=obs_dd, synthetic_dd=syn_dd, windows_dd=example_window
    )

    for adjsrc in adjsrcs:
        assert adjsrc.adjoint_source.any()
        assert adjsrc.misfit >= 0.0
        assert len(adjsrc.windows) == 1
        assert isinstance(adjsrc.adjoint_source, np.ndarray)


def test_cc_traveltime_misfit(example_data, example_window):
    """
    Test the waveform misfit function
    """
    obs, syn = example_data
    cfg = get_config(adjsrc_type="cc_traveltime_misfit", min_period=30.,
                     max_period=75.)
    adjsrc = calculate_adjoint_source(
        adj_src_type="cc_traveltime_misfit", observed=obs, synthetic=syn,
        config=cfg, windows=example_window, adjoint_src=True, plot=True,
        plot_filename=f"{path}/cc_traveltime_misfit.png"
    )

    assert adjsrc.adjoint_source.any()
    assert adjsrc.misfit >= 0.0
    assert len(adjsrc.windows) == 1
    assert isinstance(adjsrc.adjoint_source, np.ndarray)


def test_multitaper_misfit(example_data, example_window):
    """
    Test the waveform misfit function
    """
    obs, syn = example_data
    cfg = get_config(adjsrc_type="multitaper_misfit", min_period=30.,
                     max_period=75., min_cycle_in_window=3., 
                     use_cc_error=False)

    adjsrc = calculate_adjoint_source(
        adj_src_type="multitaper_misfit", observed=obs, synthetic=syn,
        config=cfg, windows=example_window, adjoint_src=True, plot=True,
        plot_filename=f"{path}/multitaper_misfit.png"
    )

    assert adjsrc.adjoint_source.any()
    assert adjsrc.misfit >= 0.0

    assert isinstance(adjsrc.adjoint_source, np.ndarray)


def test_exponentiated_phase_misfit(example_data, example_window):
    """
    Test the waveform misfit function
    """
    obs, syn = example_data
    cfg = get_config(adjsrc_type="exponentiated_phase_misfit", min_period=30.,
                     max_period=75.)

    adjsrc = calculate_adjoint_source(
        adj_src_type="exponentiated_phase_misfit", observed=obs, synthetic=syn,
        config=cfg, windows=example_window, adjoint_src=True, plot=True,
        plot_filename=f"{path}/exponentiated_phase_misfit.png"
    )

    assert adjsrc.adjoint_source.any()
    assert adjsrc.misfit >= 0.0

    assert isinstance(adjsrc.adjoint_source, np.ndarray)

