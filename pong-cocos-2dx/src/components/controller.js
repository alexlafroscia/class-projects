var Controller = cc.Sprite.extend({
  active: true,

  gameLayer: null,

  upEventCallback: undefined,
  downEventCallback: undefined,

  ctor: function(position) {
    this._super(res.controller);

    var winSize = cc.director.getWinSize();
    var offset = this.width / 2;
    var horizontalPosition;
    if (position == 'left') {
      horizontalPosition = 0 + offset;
    } else if (position === 'right') {
      horizontalPosition = winSize.width - offset;
    } else {
      throw Error('Position must be either left or right');
    }
    this.setPosition(horizontalPosition, winSize.height / 2);

    cc.eventManager.addListener({
      event: cc.EventListener.TOUCH_ONE_BY_ONE,
      swallowTouches: true,
      onTouchBegan: this.handleTouch.bind(this)
    }, this);
  },

  getCurrentRectangle: function() {
    return convertBoxToGL(this.getBoundingBox());
  },

  handleTouch: function(touch, event) {
    var touchLocation = cc.director.convertToGL(touch.getLocation());
    if (this.touchTopHalf(touchLocation)) {
      this.upEventCallback();
    } else if (this.touchBottomHalf(touchLocation)) {
      this.downEventCallback();
    } else {
      return false;
    }
    return true;
  },

  touchTopHalf: function(loc) {
    var rect = this.getCurrentRectangle();
    rect.height = rect.height / 2;
    rect.y = rect.y + rect.height;
    return cc.rectContainsPoint(rect, loc);
  },

  touchBottomHalf: function(loc) {
    var rect = this.getCurrentRectangle();
    rect.height = rect.height / 2;
    return cc.rectContainsPoint(rect, loc);
  }
});

Controller.create = function(position) {
  var controller = new Controller(position);
  controller.setVisible(true);
  return controller;
};
