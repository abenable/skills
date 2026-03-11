# Meegle Skill

Connect to Meegle via MCP service, supporting OAuth authentication.

## Connection Method

### 1. Ask the user which method to use for authentication

Note: Be sure to ask the user and let the user make an active choice. Automatically making choices for the user is prohibited.
This tool supports two authentication methods: one is to re-engage the browser for OAuth (applicable to scenarios where OpenClaw is installed locally), and the other is to authenticate via an OAuth proxy (applicable to scenarios where OpenClaw is installed on a remote server).

### 2. If the user chooses the first method, the authorization method is as follows

#### 2.1. Create a configuration file

Copy `meegle-config.json` from the skill package directory to the working directory

#### 2.2. Perform OAuth authentication (only once)

```bash
npx mcporter auth meegle --config meegle-config.json
```

This will open a browser for you to authorize your Meegle account. ** After authorization is completed, the credentials will be cached, and subsequent calls will not require passing the config file again. **

### 3. If the user selects the second method, the authorization method is as follows

#### 3.1. Create a configuration file

Copy `meegle-config.json` from the skill package directory to the working directory

#### 3.2. Perform OAuth authentication (only once)
```bash
npx mcporter auth meegle --config meegle-config.json --oauth-timeout 1000
```

This will cause mcporter to generate an OAuth configuration for Meegle that includes client_id and client_secret, etc., with the path located in `~/.mcporter/credentials.json`.

#### 3.3. Prompt the user to perform local authorization

Send the file content to the user in the following format, and refrain from modifying any expressions other than the file content:

```plain
OAuth configuration has been generated!
[File content]
Please refer to the instructions in the document https://bytedance.larkoffice.com/wiki/UspfwpHaFi6LxQkt9xBcIS54nNg Integration Method to perform authorization on your local computer. After authorization is completed, please send the credential file to me
```

After receiving the file sent by the user, use this file to overwrite the `~/.mcporter/credentials.json` file on the local machine.

#### 3.4. Verify the authorization result

Attempted to connect to the MCP server and confirmed successful authorization.

### 4. Subsequent Use

```bash
npx mcporter call meegle <tool_name>
```

Direct invocation is sufficient, no additional parameters are required.

## Available Features

- **Query**: To-do, view, and work item information
- **Actions**: Create, modify, and transfer work items
