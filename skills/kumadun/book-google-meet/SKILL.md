---
name: book-google-meet
description: Book Google Meet meetings from the command line.
# Registry Metadata:
# - Required binaries: gog (for OAuth credential management)
# - Optional env vars: GOG_CREDENTIALS_PATH (custom path to gog credentials)
# - Install methods: brew (macOS/Linux), manual download (Windows)
metadata: {"clawbot":{"emoji":"🎥","requires":{"bins":["gog"],"envVars":["GOG_CREDENTIALS_PATH"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"},{"id":"manual-windows","kind":"manual","label":"Windows users - gog cannot be installed via brew","instructions":"gog is not available via Homebrew on Windows. Install options: 1) Download from: https://github.com/steipete/gogcli/releases 2) Or install via Go: go install github.com/steipete/gogcli@latest"}]}}
---

> ⚠️ **Required Binary**: This skill requires the `gog` CLI tool for OAuth credential management. See installation instructions below.

# book-google-meet

Create Google Meet spaces with custom access settings using the Google Meet API v2.

## Prerequisites

### 1. Install gog CLI

gog is **required** for OAuth authentication.

**macOS/Linux:**
```bash
brew install steipete/tap/gogcli
```

**Windows:**
```powershell
# gog is not available via Homebrew on Windows
# Download from: https://github.com/steipete/gogcli/releases
# Or install via Go:
go install github.com/steipete/gogcli@latest
```

> ⚠️ **Windows users**: gog cannot be installed via brew. Please download the binary from the releases page or install with Go.

### 2. Authenticate with gog

```bash
gog auth credentials /path/to/client_secret.json
gog auth add your@email.com --services meet
gog auth list
```

> **Note**: Use `--services meet` (not `calendar`) to ensure the correct OAuth scope is requested for the Meet API.

### 3. Enable Google Meet API

Go to: https://console.developers.google.com/apis/api/meet.googleapis.com/overview

Enable the **Google Meet API** for your project.

### 4. Install Python Dependencies

```bash
pip install google-auth google-auth-oauthlib
```

## Required OAuth Scope

```
https://www.googleapis.com/auth/meetings.space.created
```

## API Endpoint

```
POST https://meet.googleapis.com/v2/spaces
```

## SpaceConfig Options

### AccessType
| Value | Description |
|-------|-------------|
| `OPEN` | Anyone with the link can join without knocking |
| `TRUSTED` | Org members + invited external users can join without knocking |
| `RESTRICTED` | Only invitees can join without knocking |

### ArtifactConfig
| Config | Option | Description |
|--------|--------|-------------|
| `recordingConfig` | `autoRecordingGeneration: ON` | Auto-record when privileged user joins |
| `transcriptionConfig` | `autoTranscriptionGeneration: ON` | Auto-transcribe when privileged user joins |

## Request Body Example

```json
{
  "config": {
    "accessType": "OPEN",
    "entryPointAccess": "ALL",
    "artifactConfig": {
      "recordingConfig": {
        "autoRecordingGeneration": "ON"
      },
      "transcriptionConfig": {
        "autoTranscriptionGeneration": "ON"
      }
    }
  }
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| `name` | Unique space identifier (e.g., `spaces/-yy3uKlef_QB`) |
| `meetingUri` | Full URL to join (e.g., `https://meet.google.com/cka-oqpj-ohs`) |
| `meetingCode` | Short code for joining (e.g., `cka-oqpj-ohs`) |
| `config.accessType` | Access control setting |
| `config.artifactConfig` | Recording/transcription settings |

## Usage

### Basic Usage

```bash
python create_meet_space.py
```

First run opens browser for OAuth authorization. Token is cached in `meet_token.pickle`.

### Command Line Options

```bash
# Use custom credentials file
python create_meet_space.py --credentials /path/to/credentials.json

# Or set environment variable
export GOG_CREDENTIALS_PATH=/path/to/credentials.json
python create_meet_space.py

# Create meeting with restricted access
python create_meet_space.py --access-type RESTRICTED

# Disable auto-recording or transcription
python create_meet_space.py --no-recording
python create_meet_space.py --no-transcription
```

## How It Works

1. **Load gog credentials** from gog's stored credentials file
2. **OAuth flow** — authenticate with Google (scope: `meetings.space.created`)
3. **Cache token** in `meet_token.pickle` for future runs
4. **Call Meet API v2** — `POST /v2/spaces` with config
5. **Return meeting details** — URI, code, access settings

### Credential File Location

The script loads client credentials from gog's stored credentials. By default, this is:
- **Windows**: `%APPDATA%/gogcli/credentials.json`
- **macOS/Linux**: `~/.config/gogcli/credentials.json`

To use a custom credentials file, set the environment variable:
```bash
export GOG_CREDENTIALS_PATH=/path/to/credentials.json
```

## Notes

- **No Calendar event created** — this is a standalone Meet space
- **Auto-recording** requires a user with recording privileges to join
- **Auto-transcription** requires a user with transcription privileges to join
- Recordings and transcriptions are saved to Google Drive

## Troubleshooting

### 403 PERMISSION_DENIED — API Not Enabled
Enable Meet API at:
```
https://console.developers.google.com/apis/api/meet.googleapis.com/overview?project=YOUR_PROJECT_ID
```

### 401 UNAUTHENTICATED — Invalid Credentials
- Delete `meet_token.pickle` to force re-authentication

## Files

- `create_meet_space.py` — Main script
- `meet_token.pickle` — Cached OAuth credentials (auto-generated)

### Security Notes

⚠️ **Sensitive Files**: The following files contain credentials and should be protected:

| File | Description | Security Recommendation |
|------|-------------|------------------------|
| `meet_token.pickle` | Cached OAuth tokens (access token + refresh token) | Keep in a secure directory; delete when no longer needed |
| `gogcli/credentials.json` | OAuth client credentials | Protect with appropriate file permissions; do not commit to version control |

**To delete cached credentials:**
```bash
rm meet_token.pickle  # Force re-authentication on next run
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOG_CREDENTIALS_PATH` | Path to gog credentials JSON file | Windows: `%APPDATA%/gogcli/credentials.json`<br>macOS/Linux: `~/.config/gogcli/credentials.json` |

## References

- Google Meet API docs: https://developers.google.com/workspace/meet/api/guides
- Spaces resource: https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces
- gog CLI: https://github.com/steipete/gogcli
