var HomeLayer = cc.Layer.extend({
  sprite: null,

  ctor: function() {
    this._super();

    var size = cc.winSize;

    // Add the "new game" button
    var newGameButton = cc.MenuItemSprite.create(
      sprites.startGame.normal(),
      sprites.startGame.selected(),
      sprites.startGame.disabled(),
      this.onNewGameSelect
    );

    // Add the options button
    var optionsButton = cc.MenuItemSprite.create(
      sprites.options.normal(),
      sprites.options.selected(),
      sprites.options.disabled(),
      this.onOptionsSelect
    );

    var menu = cc.Menu.create(newGameButton, optionsButton);
    menu.alignItemsHorizontallyWithPadding(10);
    this.addChild(menu);
    menu.setPosition(size.width / 2, size.height / 2 - 80);
    this.schedule(this.update, 0.1);

    var titleLabel = new cc.LabelTTF('Pong', 'Arial', 100);
    titleLabel.x = size.width / 2;
    titleLabel.y = size.height / 2 + 90;
    this.addChild(titleLabel);

    // Author name label
    var authorLabel = new cc.LabelTTF('By Alex LaFroscia', 'Arial', 38);
    authorLabel.x = size.width / 2;
    authorLabel.y = size.height / 2;
    this.addChild(authorLabel);

    return true;
  },

  onNewGameSelect: function() {
    var gameScene = new GameScene();
    if (gameScene.init()) {
      cc.director.pushScene(
        cc.TransitionFade.create(0.5, gameScene)
      );
    } else {
      throw Error('Could not initialize game scene');
    }
  },

  onOptionsSelect: function() {
    var optionsScene = new OptionsScene();
    if (optionsScene.init()) {
      cc.director.pushScene(
        cc.TransitionFade.create(0.5, optionsScene)
      );
    } else {
      throw Error('Could not initialize options scene');
    }
  }
});

var HomeScene = cc.Scene.extend({
  onEnter: function() {
    this._super();
    var layer = new HomeLayer();
    this.addChild(layer);
  }
});
