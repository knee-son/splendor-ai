### backlogs
- ✅ make sure observation shape aligns with observation space
  - ✅ run assert if the **observation** aligns with the **observation space**
- ✅ materialize game state structure and provide initial state
  - ✅ successfully send API response to frontend
- ✅ merge `refactor-backend` branch
- 🔧 there was an issue with `generate_cards_json`'s sorting because it was vibe coded
  - 📝 learned that tuples can be generated via list comprehension, and sort keys can't be lists since they're not hashable, only tuples are allowed
- ✅ generate ANSI representation of game state
  - done and dusted 🤗
- ✅ did a little sidequest and make the game ~~playable~~ renderable for the frontend
  - learned that setting a useState is async

### now
- ✅ ansi will output on backend terminal (done)
  - while all training and triggering will be done on ministry frontend
  - hence, websocket fits perfect for this use case
- let's work on backend and implement `step()`
  - after `step()`, send ws event to FE
- holy fuck, i need to migrate to ASGI

---
### others
- we may want to use Phaser as rendering engine for FE

### very, very, veryyyyyy far along the way
  - visualize NN activations, inputs, and outputs [frontend]
