# Scrapping project

Mikroserwis pobierający zdjęcia i tekst ze stron www.
Funkcjonalność
- Zlecenie pobrania tekstu z danej strony internetowej i zapis jej w systemie.
- Zlecenie pobrania wszystkich obrazków z danej strony i zapis ich w systemie.
- Sprawdzenie statusu zleconego zadania.
- Możliwość pobrania stworzonych zasobów (tekstu i obrazków)

## Getting Started

Serwis dostaje zapytania poprzez RESTowe API wystawione przez jeden z serwisów.
Serwis z API wysyła zadanie pobrania zasobów konkretnej strony internetowej.
Zadania są kolejkowane w Rabbicie i serwis w miare możliwosci
 pobiera kolejne (liczba wykonywanych zadań zależy odilości workerów (domyślnie 10)).
 
 Kod nie sprawdza zbytnio wyjątków i innych nieprzewidzianych sytuacji.
 W celu lepszego crawlowania (np zaciągania danych z kolejnych podstron 
 na wybranej domenie trzebaby użyć normalnie scrapy'iego.

### Prerequisites

To run a service you need docker and docker-compose.
To run service locally and run tests you will need:
- python3 + pyenv/venv + requirements
- rabbitmq
    
    `sudo apt-get install rabbitmq-server`
    
    `sudo rabbitmq-plugins enable rabbitmq_management`

## Deployment

Docker images are build using Dockerfile.
To build the image run:

`docker build -t scrapper_base .`

And run the stack with command:

`docker-compose up`

## Running the tests

Having requirements installed:

`cd app`

`python -m pytest tests`

## Built With

* Python
* Docker
* RabbitMQ

## Authors

* **Stankiewicz Mateusz** - https://www.linkedin.com/in/mateusz-stankiewicz-3b04a2108/

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

