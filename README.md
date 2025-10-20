## statement of the problem
i've been losing too much on this game so i'll train AI to train me to get better at Splendor

### roadmap
- [x] import Splendor cards and nobles data
    - [ ] cross-check cards with visuals
- [ ] compose game structure and rules
    - [ ] present initial game states
    - [ ] validate some game states
- [ ] compose game API
- [ ] make AI model
- [ ] train

## buildout
### on `backend`
- `python14 -m venv venv`
- `pip install -r requirements.txt`
- `cp .env.example .env`
- run using `./serve`

### on `frontend-ministry`
- `npm i`
- `cp .env.example .env`
- run using `npm run dev`

## cards_minified.json
source: https://www.scribd.com/document/534963546/Splendor-Card-List-With-Pics

**cards_minified.json** >>  `python scripts/convert_minify_to_cards.py` > **cards.json**
