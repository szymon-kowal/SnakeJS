# Snake but in JS

I used : HTML, CSS, JS, Python, FastAPI, Starlette

The main purpose of writing this page was to learn the fast api and how the relationship between user and server works and how it can be influenced, so the visual side is terrible LOL.

I slightly edited the game created by https://www.youtube.com/watch?v=Je0B3nHhKmM, and added to it the ability to register, log in, and if the user is logged in then show the average of all the scores of the games played by the user.

During registration has been added password hashing and creation of new databases in the databases folder, during login encoding and decoding of the token in cookies, which is used to check if the user is logged in, and if he is then his name is shown in the upper left corner, and the results of each game are saved when the reset button is pressed.

You can reset the game by pressing RESET button. 

To run this website you need to download some of libraries such as : sqlite3, starlette, FastApi and Uvicore.
After downloading these things you have to type in the terminal following code without brackets : " uvicorn main:app ".
Have fun !
