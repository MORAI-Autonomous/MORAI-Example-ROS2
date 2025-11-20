import pytest

from morai_sim_examples.publishers.pub_set_traffic_light import LightColors
from test_base.test_02_set_traffic_light_and_status import Test02SetTrafficLightAndStatusBase


class Test02SetTrafficLightAndStatusMorai(Test02SetTrafficLightAndStatusBase):
    def test_1_set_traffic_light(self, setup_teardown_method):
        self.publish(self.set_traffic_light("C119AS318012", LightColors.R))
        assert True
    
    @pytest.mark.skip(reason="can get value when ego vehicle detects traffic light")
    def test_2_get_traffic_light(self, setup_teardown_method):
        result = self.get_traffic_light_status()
        assert result.traffic_light_status == LightColors.R.value
