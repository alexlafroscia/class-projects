var Switch = cc.Sprite.extend({
  ctor: function(enabled, x, y) {
    var imageName = res['switch_png'];
    this._super(imageName);

    if (enabled) {
      this.setFlippedX(true);
    }

    if (arguments.length === 3) {
      this.setPosition(x, y);
    }

    cc.eventManager.addListener({
      event: cc.EventListener.TOUCH_ONE_BY_ONE,
      swallowTouches: true,
      onTouchBegan: function switchTouchHandler(touch) {
        var touchLocation = touch.getLocationInView();
        if (cc.rectContainsPoint(this.getBoundingBox(), touchLocation)) {
          return this.onClickHandler();
        } else {
          return false;
        }
      }.bind(this)
    }, this);
  },

  onClickHandler: function(touch, event) {
    console.log('not implemented');
  }

});
