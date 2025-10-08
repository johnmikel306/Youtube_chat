# Streamlit Configuration

This folder contains Streamlit configuration files for the YouTube Q&A application.

## Files

### `config.toml`
Main configuration file with ChatGPT-inspired theme settings:
- **Primary Color**: `#10a37f` (ChatGPT green)
- **Background**: White with light gray secondary
- **Text Color**: Dark gray for readability

### `secrets.toml` (not tracked)
Store your API keys here for local development:

```toml
GROQ_API_KEY = "your-api-key-here"
```

**Note**: This file is gitignored for security. Never commit API keys!

## Customization

You can customize the theme by editing `config.toml`. See [Streamlit theming docs](https://docs.streamlit.io/library/advanced-features/theming) for more options.

