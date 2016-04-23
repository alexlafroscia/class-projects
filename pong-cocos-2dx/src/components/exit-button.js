function convertBoxToGL(box) {
  var coord = cc.director.convertToGL(box);
  return {
    x: coord.x,
    y: coord.y - box.height,
    height: box.height,
    width: box.width
  };
}

var ExitButton = cc.Sprite.extend({
  ctor: function(x, y) {
    var imageName = res['exit_button_png'];
    this._super(imageName);
    this.setPosition(x, y);

    cc.eventManager.addListener({
      event: cc.EventListener.TOUCH_ONE_BY_ONE,
      swallowTouches: true,
      onTouchBegan: function exitButtonTouchHandler(touch) {
        var touchLocation = cc.director.convertToGL(touch.getLocation());
        var box = convertBoxToGL(this.getBoundingBox());
        if (cc.rectContainsPoint(box, touchLocation)) {
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

ExitButton.create = function(x, y) {
  var button = new ExitButton(x, y);
  button.setVisible(true);
  return button;
};
