import json
import os
from pathlib import Path
import pytest

from quetz.config import Config
from quetz.dao import Dao
from quetz.db_models import Channel as Channel_model
from quetz.tasks.indexing import update_indexes
from quetz.rest_models import Channel, Package
from quetz import channel_data

from .api.conftest import *


@pytest.fixture
def empty_channeldata(dao):
    return channel_data.export(dao, "")


def test_update_indexes_empty_channel(
    config: Config,
    public_channel,
    dao,
    empty_channeldata
):
    pkgstore = config.get_package_store()

    update_indexes(dao, pkgstore, public_channel.name)

    files = pkgstore.list_files(public_channel.name)

    base_files = [
        'channeldata.json',
        'index.html',
        'noarch/index.html',
        'noarch/repodata.json',
    ]

    expected_files = base_files.copy()

    for suffix in ['.bz2', '.gz']:
        expected_files.extend(s + suffix for s in base_files)

    assert sorted(files) == sorted(expected_files)

    channel_dir = Path(pkgstore.channels_dir) / public_channel.name
    with open(channel_dir / 'channeldata.json', 'r') as fd:
        assert json.load(fd) == empty_channeldata


def test_update_indexes_empty_package(
    config: Config,
    public_channel,
    public_package,
    dao,
    empty_channeldata
):
    pkgstore = config.get_package_store()

    update_indexes(dao, pkgstore, public_channel.name)

    files = pkgstore.list_files(public_channel.name)

    base_files = [
        'channeldata.json',
        'index.html',
        'noarch/index.html',
        'noarch/repodata.json',
    ]

    expected_files = base_files.copy()

    for suffix in ['.bz2', '.gz']:
        expected_files.extend(s + suffix for s in base_files)

    assert sorted(files) == sorted(expected_files)

    channel_dir = Path(pkgstore.channels_dir) / public_channel.name
    with open(channel_dir / 'channeldata.json', 'r') as fd:
        channeldata = json.load(fd)

    assert public_package.name in channeldata["packages"].keys()

    assert channeldata["packages"].pop(public_package.name) == {}
    assert channeldata == empty_channeldata


def test_update_indexes_with_package_version(
    config: Config,
    public_channel,
    public_package,
    package_version,
    dao
):
    platform="linux-64"
    pkgstore = config.get_package_store()

    update_indexes(dao, pkgstore, public_channel.name)

    files = pkgstore.list_files(public_channel.name)

    base_files = [
        'channeldata.json',
        'index.html',
        'linux-64/index.html',
        'linux-64/repodata.json',
        'noarch/index.html',
        'noarch/repodata.json',
    ]

    expected_files = base_files.copy()

    for suffix in ['.bz2', '.gz']:
        expected_files.extend(s + suffix for s in base_files)

    expected_files.append(f"linux-64/{package_version.filename}")

    assert sorted(files) == sorted(expected_files)

    channel_dir = Path(pkgstore.channels_dir) / public_channel.name
    with open(channel_dir / 'channeldata.json', 'r') as fd:
        channeldata = json.load(fd)

    assert public_package.name in channeldata["packages"].keys()
