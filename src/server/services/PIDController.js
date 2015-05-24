var PIDController = function(gains) {
  this.k_p = gains.k_p || 1;
  this.k_i = gains.k_i || 0;
  this.k_d = gains.k_d || 0;

  this.sumError  = 0;
  this.lastError = 0;
  this.lastTime  = 0;

  this.target = 0;
};

PIDController.prototype.setTarget = function(target) {
  this.target = target;
};

PIDController.prototype.update = function(current_value) {
  this.current_value = current_value;

  var error = (this.target - this.current_value);
  this.sumError = this.sumError + error;
  var dError = error - this.lastError;
  this.lastError = error;
  return (this.k_p*error) + (this.k_i * this.sumError) + (this.k_d * dError);
};

module.exports = PIDController
