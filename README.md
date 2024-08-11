# Tetr.io-Bot
Teapot is a python pixel bot for Tetr.io  
USE AT YOUR OWN RISK  

Download the included skin (skin.png) and apply using Tetr.io Plus at https://gitlab.com/UniQMG/tetrio-plus  
If the bot is seemingly placing pieces at random, try increasing the delay in the loop. This happens because your computer may be calculating the best move faster than Python can send the input to the game.

Config settings:
Gameplay: boardzoom 130%, shadowvisibility 0%, boardbounciness 0%

In Tetr.io+, it is also recommended to replace 
`particle_beam` 
`particle_beams_beam`
`particle_chirp` 
`particle_star`

with transparent files (empty.png) to avoid the bot reading particle effects as unknown blocks.
