function isSoundEnabled() {
  return !!cc.sys.localStorage.getItem('SOUND_ENABLED');
}

var SoundSettingsLayer = cc.Layer.extend({
  sprite: null,

  ctor: function(enabled) {
    this._super();

    var winSize = cc.director.getWinSize();

    if (enabled) {
      var soundLabelText = 'Sound Effects: On';
    } else {
      var soundLabelText = 'Sound Effects: Off';
    }

    var soundLabel = new cc.LabelTTF(soundLabelText, 'Arial', 30);
    soundLabel.x = winSize.width / 2 - 120;
    soundLabel.y = winSize.height / 2;
    this.addChild(soundLabel);

    var soundSwitch = new Switch(enabled);
    soundSwitch.x = winSize.width / 2 + 80;
    soundSwitch.y = winSize.height / 2;
    soundSwitch.onClickHandler = this.handleSoundSwitchTouch.bind(this);
    this.addChild(soundSwitch);

    return true;
  },

  handleSoundSwitchTouch: function() {
    if (isSoundEnabled()) {
      cc.sys.localStorage.removeItem('SOUND_ENABLED');
    } else {
      cc.sys.localStorage.setItem('SOUND_ENABLED', 'true');
    }
    this.parent.refreshSoundLayer();
    return true;
  }
});

var OptionsLayer = cc.Layer.extend({
  sprite: null,

  ctor: function() {
    this._super();

    var winSize = cc.director.getWinSize();

    var exitButton = ExitButton.create(winSize.width / 2, winSize.height - (SCORE_TEXT_SIZE * 1.5));
    exitButton.onClickHandler = this.onExit.bind(this);
    this.addChild(exitButton, 3);

    return true;
  },

  onExit: function onExit() {
    cc.director.popToRootScene();
    return true;
  }

});

var OptionsScene = cc.Scene.extend({
  soundLayer: null,

  onEnter: function() {
    this._super();
    var optionsLayer = new OptionsLayer();
    this.addChild(optionsLayer);
    this.refreshSoundLayer();
  },

  refreshSoundLayer: function() {
    if (this.soundLayer) {
      this.removeChild(this.soundLayer);
    }
    this.soundLayer = new SoundSettingsLayer(isSoundEnabled());
    this.addChild(this.soundLayer);
  }
});
