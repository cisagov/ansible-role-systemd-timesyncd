"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Verify that the expected packages are installed/removed."""
    installed_pkgs = None
    removed_pkgs = None
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        installed_pkgs = ["systemd-timesyncd"]
        removed_pkgs = []
    elif host.system_info.distribution in ["amzn", "fedora"]:
        installed_pkgs = ["systemd-udev"]
        removed_pkgs = ["chrony"]
    else:
        assert False, f"Unknown distribution {host.system_info.distribution}."

    for pkg in installed_pkgs:
        assert host.package(pkg).is_installed, f"The package {pkg} is not installed."
    for pkg in removed_pkgs:
        assert not host.package(pkg).is_installed, f"The package {pkg} is present."


@pytest.mark.parametrize("svc", ["systemd-timesyncd.service"])
def test_services(host, svc):
    """Verify that the expected services are present."""
    s = host.service(svc)
    assert s.exists, f"{svc} service does not exist."
    assert s.is_enabled, f"{svc} service is not enabled."
