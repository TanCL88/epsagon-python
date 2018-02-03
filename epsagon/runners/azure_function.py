"""
Runner for Azure Functions
"""

from __future__ import absolute_import
import os
from ..event import BaseEvent
from ..trace import tracer
from ..common import ErrorCode


class AzureFunctionRunner(BaseEvent):
    """
    Represents Azure function event runner
    """

    ORIGIN = 'runner'
    RESOURCE_TYPE = 'azure_function'
    OPERATION = 'Invoke'

    def __init__(self, start_time):
        """
        Initialize.
        :param start_time: event's start time (epoch)
        """

        super(AzureFunctionRunner, self).__init__(start_time)

        self.event_id = os.environ.get('EXECUTION_CONTEXT_INVOCATIONID', '')
        self.resource['name'] = os.environ.get('EXECUTION_CONTEXT_FUNCTIONNAME', '')
        self.resource['operation'] = self.OPERATION

        self.resource['metadata'] = {
            'region': os.environ.get('REGION_NAME', ''),
            'memory': os.environ.get('WEBSITE_MEMORY_LIMIT_MB', ''),
        }

    def set_exception(self, exception, traceback):
        """
        Sets exception data on event.
        :param exception: Exception object
        :param traceback: traceback string
        :return: None
        """

        tracer.error_code = ErrorCode.EXCEPTION
        self.error_code = ErrorCode.EXCEPTION
        self.resource['metadata']['exception'] = repr(exception)
        self.resource['metadata']['traceback'] = traceback
