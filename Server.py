import asyncio
import random
import json

HOST, PORT = "0.0.0.0", 8080

clients = []

async def broadcast(msg):
    for writer, _ in clients:
        try:
            writer.write((msg + "\n").encode())
            await writer.drain()
        except:
            pass

async def client_handler(reader, writer):
    data = await reader.read(1024)
    msg = json.loads( data.decode().strip())

    name = msg.get("name")
    clients.append((writer, name))

    print(f"[SERVER] connected {name}")

    await broadcast(f"{name} connected to game")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            msg=data.decode().strip()
            cmd = json.loads(msg).get("cmd")
            if cmd == "roll":
                roll = random.randint(1,6)
                await broadcast(f"{name} got: {roll}")
    except:
        pass

async def main():

    server = await asyncio.start_server(None, HOST, PORT)
    print(f"[server] Listen on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
