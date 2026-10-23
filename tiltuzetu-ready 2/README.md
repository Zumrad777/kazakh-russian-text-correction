# TilTüzету — ready-to-run MVP

A small FastAPI web app for demonstrating the workflow: enter Kazakh/Russian mixed text → review rule-based spelling suggestions → translate approved text → optionally save activity in MongoDB Atlas.

## Run on macOS

1. Download and unzip the project.
2. Open the `tiltuzetu-ready` folder in VS Code.
3. Open **Terminal → New Terminal** and run:

   ```bash
   chmod +x start.sh
   ./start.sh
   ```

4. Open **http://127.0.0.1:8000**. API documentation: **http://127.0.0.1:8000/docs**.
5. Keep Terminal open while the app is running. Stop it with `Control + C`.

## Translation API

The MVP calls the MyMemory Translation API for basic requests, so you do not need to create a Google Cloud or FreedomSpeech key to try it. It is an external service; it needs internet access, has usage limits, and may not support every language pair or mixed-language sentence reliably. The app reports provider errors rather than pretending that an arbitrary translation succeeded. Short built-in phrases are used only as a clearly labelled fallback demo.

Supported UI language choices are Kazakh (`kk`), Russian (`ru`) and English (`en`). Test the specific language pairs you intend to demonstrate. This is a prototype, not a validated production translation system.

## Optional MongoDB Atlas history

MongoDB is the database, not the translation engine. You can demonstrate the website without it; adding MongoDB enables saving correction and translation history.

1. Sign in at https://www.mongodb.com/atlas and create a **Free (M0)** cluster.
2. In Atlas, create a database user with a password and add your current IP address under Network Access.
3. Open **Connect → Drivers** and copy the connection string. Replace the password placeholder with the database user's password. If the password has special characters, URL-encode them.
4. In this project folder, copy `.env.example` to a file named `.env`.
5. In `.env`, set:

   ```dotenv
   MONGODB_URI=mongodb+srv://YOUR_USER:YOUR_PASSWORD@YOUR_CLUSTER/tiltuzetu?retryWrites=true&w=majority
   MONGODB_DATABASE=tiltuzetu
   ```

   Use your actual Atlas connection string, not the example above.
6. Save the file and restart the server. `/api/health` should report `database_connected: true`; `/api/history` will return recent saved items.

Never send the MongoDB connection string or password in chat, screenshots, or GitHub. The `.gitignore` file excludes `.env`.

## API endpoints

- `GET /api/health` — backend and database status.
- `GET /api/config` — active modes and options.
- `POST /api/correct` — demo spelling correction.
- `POST /api/translate` — external translation request.
- `GET /api/history` — recent history if MongoDB is configured.
- `GET /docs` — interactive Swagger UI.

Example correction request:

```bash
curl -X POST http://127.0.0.1:8000/api/correct \
  -H 'Content-Type: application/json' \
  -d '{"text":"Салем, казакша калай жазам?"}'
```

Example translation request:

```bash
curl -X POST http://127.0.0.1:8000/api/translate \
  -H 'Content-Type: application/json' \
  -d '{"text":"Сәлем","source_language":"kk","target_language":"en"}'
```

## Honest limitations

- Spelling correction uses a small set of transparent rules. It is **not** a trained ByT5/mT5 model and cannot reliably correct arbitrary mixed text.
- MyMemory is a third-party service. Availability, language coverage, quality and limits may vary. Check results before presenting them as validated translations.
- MongoDB history is optional. Without `MONGODB_URI`, the app still runs, but does not persist history.
