from collect.serializers import ResponseSerializer
from core.Integration import Integration
from core.execution import Execution


class DemoIntegration(Integration):
    # create a demo step where you just return the values back

    def initialize(self, init_data, form):
        return Execution(
            success=True,
            message="Success",
            data={
                "processed_data": init_data
            }
        )

    def execute(self, processed_data):
        return Execution(
            success=True,
            message="Success",
            data={
                "newstuff": "asdasd"
            }
        )
