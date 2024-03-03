import asyncio
from app import create_app

async def main():
    app = await create_app()
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
