from drivers.devices import TestInfraManager
from drivers.driver import create_driver


if __name__ == "__main__":
    driver = create_driver()
    infra_manager = TestInfraManager()

    infra_manager.deploy()
    infra_manager.start()
    driver.run_tests?()

    infra_manager.stop()