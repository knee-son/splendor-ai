## Splendor AI
I've been losing too much on this game. So I came up with the idea of training AI to train me to get better at Splendor.

### Tech Stack
- VITE React on TypeScript for frontend.
- FastAPI for communicating with the backend.
- Homebrew my own ORM and auth (?) if I'd like to deploy this for HvH or HvM.
- Use Gymnasium API to set up the game environment.
- CNN would be the initial model for the AI. Would venture to other models if it goes well.

### Roadmap
- [x] import Splendor cards and nobles data
    - [x] cross-check cards with visuals
- [ ] compose game structure and rules
    - [ ] present initial game states
    - [ ] validate some game states
- [x] compose game API (done-ish)
- [ ] make AI model
- [ ] train
- [ ] also do some unit tests 'cause every good boy does that

## buildout

### Very first thing to do before starting:
- please run `./run-me-first` to install stuff for first time use.

### on `backend/`
- run using `./serve`

### on `frontend-ministry/`
- run using `npm run dev`

## cards_minified.json
### source https://www.scribd.com/document/534963546/Splendor-Card-List-With-Pics
### conversion
**cards_minified.json** >>  `python scripts/generate_cards_json.py` > **cards.json**
