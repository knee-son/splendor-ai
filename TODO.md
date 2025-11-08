### backlogs
- ✅ make sure observation shape aligns with observation space
  - ✅ run assert if the **observation** aligns with the **observation space**
- ✅ materialize game state structure and provide initial state
  - ✅ successfully send API response to frontend
- ✅ merge `refactor-backend` branch
- 🔧 there was an issue with `generate_cards_json`'s sorting because it was vibe coded
  - 📝 learned that tuples can be generated via list comprehension, and sort keys can't be lists since they're not hashable. only tuples are allowed

### now
- generate ANSI representation of game state
  - ansi will output on backend terminal
  - while all training and triggering will be done on ministry frontend
- let's do a little sidequest and make the game playable for the frontend
- deprio anything related with acquiring agents' `_get_observation()`

---
### others
- none 🥳

### very, very, veryyyyyy far along the way
  - visualize NN activations, inputs, and outputs [frontend]
