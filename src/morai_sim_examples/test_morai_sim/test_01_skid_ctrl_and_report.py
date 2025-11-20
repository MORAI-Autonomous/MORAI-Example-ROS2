import time
from test_base.test_01_skid_ctrl_and_report import Test01SkidCtrlCmdAndReportBase


class Test01SkidCtrlCmdAndReportMorai(Test01SkidCtrlCmdAndReportBase):
    def test_1_rpm_control_left_front(self, setup_teardown_method):
        self.publish(self.rpm_control([1000.0, 0.0, 0.0, 0.0], [False, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.rpm.left_front_wheel_rpm > 0.0

    def test_2_rpm_control_left_rear(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 1000.0, 0.0, 0.0], [False, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.rpm.left_rear_wheel_rpm > 0.0
    
    def test_3_rpm_control_right_front(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 1000.0, 0.0], [False, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.rpm.right_front_wheel_rpm > 0.0

    def test_4_rpm_control_right_rear(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 1000.0], [False, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.rpm.right_rear_wheel_rpm > 0.0
    
    def test_5_rpm_control_all(self, setup_teardown_method):
        self.publish(self.rpm_control([1000.0, 1000.0, 1000.0, 1000.0], [False, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert round(result.velocity.x, 2) > 0.0
    
    def test_6_rpm_control_stop(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 0.0], [False, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert round(result.velocity.x, 2) == 0.0

    def test_7_torque_control_left_front(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 0.0], [True, False, False, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.torque.left_front_wheel_torque_off

    def test_8_torque_control_left_rear(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 0.0], [False, True, False, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.torque.left_rear_wheel_torque_off
    
    def test_9_torque_control_right_front(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 0.0], [False, False, True, False]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.torque.right_front_wheel_torque_off

    def test_10_torque_control_right_rear(self, setup_teardown_method):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 0.0], [False, False, False, True]))
        result = self.get_skid_ctrl_report()
        assert result.skid_model_report.torque.right_rear_wheel_torque_off

    def test_11_velocity_control_longitudinal_forward(self, setup_teardown_method):
        self.publish(self.velocity_control(1.9, 0.0))
        result = self.get_skid_ctrl_report()
        #assert round(result.velocity.x, 2) > 0.0
        assert result.skid_model_report.rpm.left_front_wheel_rpm > 0.0 and \
                result.skid_model_report.rpm.left_rear_wheel_rpm > 0.0 and \
                result.skid_model_report.rpm.right_front_wheel_rpm > 0.0 and \
                result.skid_model_report.rpm.right_rear_wheel_rpm > 0.0

    def test_12_velocity_control_longitudinal_backward(self, setup_teardown_method):
        self.publish(self.velocity_control(-1.9, 0.0))
        result = self.get_skid_ctrl_report()
        #assert round(result.velocity.x, 2) < 0.0
        assert result.skid_model_report.rpm.left_front_wheel_rpm < 0.0 and \
                result.skid_model_report.rpm.left_rear_wheel_rpm < 0.0 and \
                result.skid_model_report.rpm.right_front_wheel_rpm < 0.0 and \
                result.skid_model_report.rpm.right_rear_wheel_rpm < 0.0
    
    def test_13_velocity_control_lateral_left(self, setup_teardown_method):
        self.publish(self.velocity_control(0.0, -1.1))
        result = self.get_skid_ctrl_report()
        #assert result.angular_velocity.z > 0.0
        assert result.skid_model_report.rpm.left_front_wheel_rpm < 0.0 and \
                result.skid_model_report.rpm.left_rear_wheel_rpm < 0.0

    def test_14_velocity_control_lateral_right(self, setup_teardown_method):
        self.publish(self.velocity_control(0.0, 1.1))
        result = self.get_skid_ctrl_report()
        #assert result.angular_velocity.z < 0.0
        assert result.skid_model_report.rpm.right_front_wheel_rpm < 0.0 and \
                result.skid_model_report.rpm.right_rear_wheel_rpm < 0.0