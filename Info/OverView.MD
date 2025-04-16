# MC Solutions for All-in or fold poker game
Aim: Design and assess range charts for All in or fold game mode.

## Coding strategy
For a given range chart (optional: supply opponent range chart too) track player net value over given number of hands, repeat this to find EV (expected value) of the chart's strategy.

Supplied game info:
- Players starting net value (Bankroll)
- Buy-in Amount
- Max bet amount (game mode offers maximum bet, if player stack exceeds max bet, only max bet is placed)
- Blinds  
- Number of hands played
- Optional: number of player, player range charts.  

The user can also specify the number of iterations in the MC simulation.

As the game mode is all in or fold, we do not need to consider later street betting, we simply need a method to determine the winning hand among a group of hole cards and a shared board.