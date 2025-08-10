
import asyncio
import logging
from mcp_server import MCPGitHubIssueServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    try:
        server = MCPGitHubIssueServer()
        logger.info('Starting MCP GitHub Issue Matcher server on port 5000...')
        
        # Override the server configuration to use port 5000
        import uvicorn
        config = uvicorn.Config(
            app=server.app,
            host='0.0.0.0',
            port=5000,
            log_level='info'
        )
        server_instance = uvicorn.Server(config)
        await server_instance.serve()
    except Exception as e:
        logger.error(f'Failed to start server: {e}')
        raise

if __name__ == '__main__':
    asyncio.run(main())
