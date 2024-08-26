import asyncio
import websockets
import json
import time

# Load the mock data from the JSON file
def load_mock_data():
    with open('mockdata.json', 'r') as file:
        return json.load(file)

async def send_example_data(websocket, path):
    print(f"Client connected: {websocket.remote_address}")

    # Load the mock data
    mock_data = load_mock_data()
    
    index = 0  # Start with the first element in the list
    try:
        while True:
            if index >= len(mock_data):
                index = 0  # Reset index if we reach the end of the list

            # Create the data to send
            data = {
                'timestamp': time.time(),
                'data': mock_data[index]
            }
            
            # Send the data as a JSON string
            await websocket.send(json.dumps(data))
            print(f"Sent data: {data}")
            
            # Increment index to send the next element in the list
            index += 1
            
            # Wait for 2 seconds before sending the next message
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {websocket.remote_address}, {e}")

# Start the WebSocket server
async def main():
    print("Starting WebSocket server...")
    async with websockets.serve(send_example_data, "localhost", 8765):
        print("WebSocket server is running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
