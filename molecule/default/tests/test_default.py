"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["systemd-timesyncd"])
def test_packages(host, pkg):
    """Verify that the expected packages are installed."""
    assert host.package(pkg).is_installed, f"The package {pkg} is not installed."


@pytest.mark.parametrize("svc", ["systemd-timesyncd.service"])
def test_services(host, svc):
    """Verify that the expected services are present."""
    s = host.service(svc)
    assert s.exists, f"{svc} service does not exist."
    assert s.is_enabled, f"{svc} service is not enabled."
