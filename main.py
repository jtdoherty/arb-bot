import asyncio
from kalshi import KalshiClient
from polymarket import PolymarketClient
from data import OrderBookManager
from arbitrage import ArbitrageBot, run_arbitrage_bot

async def run_kalshi(kalshi_client):
    await kalshi_client.run()

async def run_order_book_manager(order_book_manager):
    while True:
        order_book_manager.print_comparison()
        await asyncio.sleep(2)

async def main():
    # You can choose which mode to run:
    # 1. Original order book comparison mode
    # 2. New arbitrage bot mode
    mode = "arbitrage"  # Change to "order_book" for original mode
    
    if mode == "arbitrage":
        await run_arbitrage_bot()
    else:
        kalshi_client = KalshiClient()
        polymarket_client = PolymarketClient()
        polymarket_client.run()
        order_book_manager = OrderBookManager(kalshi_client, polymarket_client)
        kalshi_task = asyncio.create_task(run_kalshi(kalshi_client))
        
        # Wait longer for initial data
        await asyncio.sleep(1)

        try:
            await run_order_book_manager(order_book_manager)
        except KeyboardInterrupt:
            print("Shutting down...")
            kalshi_task.cancel()
            try:
                await kalshi_task
            except asyncio.CancelledError:
                print("Kalshi task cancelled successfully")

if __name__ == "__main__":
    asyncio.run(main())