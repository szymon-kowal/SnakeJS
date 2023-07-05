# Snake but in JS

I slightly edited the game created by https://www.youtube.com/watch?v=Je0B3nHhKmM, and added to it the ability to register, log in, and if the user is logged in then show the average of all the scores of the games played by the user.

During registration has been added password hashing and creation of new databases in the databases folder, during login encoding and decoding of the token in cookies, which is used to check if the user is logged in, and if he is then his name is shown in the upper left corner, and the results of each game are saved when the reset button is pressed.