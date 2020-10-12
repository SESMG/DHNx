# -*- coding: utf-8 -*-
"""
These tests test little examples for the use of the library.

This file is part of project oemof (). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/tools/helpers.py

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd
import networkx as nx

import dhnx
from . import helpers


tmpdir = helpers.extend_basic_path('tmp')

basedir = os.path.dirname(__file__)

dir_import_tree = os.path.join(basedir, '_files/tree_network_import')

dir_import_looped = os.path.join(basedir, '_files/looped_network_import')

tree_thermal_network = dhnx.network.ThermalNetwork(dir_import_tree)

looped_thermal_network = dhnx.network.ThermalNetwork(dir_import_looped)


def test_import_export_csv():
    dir_export = os.path.join(tmpdir, 'network_export')

    network = dhnx.network.ThermalNetwork()
    network = network.from_csv_folder(dir_import_looped)

    network.to_csv_folder(dir_export)

    helpers.check_if_csv_dirs_equal(dir_import_looped, dir_export)


def test_access_attributes():

    network = dhnx.network.ThermalNetwork(dir_import_looped)

    assert isinstance(network.available_components, pd.DataFrame)

    assert network.component_attrs.consumers.id.type == 'int'

    assert isinstance(network.components.consumers, pd.DataFrame)

    assert isinstance(network.sequences.pipes.temperature_return, pd.DataFrame)


def test_get_nx_graph():

    nx_graph = looped_thermal_network.to_nx_graph()

    assert isinstance(nx_graph, nx.Graph)


def test_static_map():
    # plot static map
    dhnx.plotting.StaticMap(looped_thermal_network)


def test_interactive_map():
    # plot interactive map
    interactive_map = dhnx.plotting.InteractiveMap(looped_thermal_network)
    interactive_map.draw()


def test_setup_operation_optimization():

    looped_thermal_network.optimize_operation()


def test_setup_investment_optimization():

    looped_thermal_network.optimize_investment()


def test_setup_simulation():

    tree_thermal_network.simulate()
