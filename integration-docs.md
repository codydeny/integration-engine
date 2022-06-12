# Integration Docs
## Create your own integration
you can create your own integration by inheriting the `Integration` class, example `DemoIntegration` built with it can be found at `integrations/demo/demo_integration.py`

### `Integration` class

```
class Integration(ABC):
    @abstractmethod
    def initialize(self, init_data, form) -> Execution:
        pass

    def pre_process(self, response, steps_data):
        pass

    @abstractmethod
    def execute(self, processed_data) -> Execution:
        pass
```
just by implementing these three functions you can create an integration.
#### `initialize`
* only gets called once
* should instance of the `Execution` class

#### `pre_process`
* gets called everytime before calling execute.
* its returned data is directly passed to `execute`

#### `execute`
* gets called every single time there is a response submission
* should instance of the `Execution` class


### Add enum value to mapper
after developing the integration, add its enum value to `core/types.py` with an `identifier` as key and complete path to the `Integration` class in dot notion as value.
#### example
```
IntegrationToClassMapper = {
    ...,
    "DEMO": "integrations.demo.demo_integration.DemoIntegration",
    ...
}
```