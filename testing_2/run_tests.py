from drivers.devices import TestInfraManager
from drivers.driver import driver


if __name__ == "__main__":
    infra_manager = TestInfraManager()

    infra_manager.deploy()
    infra_manager.start()
    driver.run_tests?()

    infra_manager.stop()

    driver.quit()