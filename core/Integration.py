from abc import ABC, abstractmethod

from core.execution import Execution


class Integration(ABC):
    integration_instance = None

    def __init__(self, integration_instance):
        self.integration_instance = integration_instance

    @abstractmethod
    def initialize(self, init_data, form) -> Execution:
        NotImplementedError("Implement Initialize Function")
        return init_data

    def pre_process(self, response, steps_data):
        return {
            "response": response,
            "steps_data": steps_data
        }

    @abstractmethod
    def execute(self, processed_data) -> Execution:
        NotImplementedError("Implement Execute Function")
        return processed_data
