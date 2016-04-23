function getRandomVelocity() {
  var r = Math.random();
  if (r > 0.5) {
    return 400;
  } else {
    return -400;
  }
}
var Puck = cc.Sprite.extend({
  active: true,

  xVelocity: 0,
  yVelocity: 0,

  onDestroyCallback: null,

  onCrossLeftBoundary: undefined,
  onCrossRightBoundary: undefined,

  isColliding: false,

  gameLayer: null,

  ctor: function() {
    this._super(res.puck_png);
    this.xVelocity = getRandomVelocity();
    this.yVelocity = getRandomVelocity();
  },

  detectCollisionWithPaddle: function(paddle) {
    var puckRect = this.getCurrentRectangle();
    var paddleRect = paddle.getCurrentRectangle();
    return cc.rectIntersectsRect(puckRect, paddleRect);
  },

  /**
   * Whether or not the puck is currently colliding with something else
   */
  isCollidingTop: function() {
    var p = this.getPosition();
    var gl = this.gameLayer;
    return p.y < 0;
  },

  isCollidingBottom: function() {
    var p = this.getPosition();
    var gl = this.gameLayer;
    return p.y > gl.screenRect.height;
  },

  isCollidingLeft: function() {
    return this.detectCollisionWithPaddle(this.gameLayer.paddles.left);
  },

  isOutOfBoundsLeft: function() {
    var p = this.getPosition();
    return p.x < 0;
  },

  isCollidingRight: function() {
    return this.detectCollisionWithPaddle(this.gameLayer.paddles.right);
  },

  isOutOfBoundsRight: function() {
    var p = this.getPosition();
    var gl = this.gameLayer;
    return p.x > gl.screenRect.width;
  },

  bounceHorizontal: function() {
    this.isColliding = true;
    this.xVelocity = this.xVelocity * -1;
    this.playCollisionSound();
  },

  bounceVertical: function() {
    this.isColliding = true;
    this.yVelocity = this.yVelocity * -1;
    this.playCollisionSound();
  },

  update: function(dt) {
    this._super(dt);
    var p = this.getPosition();

    // Detect collisions and bounce
    if (this.isCollidingTop() || this.isCollidingBottom()) {
      this.bounceVertical();
    } else if (this.isOutOfBoundsLeft()) {
      this.onCrossLeftBoundary();
    } else if (this.isOutOfBoundsRight()) {
      this.onCrossRightBoundary();
    } else if (this.isCollidingRight() || this.isCollidingLeft()) {
      this.isColliding || this.bounceHorizontal();
    } else {
      this.isColliding = false;
    }

    this.setPosition(p.x - this.xVelocity * dt, p.y - this.yVelocity * dt);
  },

  playCollisionSound: function() {
    if (isSoundEnabled()) {
      cc.audioEngine.playEffect(res.boop_wav, false);
    }
  },

  destroy: function() {
    if (this.onDestroyCallback) {
      this.onDestroyCallback.call(this);
    }
    this.gameLayer.removeChild(this);
    // this.release();
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

Puck.create = function() {
  var puck = new Puck();
  puck.setVisible(true);
  return puck;
};
