import unittest
from unittest.mock import patch, MagicMock
from costs_management.cloud_providers.azure_provider import AzureProvider

class TestAzureProvider(unittest.TestCase):
    def setUp(self):
        # Patch yaml loading to avoid real file dependency
        patcher_yaml = patch("costs_management.cloud_providers.azure_provider.yaml.safe_load", return_value={
            "tenant_id": "fake-tenant",
            "client_id": "fake-client",
            "client_secret": "fake-secret",
            "subscription_id": "fake-subscription",
            "resource_groups": ["fake-rg"],
            "shutdown_enabled": True,
            "dry_run": True,
            "cost_threshold_usd": 10.0,
            "log_level": "CRITICAL"  # suppress logs in tests
        })
        self.mock_yaml = patcher_yaml.start()
        self.addCleanup(patcher_yaml.stop)

        # Create instance with mocked config
        self.provider = AzureProvider(config_path="fake_path.yaml")

    @patch("costs_management.cloud_providers.azure_provider.ComputeManagementClient.virtual_machines.list")
    def test_fetch_services(self, mock_vm_list):
        mock_vm = MagicMock()
        mock_vm.name = "vm1"
        mock_vm_list.return_value = [mock_vm]
        
        services = self.provider.fetch_services()
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0]["name"], "vm1")
        self.assertEqual(services[0]["resource_group"], "fake-rg")

    @patch("costs_management.cloud_providers.azure_provider.CostManagementClient.query.usage")
    def test_fetch_costs(self, mock_query_usage):
        # Mock response object with expected structure
        mock_response = MagicMock()
        mock_response.rows = [[15.0]]  # Cost of $15
        mock_query_usage.return_value = mock_response

        service = {"name": "vm1", "resource_group": "fake-rg", "type": "vm"}
        cost = self.provider.fetch_costs(service)
        self.assertEqual(cost, 15.0)

    @patch("costs_management.cloud_providers.azure_provider.ComputeManagementClient.virtual_machines.begin_power_off")
    def test_shut_down_dry_run(self, mock_power_off):
        service = {"name": "vm1", "resource_group": "fake-rg", "type": "vm"}

        # dry_run True: begin_power_off should NOT be called
        self.provider.shut_down(service)
        mock_power_off.assert_not_called()

        # Now test with dry_run False
        self.provider.config["dry_run"] = False
        self.provider.shut_down(service)
        mock_power_off.assert_called_once_with("fake-rg", "vm1")

if __name__ == "__main__":
    unittest.main()
