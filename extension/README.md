# TubeMind AI Chrome Extension

A Manifest V3 React popup that detects the current YouTube video and connects it to the TubeMind FastAPI backend.

## Development

```bash
npm install
npm run dev
npm run build
```

Load `extension/dist` as an unpacked extension at `chrome://extensions`. The default backend is `http://localhost:8000`; change it from the popup settings if needed.

The optional OpenAI key is stored in Chrome local storage and sent as `X-OpenAI-API-Key`. Chat state is saved per YouTube video in Chrome local storage.
