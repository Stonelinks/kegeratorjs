# kegeratorjs
Javascript quad kegerator

TODO: 
```js

  /**
   * Scales the value to a [-1, 1] range given the min/max/center
   */
  normalizeInput: function(value, min, max, center) {
    var scaled = 0;

    if(value < center) {
      scaled = -1 * (value - min) / (center - min);
    } else {
      scaled = (value - center) / (max - center);
    }

    if(isNaN(scaled)) {
      scaled = 0;
    }

    return scaled;
  },
  /**
   * Scales the value assuming an input range of [-1, 1]
   */
  scaleOutput: function(value, min, max, center) {
    var scaled = 0;

    if (value > 0) {
      scaled = Math.floor(value * (max - center) + center);
    } else {
      scaled = Math.floor(value * (center - min) + center);
    }

    return scaled;
  },

```
