function Player(controller) {
  this.score = 0;
  this.onScoreUpdate = undefined;
}

Player.prototype.scorePoint = function() {
  this.score += 1;
  if (this.onScoreUpdate) {
    this.onScoreUpdate(this.score);
  }
}
