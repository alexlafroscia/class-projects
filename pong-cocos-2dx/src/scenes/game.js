var SCORE_TEXT_SIZE = 40;
var SCORE_TEXT_CENTER_OFFSET = 100;

var GameLayer = cc.Layer.extend({
  sprite: null,

  screenRect: null,

  puck: null,
  paddles: {
    left: null,
    right: null,
  },
  players: {
    left: null,
    right: null,
  },

  ctor: function() {
    this._super();

    var winSize = cc.director.getWinSize();
    this.screenRect = cc.rect(0, 0, winSize.width, winSize.height + 10);

    var leftScoreLabel = new cc.LabelTTF('0', 'Arial', SCORE_TEXT_SIZE);
    leftScoreLabel.x = winSize.width / 2 - SCORE_TEXT_CENTER_OFFSET;
    leftScoreLabel.y = winSize.height - (SCORE_TEXT_SIZE * 1.5);
    this.addChild(leftScoreLabel);

    var exitButton = ExitButton.create(winSize.width / 2, winSize.height - (SCORE_TEXT_SIZE * 1.5));
    exitButton.onClickHandler = this.onExit.bind(this);
    this.addChild(exitButton, 3);

    var rightScoreLabel = new cc.LabelTTF('0', 'Arial', SCORE_TEXT_SIZE);
    rightScoreLabel.x = winSize.width / 2 + SCORE_TEXT_CENTER_OFFSET;
    rightScoreLabel.y = winSize.height - (SCORE_TEXT_SIZE * 1.5)
    this.addChild(rightScoreLabel);

    var leftController = Controller.create('left');
    leftController.gameLayer = this;
    this.addChild(leftController);

    var leftPaddle = Paddle.create(leftController, 'left');
    leftPaddle.gamelayer = this;
    this.addChild(leftPaddle);
    this.paddles.left = leftPaddle;

    var rightController = Controller.create('right');
    rightController.gameLayer = this;
    this.addChild(rightController);

    var rightPaddle = Paddle.create(rightController, 'right');
    rightPaddle.gameLayer = this;
    this.addChild(rightPaddle);
    this.paddles.right = rightPaddle;

    this.players.left = new Player(leftController);
    this.players.left.onScoreUpdate = function(newScore) {
      leftScoreLabel.string = newScore + '';
    };
    this.players.right = new Player(rightController);
    this.players.right.onScoreUpdate = function(newScore) {
      rightScoreLabel.string = newScore + '';
    };

    this.createPuck();

    this.scheduleUpdate();
    return true;
  },

  createPuck: function() {
    var size = cc.director.getWinSize();
    var puck = Puck.create();
    puck.gameLayer = this;

    puck.onCrossLeftBoundary = function() {
      this.players.left.scorePoint();
      this.resetPuck();
    }.bind(this);
    puck.onCrossRightBoundary = function() {
      this.players.right.scorePoint();
      this.resetPuck();
    }.bind(this);

    this.addChild(puck);
    puck.setPosition(size.width / 2, size.height / 2);
    this.puck = puck;
  },

  update: function(dt) {
    this._super(dt);
    if (this.puck) {
      this.puck.scheduleUpdate();
    }
    this.paddles.right.scheduleUpdate();
    this.paddles.left.scheduleUpdate();
  },

  resetPuck: function() {
    this.puck.destroy();
    this.createPuck();
  },

  onExit: function onExit() {
    cc.director.popToRootScene();
    return true;
  }

});

GameLayer.create = function() {
  var layer = new GameLayer();
  if (layer && layer.init()) {
    return layer;
  } else {
    throw Error('Could not initialize game layer');
  }
};

var GameScene = cc.Scene.extend({
  onEnter: function() {
    this._super();
    var layer = GameLayer.create();
    this.addChild(layer, 1);
  }
});
