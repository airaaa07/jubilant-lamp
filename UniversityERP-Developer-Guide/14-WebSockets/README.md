# 14-WebSockets

## Purpose

This folder provides comprehensive documentation about WebSockets in the University ERP system. It details how WebSockets are used for real-time communication, event broadcasting, and live updates.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses WebSockets for real-time features. Understanding WebSockets is critical for:
- Implementing real-time updates
- Broadcasting events
- Live notifications
- Debugging WebSocket issues
- Optimizing WebSocket performance

Without understanding WebSockets, developers may struggle with real-time features or may introduce WebSocket-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn WebSockets
- **Feature Development**: Implementing real-time features
- **Code Reviews**: Reviewing WebSocket code
- **Real-Time Updates**: Implementing live updates
- **Notifications**: Broadcasting notifications

## Dependencies

### WebSockets Dependencies

**Confirmed by Code**: WebSockets depend on:

- **@nestjs/websockets**: NestJS WebSocket module
- **@nestjs/platform-socket.io**: Socket.IO adapter
- **socket.io**: Socket.IO client and server
- **Redis**: For scaling WebSocket connections
- **Environment Variables**: WebSocket configuration

## Internal Architecture

### WebSockets Architecture

**Confirmed by Code**: WebSockets follow event-driven architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Client                                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Socket.IO Client                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              WebSocket Gateway                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              WebSocket Gateway Adapter                      │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Events       │  │  Rooms          │  │  Namespaces    │
│  (Messages)   │  │  (Groups)       │  │  (Isolation)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### WebSocket Gateway

**Confirmed by Code**: WebSocket gateway handles WebSocket connections.

**NotificationsGateway**:
```typescript
import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  OnGatewayConnection,
  OnGatewayDisconnect,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({
  cors: {
    origin: '*',
  },
})
export class NotificationsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  async handleConnection(client: Socket) {
    const userId = client.handshake.query.userId as string;
    if (userId) {
      client.join(`user:${userId}`);
      console.log(`Client connected: ${client.id}, User: ${userId}`);
    }
  }

  async handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
  }

  @SubscribeMessage('join-room')
  handleJoinRoom(@MessageBody() data: { room: string }, @ConnectedSocket() client: Socket) {
    client.join(data.room);
    return { event: 'joined', room: data.room };
  }

  @SubscribeMessage('leave-room')
  handleLeaveRoom(@MessageBody() data: { room: string }, @ConnectedSocket() client: Socket) {
    client.leave(data.room);
    return { event: 'left', room: data.room };
  }

  async sendNotificationToUser(userId: string, notification: any) {
    this.server.to(`user:${userId}`).emit('notification', notification);
  }

  async broadcastToRoom(room: string, event: string, data: any) {
    this.server.to(room).emit(event, data);
  }
}
```

**What This Does**:
- **@WebSocketGateway**: Decorator for WebSocket gateway
- **handleConnection**: Handles client connection
- **handleDisconnect**: Handles client disconnection
- **@SubscribeMessage**: Handles incoming messages
- **sendNotificationToUser**: Sends notification to specific user
- **broadcastToRoom**: Broadcasts to room

### WebSocket Module

**Confirmed by Code**: WebSocket module provides WebSocket integration.

**WebsocketsModule**:
```typescript
import { Module } from '@nestjs/common';
import { NotificationsGateway } from './notifications.gateway';

@Module({
  providers: [NotificationsGateway],
  exports: [NotificationsGateway],
})
export class WebsocketsModule {}
```

**What This Does**:
- **Providers**: Provides WebSocket gateways
- **Exports**: Exports gateways for other modules

## Database Interactions

### WebSockets-Database Flow

**Confirmed by Code**: WebSockets don't interact with database directly.

**Flow**:
```
WebSockets → No database interaction
```

## Redis Interactions

### WebSockets-Redis Flow

**Confirmed by Code**: WebSockets can use Redis for scaling.

**Flow**:
```
WebSockets → Redis Adapter → Scale WebSocket Connections
```

## Queue Interactions

### WebSockets-Queue Flow

**Confirmed by Code**: WebSockets don't interact with queues.

**Flow**:
```
WebSockets → No queue interaction
```

## Worker Interactions

### WebSockets-Worker Flow

**Confirmed by Code**: Workers can broadcast via WebSockets.

**Flow**:
```
Worker → WebSocket Gateway → Broadcast Event
```

## Business Rules

### WebSockets Rules

**Confirmed by Code**: WebSockets follow these rules:

1. **Event-Driven**: Event-driven communication
2. **Rooms**: Clients can join rooms
3. **Namespaces**: Namespaces for isolation
4. **Authentication**: Authenticate connections
5. **Authorization**: Authorize room access

### Event Rules

**Confirmed by Code**: Event rules:

1. **Naming**: Use consistent event naming
2. **Data**: Send structured data
3. **Validation**: Validate event data
4. **Error Handling**: Handle errors gracefully
5. **Logging**: Log all events

## Security

### WebSockets Security

**Confirmed by Code**: Security considerations for WebSockets:

1. **Authentication**: Authenticate connections
2. **Authorization**: Authorize room access
3. **CORS**: Configure CORS properly
4. **Rate Limiting**: Rate limit events
5. **Input Validation**: Validate event data

## Performance Considerations

### WebSockets Performance

**Confirmed by Code**: Performance considerations:

1. **Connection Pooling**: Use connection pooling
2. **Redis Adapter**: Use Redis adapter for scaling
3. **Event Throttling**: Throttle events if needed
4. **Room Management**: Manage rooms efficiently
5. **Connection Limits**: Limit concurrent connections

## Common Mistakes

### Mistake 1: Not Authenticating Connections

**Symptom**: Unauthorized access

**Cause**: Not authenticating connections

**Fix**:
```typescript
// Authenticate connection
async handleConnection(client: Socket) {
  const token = client.handshake.auth.token;
  const user = await this.authService.validateToken(token);
  if (!user) {
    client.disconnect();
    return;
  }
  client.join(`user:${user.id}`);
}
```

### Mistake 2: Not Validating Event Data

**Symptom**: Invalid data processed

**Cause**: Not validating event data

**Fix**:
```typescript
// Validate event data
@SubscribeMessage('send-message')
handleSendMessage(@MessageBody() data: SendMessageDto) {
  // DTO validation
}
```

### Mistake 3: Not Handling Disconnections

**Symptom**: Memory leak

**Cause**: Not handling disconnections

**Fix**:
```typescript
// Handle disconnection
async handleDisconnect(client: Socket) {
  // Cleanup
  client.leaveAll();
}
```

## Debugging Guide

### WebSockets Debugging

**Issue**: WebSocket not working

**Investigation**:
1. Check WebSocket connection
2. Check event handling
3. Check room membership
4. Check authentication
5. Check logs

**Tools**:
- Socket.IO client debugger
- WebSocket logs
- Network tab in browser
- Console logs

## Future Enhancements

### Redis Adapter

**Status**: Not implemented

**Proposal**: Implement Redis adapter:
- Scale WebSocket connections
- Multiple server support
- Better scalability
- More complex
- Better for production

### Presence System

**Status**: Not implemented

**Proposal**: Implement presence system:
- User online status
- Typing indicators
- Better user experience
- More complex
- Better for real-time features

## Production Considerations

### Production WebSockets

**Production Deployment**:
- Enable authentication
- Enable authorization
- Configure CORS
- Use Redis adapter
- Monitor connections

### WebSockets Monitoring

**Monitoring Metrics**:
- Connection count
- Event rate
- Room count
- Error rate
- Message latency

## Example Requests

### WebSockets Example

**Connect**:
```javascript
const socket = io('http://localhost:3000', {
  auth: { token: 'jwt-token' },
  query: { userId: 'user-id' },
});
```

**Join Room**:
```javascript
socket.emit('join-room', { room: 'notifications' });
```

## Example Responses

### WebSockets Response

**Event Received**:
```javascript
socket.on('notification', (data) => {
  console.log('Notification:', data);
});
```

## Sequence Diagrams

### WebSockets Flow

```
Client → Connect → Gateway → Join Room → Send Event → Broadcast → Client Receives
```

## Architecture Diagrams

### WebSockets Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Socket.IO Client                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  WebSocket Gateway                         │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Events       │  │  Rooms          │  │  Namespaces    │
│  (Messages)   │  │  (Groups)       │  │  (Isolation)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How are WebSockets used in the system?

**Answer**: WebSockets via:
- Real-time notifications
- Live updates
- Event broadcasting
- Room-based communication
- User-specific messaging

### Q2: How do you implement real-time notifications?

**Answer**: Real-time notifications via:
- WebSocket gateway
- User joins user-specific room
- Service broadcasts to user room
- Client receives notification
- Display notification to user

### Q3: How do you scale WebSocket connections?

**Answer**: Scale WebSockets via:
- Redis adapter
- Multiple WebSocket servers
- Load balancing
- Sticky sessions
- Connection limits

## Exercises

### Exercise 1: Create a WebSocket Gateway

**Task**: Create a custom WebSocket gateway.

**Steps**:
1. Create gateway class
2. Add @WebSocketGateway decorator
3. Implement connection handling
4. Implement message handling
5. Test gateway

**Verification**:
- Gateway created
- Connection works
- Message handling works
- Events emitted
- Tests pass

### Exercise 2: Implement Room-Based Communication

**Task**: Implement room-based communication.

**Steps**:
1. Add join-room handler
2. Add leave-room handler
3. Add broadcast method
4. Test room communication
5. Test multiple clients

**Verification**:
- Room join works
- Room leave works
- Broadcast works
- Multiple clients work
- Tests pass

## Real Production Scenarios

### Scenario 1: WebSocket Connection Failed

**Situation**: WebSocket connection failed

**Response**:
1. Check WebSocket server
2. Check authentication
3. Check CORS configuration
4. Fix configuration
5. Test connection

### Scenario 2: Events Not Received

**Situation**: Events not received by client

**Response**:
1. Check room membership
2. Check event emission
3. Check event subscription
4. Fix event handling
5. Test events

## Navigation

**Next Section**: [01-Real-Time-Notifications](./01-Real-Time-Notifications.md)

**Previous Section**: [13-MinIO](../13-MinIO/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [11-Workers](../11-Workers/README.md) - Workers details
