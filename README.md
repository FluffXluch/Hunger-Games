Hunger Games -- A game theory programming tournament

"Write an algorithm to fight to the death against other algorithms. Cooperate and compete with other players at different points in the game to survive and win."

https://brilliant.org/competitions/hunger-games/
============
My algorithm (named HoneyBadger) is made to go for a win. A gameplay of it depends on a stage of the game. The first stage is when there are so many players and change in their reputations is so large that it is impossible to track specific players from round to round. The second stage is when it becomes possible.

In the first stage, HoneyBadger can influence other players’ decisions mostly by its reputation. Since there are very many possible strategies opponents might use, HoneyBadger do not to try to guess what they will choose and do not play counter-strategy for that. Instead, it just uses a local search.

It is easy to see, that independently of opponents choice in each round, HoneyBadger loses one food in that round for playing ‘hunt’. Also, reputation changes slower in later rounds. Therefore, HoneyBadger  ‘hunts’ in the first rounds to grow large reputation and then climb down slowly until it finds a place for maximum food gain. Climbing down must be slow enough not to be over-sensitive to a noise. A noise may come from other player’s adaptation and learning, their algorithms inherent randomness and dependence of m (for players who play for a survival). Of course, this local optimum may not be the global one, but that is a downside I can accept in the face of so many uncertainties. Even the local optimum might change because some players drop out and remaining ones adapt, therefore a search never really stops.

Since in this stage a personal retaliation is impossible, it makes sense to ‘slacker’ to the best players for they are the most dangerous opponents. It is safe to assume that the best players are those whose reputation is close to HoneyBadger’s reputation, because if it is wrong then HoneyBadger just gets busted faster and there is no difference between 2nd place and busting first.

In the second stage, it becomes possible to track specific players over many rounds and they can do it for HoneyBadger too, therefore reputation becomes mostly irrelevant. HoneyBadger plays a variation of “tit for two tats” because Wikipedia suggests it could be the best strategy against not very experienced players in the iterated Prisoners’ Dilemma. HoneyBadger slightly modifies it by making some random moves just to make sure an opponent cares to retaliate to it or maybe starts to cooperate.
