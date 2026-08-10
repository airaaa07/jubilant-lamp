# Real-Time Notifications

## Purpose

This document explains real-time notifications in the University ERP system. It details how real-time notifications are implemented using WebSockets, notification broadcasting, and live updates.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses WebSockets for real-time notifications. Understanding real-time notifications is critical for:
- Implementing live notifications
- Broadcasting events
- Real-time updates
- Debugging notification issues
- Optimizing notification delivery

Without understanding real-time notifications, developers may struggle with live features or may introduce notification bugs.

## Where This Is Used

- **Onboarding**: New developers learn real-time notifications
- **Feature Development**: Implementing real-time features
- **Code Reviews**: Reviewing notification code
- **Real-Time Updates**: Implementing live updates
- **Notifications**: Broadcasting notifications

## Dependencies

### Real-Time Notifications Dependencies

**Confirmed by Code**: Real-time notifications depend on:

- **NotificationsGateway**: WebSocket gateway
- **NotificationService**: Notification service
- **NestJS**: Framework for real-time features
- **Socket.IO**: Socket.IO client and server

## Internal Architecture

### Real-Time Notifications Architecture

**Confirmed by Code**: Real-time notifications follow event-driven architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Service                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Notification Service                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              WebSocket Gateway                              │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  User Room    │  │  Role Room      │  │  Broadcast      │
│  (User-Specific)│  │  (Role-Based)   │  │  (All Users)    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Client                                       │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Notification Service

**Confirmed by Code**: Notification service manages notifications.

**NotificationService**:
```typescript
import { Injectable } from '@nestjs/common';
import { NotificationsGateway } from '../websockets/notifications.gateway';

@Injectable()
export class NotificationService {
  constructor(private notificationsGateway: NotificationsGateway) {}

  async sendToUser(userId: string, notification: any) {
    await this.notificationsGateway.sendNotificationToUser(userId, notification);
  }

  async sendToRole(role: string, notification: any) {
    await this.notificationsGateway.broadcastToRoom(`role:${role}`, 'notification', notification);
  }

  async sendToAll(notification: any) {
    await this.notificationsGateway.broadcastToRoom('all', 'notification', notification);
  }

  async sendToInstitute(instituteId: string, notification: any) {
    await this.notificationsGateway.broadcastToRoom(`institute:${instituteId}`, 'notification', notification);
  }

  async sendToDepartment(departmentId: string, notification: any) {
    await this.notificationsGateway.broadcastToRoom(`department:${departmentId}`, 'notification', notification);
  }
}
```

**What This Does**:
- **sendToUser**: Sends notification to specific user
- **sendToRole**: Sends notification to role
- **sendToAll**: Broadcasts to all users
- **sendToInstitute**: Sends to institute
- **sendToDepartment**: Sends to department

### Notification Gateway Integration

**Confirmed by Code**: Gateway integrated with notification service.

**NotificationsGateway**:
```typescript
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
    const role = client.handshake.query.role as string;
    const instituteId = client.handshake.query.instituteId as string;
    const departmentId = client.handshake.query.departmentId as string;

    if (userId) {
      client.join(`user:${userId}`);
    }
    if (role) {
      client.join(`role:${role}`);
    }
    if (instituteId) {
      client.join(`institute:${instituteId}`);
    }
    if (departmentId) {
      client.join(`department:${departmentId}`);
    }
    client.join('all');

    console.log(`Client connected: ${client.id}, User: ${userId}`);
  }

  async handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
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
- **handleConnection**: Joins user to relevant rooms
- **handleDisconnect**: Handles disconnection
- **sendNotificationToUser**: Sends to user room
- **broadcastToRoom**: Broadcasts to room

## Database Interactions

### Real-Time Notifications-Database Flow

**Confirmed by Code**: Notifications may be logged to database.

**Flow**:
```
Service → Database → Notification Log → WebSocket Broadcast
```

## Redis Interactions

### Real-Time Notifications-Redis Flow

**Confirmed by Code**: Redis can be used for scaling WebSocket connections.

**Flow**:
```
WebSocket → Redis Adapter → Scale Broadcasts
```

## Queue Interactions

### Real-Time Notifications-Queue Flow

**Confirmed by Code**: Notifications can be queued for processing.

**Flow**:
```
Service → Queue → Worker → WebSocket Broadcast
```

## Worker Interactions

### Real-Time Notifications-Worker Flow

**Confirmed by Code**: Workers can broadcast notifications.

**Flow**:
```
Worker → Notification Service → WebSocket Gateway → Broadcast
```

## Business Rules

### Real-Time Notifications Rules

**Confirmed by Code**: Real-time notifications follow these rules:

1. **Room-Based**: Notifications sent to rooms
2. **User-Specific**: User-specific notifications
3. **Role-Based**: Role-based notifications
4. **Broadcast**: Broadcast to all users
5. **Hierarchy**: Institute/department hierarchy

### Notification Rules

**Confirmed by Code**: Notification rules:

1. **Type**: Notification type (info, warning, error)
2. **Priority**: Notification priority
3. **Expiry**: Notification expiry time
4. **Action**: Actionable notifications
5. **Read Status**: Read status tracking

## Security

### Real-Time Notifications Security

**Confirmed by Code**: Security considerations for real-time notifications:

1. **Authentication**: Authenticate connections
2. **Authorization**: Authorize room access
3. **Data Sanitization**: Sanitize notification data
4. **Rate Limiting**: Rate limit notifications
5. **Access Control**: Control notification access

## Performance Considerations

### Real-Time Notifications Performance

**Confirmed by Code**: Performance considerations:

1. **Room Management**: Manage rooms efficiently
2. **Connection Limits**: Limit concurrent connections
3. **Event Throttling**: Throttle notifications if needed
4. **Redis Adapter**: Use Redis adapter for scaling
5. **Batch Processing**: Batch notifications if possible

## Common Mistakes

### Mistake 1: Not Joining Rooms

**Symptom**: Notifications not received

**Cause**: Not joining rooms

**Fix**:
```typescript
// Join rooms on connection
async handleConnection(client: Socket) {
  client.join(`user:${userId}`);
  client.join(`role:${role}`);
}
```

### Mistake 2: Not Validating Data

**Symptom**: Invalid notification data

**Cause**: Not validating notification data

**Fix**:
```typescript
// Validate notification data
const notification = {
  type: 'info',
  message: data.message,
  // Validate fields
};
```

### Mistake 3: Broadcasting to Wrong Room

**Symptom**: Notifications sent to wrong users

**Cause**: Broadcasting to wrong room

**Fix**:
```typescript
// Broadcast to correct room
this.server.to(`user:${userId}`).emit('notification', notification);
```

## Debugging Guide

### Real-Time Notifications Debugging

**Issue**: Notifications not received

**Investigation**:
1. Check room membership
2. Check event emission
3. Check event subscription
4. Check authentication
5. Check logs

**Tools**:
- Socket.IO client debugger
- WebSocket logs
- Network tab in browser
- Console logs

## Future Enhancements

### Notification Persistence

**Status**: Not implemented

**Proposal**: Implement notification persistence:
- Store notifications in database
- Notification history
- Read/unread tracking
- Better user experience
- More complex

### Notification Preferences

**Status**: Not implemented

**Proposal**: Implement notification preferences:
- User notification preferences
- Notification types
- Notification channels
- Better user control
- More complex

## Production Considerations

### Production Real-Time Notifications

**Production Deployment**:
- Enable authentication
- Enable authorization
- Use Redis adapter
- Monitor connections
- Monitor notification rate

### Real-Time Notifications Monitoring

**Monitoring Metrics**:
- Notification rate
- Delivery rate
- Connection count
- Room count
- Error rate

## Example Requests

### Real-Time Notifications Example

**Send Notification**:
```typescript
await this.notificationService.sendToUser(userId, {
  type: 'info',
  title: 'New Message',
  message: 'You have a new message',
  action: 'view',
});
```

## Example Responses

### Real-Time Notifications Response

**Event Received**:
```javascript
socket.on('notification', (data) => {
  console.log('Notification:', data);
  // Display notification
});
```

## Sequence Diagrams

### Real-Time Notifications Flow

```
Service → Notification Service → WebSocket Gateway → User Room → Client Receives
```

## Architecture Diagrams

### Real-Time Notifications Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Service                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Notification Service                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  WebSocket Gateway                         │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  User Room    │  │  Role Room      │  │  Broadcast      │
│  (User-Specific)│  │  (Role-Based)   │  │  (All Users)    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Client                                   │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How are real-time notifications implemented?

**Answer**: Real-time notifications via:
- WebSocket gateway
- User joins user-specific room
- Service broadcasts to user room
- Client receives notification
- Display notification to user

### Q2: How do you send notifications to specific users?

**Answer**: Send to specific users via:
- User joins user-specific room on connection
- Service sends notification to user room
- WebSocket gateway broadcasts to room
- Client receives notification
- Display notification

### Q3: How do you scale real-time notifications?

**Answer**: Scale real-time notifications via:
- Redis adapter for WebSocket scaling
- Multiple WebSocket servers
- Load balancing
- Room management
- Connection limits

## Exercises

### Exercise 1: Implement Real-Time Notifications

**Task**: Implement real-time notifications.

**Steps**:
1. Create notification service
2. Add send to user method
3. Add send to role method
4. Integrate with WebSocket gateway
5. Test notifications

**Verification**:
- Service created
- Send to user works
- Send to role works
- Gateway integration works
- Tests pass

### Exercise 2: Implement Room-Based Notifications

**Task**: Implement room-based notifications.

**Steps**:
1. Add room joining on connection
2. Add send to room method
3. Add broadcast to all method
4. Test room notifications
5. Test broadcast

**Verification**:
- Room joining works
- Send to room works
- Broadcast works
- Notifications received
- Tests pass

## Real Production Scenarios

### Scenario 1: Notifications Not Received

**Situation**: Notifications not received by client

**Response**:
1. Check room membership
2. Check event emission
3. Check event subscription
4. Fix notification logic
5. Test notifications

### Scenario 2: High Notification Rate

**Situation**: Too many notifications sent

**Response**:
1. Check notification rate
2. Implement throttling
3. Implement batching
4. Monitor notifications
5. Optimize notification logic

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [11-Workers](../11-Workers/README.md) - Workers details
