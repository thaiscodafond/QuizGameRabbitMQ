const WebSocket = require("ws");
const amqp = require("amqplib/callback_api");
const { v4: uuidv4 } = require("uuid");

const wss = new WebSocket.Server({ port: 8080 });
const connectedClients = new Map();

let connectedPlayers = 0;
let requestedNew = 0;

wss.on("connection", function connection(ws) {
  const clientId = uuidv4();
  connectedClients.set(ws, clientId);
  console.log(`Client ${clientId} connected`);

  connectedPlayers++;

  if (connectedPlayers >= 2) {
    sendRequestForNewQuestion();
  }

  sendPlayerCountToClients();
  ws.send(JSON.stringify({ type: "clientId", clientId }));
  sendPlayerCountToServer();

  ws.on("message", function incoming(message) {
    if (message instanceof Buffer) {
      message = message.toString();
    }

    try {
      const parsedMessage = JSON.parse(message);
      console.log("Received message from client WS:", parsedMessage);

      if (parsedMessage.type === "register") {
        console.log("Client registered");
      } else if (parsedMessage.type === "answer") {
        sendMessageToConsumer(parsedMessage, clientId, connectedClients);
      } else if (parsedMessage.type == "new_question") {
        requestedNew += 1;
        if (requestedNew == connectedPlayers) {
          sendRequestForNewQuestion();
          console.log("New question requested");
          requestedNew = 0;
        }
      }
    } catch (error) {
      console.error("Error parsing message:", error);
    }
  });

  ws.on("close", function () {
    connectedClients.delete(ws);
    console.log(`Client ${clientId} disconnected`);
    connectedPlayers--;
  });
});

function sendPlayerCountToClients() {
  const data = { type: "player_count", count: connectedPlayers };
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}

// Publisher part
const { connect } = require("amqplib/callback_api");

const publisherQueue = "messages_from_clients";

function sendPlayerCountToServer() {
  sendMessageToConsumer({ type: "player_count", count: connectedPlayers });
}

function sendRequestForNewQuestion() {
  const data = { type: "fetch_question" };
  connect("amqp://rabbitmq", function (error0, connection) {
    if (error0) {
      throw error0;
    }
    connection.createChannel(function (error1, channel) {
      if (error1) {
        throw error1;
      }

      channel.assertQueue(publisherQueue, {
        durable: false,
      });

      channel.sendToQueue(publisherQueue, Buffer.from(JSON.stringify(data)));
      console.log("Request sent to RabbitMQ for a new question");

      setTimeout(function () {
        connection.close();
      }, 500);
    });
  });
}

function sendMessageToConsumer(data, answerId = null, connectedUserIds = null) {
  message = data;
  if (answerId != null) {
    const connectedClientsJSON = JSON.stringify(
      Array.from(connectedUserIds.values())
    );
    message = {
      ...data,
      answerId: answerId,
      connectedUserIds: connectedClientsJSON,
    };
  }

  connect("amqp://rabbitmq", function (error0, connection) {
    if (error0) {
      throw error0;
    }
    connection.createChannel(function (error1, channel) {
      if (error1) {
        throw error1;
      }

      channel.assertQueue(publisherQueue, {
        durable: false,
      });

      channel.sendToQueue(publisherQueue, Buffer.from(JSON.stringify(message)));
      console.log("Message sent to RabbitMQ:", message);

      setTimeout(function () {
        connection.close();
      }, 500);
    });
  });
}

// Consumer part
const consumerQueue = "messages_to_clients";

let playerScores = {};

let roundNumber = 0;

amqp.connect("amqp://rabbitmq", function (error0, connection) {
  if (error0) {
    throw error0;
  }

  connection.createChannel(function (error1, channel) {
    if (error1) {
      throw error1;
    }

    channel.assertQueue(consumerQueue, {
      durable: false,
    });

    console.log("Waiting for messages in", consumerQueue);

    channel.consume(
      consumerQueue,
      function (msg) {
        if (msg !== null) {
          const message = JSON.parse(msg.content.toString());
          console.log("Received message from RabbitMQ:", message);

          wss.clients.forEach(function each(client) {
            if (client.readyState === WebSocket.OPEN) {
              client.send(JSON.stringify(message));
            }
          });

          channel.ack(msg);
        }
      },
      {
        noAck: false,
      }
    );
  });
});

console.log("WebSocket server running on port 8080");
