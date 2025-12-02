# Effectiva API Reference

## Base URL
`http://localhost:8000`

## Core Endpoints

### Health Check
- **GET** `/health`
  - Returns status of the backend.

## Optimizer Management

### Create Optimizer
- **POST** `/api/optimizers`
  - Body: `{"agent_name": str, "optimizer_type": str, "name": str, "config": dict}`
  - Creates a new optimizer configuration.

### Get Agent Optimizers
- **GET** `/api/optimizers/agent/{agent_name}`
  - Returns list of optimizers for the specified agent.

### Deactivate Optimizer
- **DELETE** `/api/optimizers/{optimizer_id}`
  - Deactivates the specified optimizer.

## Toon Format

### Create Config
- **POST** `/api/toon/config`
  - Body: `{"agent_name": str, "enabled": bool, "config": dict}`
  - Creates Toon configuration for an agent.

### Get Config
- **GET** `/api/toon/config/{agent_name}`
  - Returns Toon configuration.

### Toggle Toon
- **PATCH** `/api/toon/config/{agent_name}/toggle?enabled={bool}`
  - Enables or disables Toon format.

### Encode Message
- **POST** `/api/toon/encode`
  - Body: `{"message": dict, "message_type": str}`
  - Encodes a message to Toon format and returns savings metrics.

### Decode Message
- **POST** `/api/toon/decode`
  - Body: `toon_str` (query param) or body
  - Decodes a Toon string.

## Built-in Tools

### Register Tool
- **POST** `/api/tools/register/{tool_key}`
  - Registers a specific built-in tool.

### Register All Tools
- **POST** `/api/tools/register-all`
  - Registers all available built-in tools.

### List Tools
- **GET** `/api/tools`
  - Lists all active tools.

### List Available Tools
- **GET** `/api/tools/available`
  - Lists all tools that can be registered.

### Get Tools by Category
- **GET** `/api/tools/category/{category}`
  - Categories: `web`, `utility`, `file`, `code`, `system`.

### Get Recommended Tools
- **GET** `/api/tools/recommended/{agent_context}`
  - Contexts: `study`, `work`, `life`, `scheduling`, `coordinator`.

### Toggle Tool
- **PATCH** `/api/tools/{tool_id}/toggle?active={bool}`
  - Activates or deactivates a tool.
