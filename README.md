**System Overview**

The system consists of two microservices built on the FastAPI framework. The first microservice is responsible for keeping track of events, while the second microservice is responsible for accepting bets on those events. The two microservices communicate with each other through a REST API.

**Line Provider Microservice**

The Line Provider microservice is responsible for managing events in the system. It exposes REST API for creating, retrieving and updating events (documentation available on endpoint */docs*).

Also it has a communacation with Bet service. When any event changes, background task starts and sends callback to Bet service.

**Bet Microservice**

The Bet microservice is responsible for managing bets in the system. REST API documentation available on endpoint */docs*.

**Launch Project.**

- *docker-compose up -d*. Line Provider service starts available on url *http://localhost:8002*, and Bet service on *http://localhost:8003*
- *pytest*. Tests available in Line Provider service.
