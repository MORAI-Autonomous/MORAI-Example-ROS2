import pytest

from test_base.test_03_set_intscn_and_status import Test03SetIntscnAndStatusBase


class Test03SetIntscnAndStatusMorai(Test03SetIntscnAndStatusBase):
    def test_1_set_intersection_status(self, setup_teardown_method):
        self.publish(self.set_intersection_status(13, 1))
    
    @pytest.mark.skip(reason="can get value when ego vehicle is inside the intersection")
    def test_2_get_intersection_status(self, setup_teardown_method):
        result = self.get_intersection_status()
        assert result.intersection_index == 13
        assert result.intersection_status == 1
