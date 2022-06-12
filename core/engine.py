from pprint import pprint

from core.Integration import Integration
import uuid

from core.execution import Execution


class Engine:
    integration: Integration = None
    response = None
    init_data = None
    integration_action = None
    execution_id = None

    def __init__(self, integration, response, integration_instance):
        self.response = response
        self.init_data = {}
        self.integration_action = integration_instance
        self.execution_id = str(uuid.uuid4())
        self.integration = integration(integration_instance)

    def pre_process_data(self):
        return self.integration.pre_process(response=self.response, steps_data=self.response.steps_data)

    def execute_integration(self):
        # execute subsequent steps
        steps_data = self.response.steps_data
        processed_data = self.pre_process_data()
        execution = self.integration.execute(processed_data)
        if execution.success is True:
            if "executions" not in steps_data:
                steps_data["executions"] = {}

            steps_data["executions"][self.execution_id] = execution.__dict__
            self.response.steps_data = steps_data
            self.response.save()

        return execution

    def init(self) -> Execution:
        # make sure to return something on every step end
        # a lot will depend on the integration instance's state, is it created, running,etc.
        # initialize is called only when integration instance is in not_started state
        status = self.integration_action.Status

        execution: Execution

        if self.integration_action.status == status.NOT_STARTED:
            init_data = self.integration_action.input
            form = self.integration_action.form
            execution = self.integration.initialize(init_data=init_data, form=form)
            if execution.success:
                init_data["init_data"] = execution.__dict__
                self.integration_action.status = status.STARTED
                self.integration_action.input = init_data
                self.integration_action.save()

        else:
            execution = self.execute_integration()

        return execution
