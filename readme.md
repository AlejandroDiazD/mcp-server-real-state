# Backend Engineering Challenge – Real Estate MCP Server

This project consists of a Model Context Protocol (MCP) Server designed to bridge the gap between Large Language Models (LLMs) and a private real estate database. The server enables AI agents through different tools to autonomously query property data, manage the catalog, and generate SEO-optimized marketing content.

The project is structured into a modular architecture with different layers (Core, Domain, Infra, Server, Services), ensuring separation of concerns. It features a non-blocking asynchronous design using asyncio to handle concurrent database operations and external API calls efficiently. The solution includes robust security via Bearer Token authentication, persistent storage with SQLite, and a standardized JSON communication layer optimized for AI interaction.

## 1. MCP Tools
- `search_properties`: Advanced filtered search by city, price range, and property status (available/sold).
- `get_property_details`: Comprehensive retrieval of full technical specifications for a specific property.
- `generate_listing_content`: An automated pipeline that generates SEO-ready HTML snippets (including `<title>` and `<meta>` tags) with customizable language and tone.
- `add_property`: Secure registration of new listings with enforced schema validation and persistent String IDs.
- `update_property`: Update capability to modify specific fields without resending the entire record.
- `delete_property`: Permanent removal of property records from the database via unique identifiers.
- `seed_data`: Built-in utility to initialize the database with sample records for testing and demonstration.

## 2. Deployment
The setup is Docker-based.

### Requirements
* Docker 20+
* Docker Compose v2+

### Configuration 
The service configuration uses environment variables inside the container. In this case, all the necessary parameters can be modified in the docker-compose file:
| Variable                   | Description                                              |
| -------------------------- | ---------------------------------------------------------|
| `APP_NAME`                 | The display name used to identify the MCP server         |
| `APP_API_TOKEN`            | Secret key required for Bearer Token authentication      |
| `DATABASE_URL`             | Connection string for the SQLite database file           |
| `HOST`                     | Network interface address the server will bind to        |
| `PORT`                     | TCP port number the server will listen on                |
| `FASTMCP_DEBUG`            | Boolean flag to enable or disable detailed debugging mode|
| `FASTMCP_LOG_LEVEL`        | Verbosity level of application logs (e.g., INFO, DEBUG)  |

### Running the application
```bash
docker compose up --build
```

After the first build, you can restart without rebuilding:
```bash
docker compose up
```

### Running MCP Inspector
The MCP inspector is launched with the bearer token already loaded. In this challenge, the test secret key has been set as: 'secret_token_2026':
```bash
npx @modelcontextprotocol/inspector http://localhost:8000/sse --header "Authorization: Bearer secret_token_2026"
```

## 3. Design Criteria
### Architecture
I opted for a layered modular architecture (Core, Domain, Infra, Server, Services) to strictly enforce the separation of concerns. By decoupling the business logic from the transport protocol and the persistence layer, I’ve ensured the system is both maintainable and extensible. This structure minimizes side effects, allowing individual components—such as the database engine or the MCP interface—to be modified or swapped without impacting the rest of the application.

### Asynchronous Design

Since the MCP protocol is inherently asynchronous, I implemented a non-blocking execution model to maintain high server responsiveness. By offloading synchronous database I/O to worker threads via asyncio.to_thread, I ensured the event loop remains unblocked. This is key because it prevents disk I/O from becoming a bottleneck. By keeping the event loop free, the server stays snappy and provides the model with immediate feedback, even when we're handling heavy data operations in the background.

### Database Integration

I went with SQLite primarily for portability. In a challenge setting, a zero-config, standalone file is the most pragmatic choice to ensure the project is "plug-and-play," although PostgreSQL would be the standard for a production environment. I chose SQL over NoSQL because real estate records are inherently structured. A relational model provides native schema enforcement and data integrity out of the box, whereas NoSQL would force us to handle those consistency checks manually within the application logic.

### Authentication

I went with Bearer Token authentication as it’s a straightforward, industry-standard pattern. It provides exactly the right balance for this project: securing sensitive write operations (like adding or deleting properties) via the Authorization header without over-engineering the auth flow. It’s reliable, easy to implement for any client, and fits perfectly with the stateless nature of the MCP protocol.

### Transport

I implemented the SSE (Server-Sent Events) transport to meet the requirement for cloud-readiness and simplified testing over HTTP. Beyond compliance, SSE is a much more robust choice for Dockerized environments compared to local alternatives like stdio. It integrates seamlessly with standard web infrastructure and reverse proxies, ensuring a stable, production-ready communication channel that is easy to monitor and debug during deployment.

### Edge cases and Error handling
I prioritized system resilience by implementing a centralized error formatter. Instead of silent failures or generic errors, the server returns structured JSON feedback for edge cases like invalid IDs or schema mismatches. This provides the LLM with enough context to understand why a request failed, allowing it to autonomously correct its parameters and retry without human intervention.

## 4. Future improvements
* Real AI based Content Generator
* MCP Resource implementation according to requirements
* MCP Prompt template implementation according to requirements
* Unit tests

_This repository is provided as part of the InteractiveAI Backend Engineer Challenge and is intended for evaluation purposes._