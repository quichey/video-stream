import yaml
import logging
from pathlib import Path
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryAggregation
from datetime import datetime, timedelta

from cloud_providers.base_provider import BaseProvider

class AzureProvider(BaseProvider):
    def __init__(self, config_path="azure_config_example.yaml"):
        self.config = self._load_config(config_path)
        self._init_logger()
        self.credential = ClientSecretCredential(
            tenant_id=self.config["tenant_id"],
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"]
        )
        self.subscription_id = self.config["subscription_id"]

        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        self.compute_client = ComputeManagementClient(self.credential, self.subscription_id)
        self.cost_client = CostManagementClient(self.credential)

    def _load_config(self, path):
        with open(Path(path), "r") as f:
            return yaml.safe_load(f)

    def _init_logger(self):
        logging.basicConfig(level=self.config.get("log_level", "INFO"))
        self.logger = logging.getLogger(__name__)

    def fetch_services(self):
        resource_groups = self.config.get("resource_groups", [])
        services = []
        for rg in resource_groups:
            vms = self.compute_client.virtual_machines.list(rg)
            for vm in vms:
                services.append({"name": vm.name, "resource_group": rg, "type": "vm"})
        return services

    def fetch_costs(self, service):
        now = datetime.utcnow()
        start = now - timedelta(days=30)
        time_period = QueryTimePeriod(from_property=start, to=now)

        query = QueryDefinition(
            type="Usage",
            timeframe="Custom",
            time_period=time_period,
            dataset=QueryDataset(
                granularity="None",
                aggregation={
                    "totalCost": QueryAggregation(name="PreTaxCost", function="Sum")
                }
            )
        )

        scope = f"/subscriptions/{self.subscription_id}/resourceGroups/{service['resource_group']}"
        result = self.cost_client.query.usage(scope=scope, parameters=query)

        # Default to 0 if no data
        if result and result.rows and result.rows[0]:
            cost = float(result.rows[0][0])
            self.logger.info(f"Service {service['name']} cost: ${cost:.2f}")
            return cost
        else:
            self.logger.warning(f"No cost data found for service: {service['name']}")
            return 0.0

    def shut_down(self, service):
        if service["type"] == "vm":
            if self.config.get("shutdown_enabled", False):
                if self.config.get("dry_run", True):
                    self.logger.info(f"[Dry Run] Would stop VM: {service['name']}")
                else:
                    self.logger.info(f"Stopping VM: {service['name']}")
                    self.compute_client.virtual_machines.begin_power_off(
                        service["resource_group"],
                        service["name"]
                    )
            else:
                self.logger.info(f"Shutdown disabled. Skipping VM: {service['name']}")
        else:
            self.logger.warning(f"Shutdown not implemented for type: {service['type']}")

    def run_monitoring(self):
        threshold = self.config.get("cost_threshold_usd", 50.0)
        services = self.fetch_services()

        for svc in services:
            cost = self.fetch_costs(svc)
            if cost >= threshold:
                self.logger.warning(f"Service {svc['name']} exceeds threshold (${threshold:.2f})")
                self.shut_down(svc)
            else:
                self.logger.info(f"Service {svc['name']} is under budget.")
