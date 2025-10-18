## buildout
### on `backend`
- `python14 -m venv venv`
- `pip install -r requirements.txt`
- `cp .env.example .env`
#### running backend
- `source venv/bin/activate` or `source venv/Scripts/activate` for cringy Windows
- run using `python serve.py`

### on `frontend-ministry`
- `npm i`
- `cp .env.example .env`
- run using `npm run dev`

## cards_minified.json
source: https://www.scribd.com/document/534963546/Splendor-Card-List-With-Pics

**cards_minified.json** >>  `python scripts/convert_minify_to_cards.py` > **cards.json**
