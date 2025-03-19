#!/usr/bin/env python

import os
import sys
import json
import time

os.system('title w-AI-fu NovelAI TTS (Mock)')

print("WARNING: This is a mock TTS service. Audio generation is disabled.", file=sys.stderr)
print("To enable audio generation, install websockets and required dependencies:", file=sys.stderr) 
print("  pip install websockets==10.4", file=sys.stderr)

# Create a dummy websocket server using standard libraries
import socket
import threading

class MockWebSocketServer:
    def __init__(self, host="127.0.0.1", port=8766):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.clients = []
        self.running = True
        
    def start(self):
        print(f"Mock WebSocket server started on {self.host}:{self.port}", file=sys.stderr)
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_thread.daemon = True
                client_thread.start()
                self.clients.append((client_socket, client_thread))
            except Exception as e:
                print(f"Error accepting connection: {e}", file=sys.stderr)
                break
                
    def handle_client(self, client_socket, address):
        print(f"Client connected: {address}", file=sys.stderr)
        try:
            # Perform WebSocket handshake
            data = client_socket.recv(1024).decode('utf-8')
            if "Upgrade: websocket" in data:
                # Very simple WebSocket handshake response
                key = ''
                for line in data.split('\r\n'):
                    if "Sec-WebSocket-Key" in line:
                        key = line.split(': ')[1]
                        break
                
                if key:
                    import base64
                    import hashlib
                    magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                    accept = base64.b64encode(hashlib.sha1((key + magic_string).encode('utf-8')).digest()).decode('utf-8')
                    
                    handshake = (
                        "HTTP/1.1 101 Switching Protocols\r\n"
                        "Upgrade: websocket\r\n"
                        "Connection: Upgrade\r\n"
                        f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
                    )
                    client_socket.send(handshake.encode('utf-8'))
                    
                    # Listen for commands and send fake responses
                    while True:
                        # For Mock service, just respond to any message with a positive result
                        try:
                            message = client_socket.recv(1024)
                            if not message:
                                break
                                
                            # Parse WebSocket frame (simplified)
                            if len(message) < 6:
                                continue
                                
                            # Try to decode the message
                            msg_text = ""
                            try:
                                # Simple WebSocket unmasking for text frames
                                if message[0] & 0x80:  # FIN bit set
                                    opcode = message[0] & 0x0F
                                    if opcode == 1:  # Text frame
                                        mask = message[1] & 0x80
                                        payload_len = message[1] & 0x7F
                                        
                                        if mask:
                                            mask_key_start = 2
                                            if payload_len == 126:
                                                mask_key_start = 4
                                            elif payload_len == 127:
                                                mask_key_start = 10
                                            
                                            mask_key = message[mask_key_start:mask_key_start+4]
                                            data_start = mask_key_start + 4
                                            payload = message[data_start:data_start+payload_len]
                                            
                                            unmasked = bytearray(len(payload))
                                            for i in range(len(payload)):
                                                unmasked[i] = payload[i] ^ mask_key[i % 4]
                                            
                                            msg_text = unmasked.decode('utf-8')
                            except Exception as e:
                                print(f"Error decoding WebSocket message: {e}", file=sys.stderr)
                            
                            # Generate and send a dummy response based on the received message
                            if "GENERATE" in msg_text:
                                # Extract the concurrent_id from the message
                                try:
                                    # Extract the JSON part
                                    json_str = msg_text.split('GENERATE ')[1]
                                    data = json.loads(json_str)
                                    concurrent_id = data.get('concurrent_id', 1)
                                    
                                    # Send a dummy response with the correct format
                                    dummy_id = "mock_audio_123"
                                    response = f"{concurrent_id} {dummy_id}"
                                    
                                    # Frame the response
                                    frame = bytearray([0x81])  # FIN + Text opcode
                                    payload = response.encode('utf-8')
                                    if len(payload) < 126:
                                        frame.append(len(payload))
                                    else:
                                        # For longer messages
                                        frame.append(126)
                                        frame.append((len(payload) >> 8) & 0xFF)
                                        frame.append(len(payload) & 0xFF)
                                    frame.extend(payload)
                                    
                                    client_socket.send(frame)
                                except Exception as e:
                                    print(f"Error processing GENERATE command: {e}", file=sys.stderr)
                            
                            elif "PLAY" in msg_text:
                                # Send a dummy PLAY DONE response
                                response = "PLAY DONE"
                                
                                # Frame the response
                                frame = bytearray([0x81])  # FIN + Text opcode
                                payload = response.encode('utf-8')
                                if len(payload) < 126:
                                    frame.append(len(payload))
                                else:
                                    # For longer messages
                                    frame.append(126)
                                    frame.append((len(payload) >> 8) & 0xFF)
                                    frame.append(len(payload) & 0xFF)
                                frame.extend(payload)
                                
                                client_socket.send(frame)
                                
                        except Exception as e:
                            print(f"Error handling client message: {e}", file=sys.stderr)
                            break
        except Exception as e:
            print(f"Error in client handler: {e}", file=sys.stderr)
        finally:
            try:
                client_socket.close()
            except:
                pass
            print(f"Client disconnected: {address}", file=sys.stderr)
                
    def stop(self):
        self.running = False
        for client, _ in self.clients:
            try:
                client.close()
            except:
                pass
        try:
            self.socket.close()
        except:
            pass
            
if __name__ == "__main__":
    try:
        server = MockWebSocketServer()
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_thread.start()
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("TTS Mock service shutting down", file=sys.stderr)
            server.stop()
            
    except Exception as e:
        print(f"Error in TTS Mock service: {e}", file=sys.stderr)
