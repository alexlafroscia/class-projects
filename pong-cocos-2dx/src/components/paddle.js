var ACTIVE_SPEED = 1000;

var Paddle = cc.Sprite.extend({
  active: true,

  yVelocity: 0,

  gameLayer: null,

  controller: null,

  position: null,

  ctor: function(controller, position) {
    // Initialize image
    var imageName = res['paddle_' + position + '_png'];
    this._super(imageName);

    controller.upEventCallback = this.moveUp.bind(this);
    controller.downEventCallback = this.moveDown.bind(this);

    // Set the starting position
    var winSize = cc.director.getWinSize();
    var offset = this.width + (this.width / 5);
    var horizontalPosition;
    if (position == 'left') {
      horizontalPosition = 0 + offset;
    } else if (position === 'right') {
      horizontalPosition = winSize.width - offset;
    } else {
      throw Error('Position must be either left or right');
    }
    this.setPosition(horizontalPosition, winSize.height / 2);
  },

  isCollidingTop: function() {
    var p = this.getPosition();
    return p.y < 0;
  },

  isCollidingBottom: function() {
    var p = this.getPosition();
    var gl = this.gameLayer;
    return p.y > gl.screenRect.height;
  },

  moveUp: function() {
    this.yVelocity = ACTIVE_SPEED;
  },

  moveDown: function() {
    this.yVelocity = -ACTIVE_SPEED;
  },

  acceptPlayerMovement: function(dt) {
    var p = this.getPosition();
    this.setPositionY(p.y - this.yVelocity * dt);

    // Reset velocity
    this.yVelocity = 0;
  },

  update: function(dt) {
    this._super(dt);
    var p = this.getPosition();

    // Detect collisions and bounce
    if (!this.isCollidingTop() || !this.isCollidingBottom()) {
      this.acceptPlayerMovement(dt);
    }
  },

  getCurrentRectangle: function() {
    return cc.rect(
      this.getPosition().x - (this.getContentSize().width / 2),
      this.getPosition().y - (this.getContentSize().height / 2),
      this.getContentSize().width,
      this.getContentSize().height
    );
  }
});

Paddle.create = function(controller, position) {
  var paddle = new Paddle(controller, position);
  paddle.setVisible(true);
  return paddle;
};
