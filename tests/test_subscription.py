from unittest.mock import patch
import json

from lolite.lib.subproc import Subproc
from lolite.lib.subscription import Subscription


def test_check_if_current():
    sample_azure_response = open('tests/test_output/test_subproc_get_resource_groups.json', 'r').read()
    with patch.object(Subproc, 'get_resource_groups', return_value = sample_azure_response):
        subproc = Subproc()
        subscription = Subscription(subproc)

        assert subscription.check_if_current("lolite-test")
        assert not subscription.check_if_current("not-lolite-test")
