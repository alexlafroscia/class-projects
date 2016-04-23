# Report Write-Up

## 1. Problems

One of the problems was the time it took to replace the words in the training data.  Originally, my approach took far too long because the check for whether a word should be replaced, which ran on every word in every sentence of the input text, took far too long.  My original solution was to parallelize this process, which helped, but not enough.  Eventually I realized how to make the check more efficient, but left the parallelization in place since it still gives a speedup.

Another problem, which I realized too late, was that I should calculate a smoothed probability and then use that to create the entropy, and from there the perplexity, instead of smoothing the perplexity values.  It would be too time consuming to change the implementation now, so I am leaving it as-is.

The final major issue is that it was hard to know how to handle instances where a word's probability was `0`, since that makes the perplexity of the whole sentences `INF` or something of that nature.  Since we can't raise it something to the power `0`, those situations had to be special-cased, but I'm fairly sure that my approach is not actually correct.

## 2. Performance of the Model

The performance of the model on part 3 is a little worse that it should be.  I realized too late that I made a fairly significant mistake in the way that I deal with the smoothed models; instead of smoothing when I calculate the probability, and then calculating the entropy and perplexity from there, I calculate the perplexity for each N-Gram and then smooth them after the fact.

Another issue, related to the one mentioned above, is that I wasn't sure how to handle instances where the probability of some word is `0`, because we can't something to the `0` power.  So, I instead just use `0`, but that messes with the perplexity of the sentence.

## 3. Bonus Part

N/A
