// input a pointer to launchpad
var HoverController = function(launchpad) {
    var launchpad_reference = launchpad;

    var m1 = { roll:0, pitch:0, yaw:0 };
    var m2 = { roll:0, pitch:0, yaw:0 };
    var m3 = { roll:0, pitch:0, yaw:0 };
    var m4 = { roll:0, pitch:0, yaw:0 };

    var motor_pwr = { m1:127, m2:127, m3:127, m4:127 };

    // constants for pd controller
    var roll_state = { pk:5, dk:1 };
    var pitch_state = { pk:5, dk:1 };

    var update_controller = function( estimated_roll, estimated_pitch ) {
        update_roll( estimated_roll );
        update_pitch( estimated_pitch );
        update_total();
        update_motor();
    };

    // counteract the estimated roll perturbation with a roll in the opposite direction
    var update_roll = function( estimated_roll ) {
        var roll_power_change = (estimated_roll * roll_state.pk);
        m1.roll += roll_power_change;
        m2.roll -= roll_power_change;
        m3.roll -= roll_power_change;
        m4.roll += roll_power_change;
    };

    // counteract the estimated pitch perturbation with a pitch in the opposite direction
    var update_pitch = function( estimated_pitch ) {
        var diff_pitch = desired_pitch - estimate_pitch;
        pitch_state.isum += diff_pitch;
        var pitch_power_change = (estimated_pitch * pitch_state.pk);
        m1.pitch += pitch_power_change;
        m2.pitch -= pitch_power_change;
        m3.pitch += pitch_power_change;
        m4.pitch -= pitch_power_change;
    };

    // update total power
    var update_total = function() {
        motor_pwr.m1 += ( m1.pitch + m1.roll );
        motor_pwr.m2 += ( m2.pitch + m2.roll );
        motor_pwr.m3 += ( m3.pitch + m3.roll );
        motor_pwr.m4 += ( m4.pitch + m4.roll );
        if( motor_pwr.m1 < 0 ) {
            motor_pwr.m1 = 0;
        }
        if( motor_pwr.m1 > 254 ) {
            motor_pwr.m1 = 254;
        }
        if( motor_pwr.m2 < 0 ) {
            motor_pwr.m2 = 0;
        }
        if( motor_pwr.m2 > 254 ) {
            motor_pwr.m2 = 254;
        }
        if( motor_pwr.m3 < 0 ) {
            motor_pwr.m3 = 0;
        }
        if( motor_pwr.m3 > 254 ) {
            motor_pwr.m3 = 254;
        }
        if( motor_pwr.m4 < 0 ) {
            motor_pwr.m4 = 0;
        }
        if( motor_pwr.m4 > 254 ) {
            motor_pwr.m4 = 254;
        }
    };

    // write result to motor
    var update_motor = function() {
        launchpad_reference.write(new Buffer([255,motor_pwr.m1,motor_pwr.m2,motor_pwr.m3,motor_pwr.m4]));
    }
};

module.exports = HoverController;
