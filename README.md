# Movie Theatre Ticket Booking API

An API as part of Zomentum's campus hiring assignment. This API helps fetch ticket data from DB, or update, delete or create tickets. Also, tickets are automatically deleted after 8 hours of their show time.

## Assumptions

- As no details about timing was provided, it is assumed that the timing is in 24-hours format
- It is assumed thatthe bookings are made taking into account only start time, no end time is considered for a show
- Movie length isn't considered in booking ticket

## Dependencies

- Python
- Flask

## Installation

- **cd** into project root
- Creating a virtual environment is recommended. Following command can be used to create a virtual environment.

```
python -m venv env
```

- Install all the requirements using the below command.

```
pip install -r requirements.txt
```

## Usage

Run the flask server as follows

```
flask run
```

This will setup a local server on http://127.0.0.1:5000<br />
Following routes are allowed on the API

- **GET** / (_Introductory page for API_)
- **POST** api/v1/ticket (_Book tickets_)
- **PUT** api/v1/ticket (_Update timing of a ticket_)
- **GET** api/v1/ticket (_Get all tickets for particular time or get ticket by ID_)
- **DELETE** api/v1/ticket (_Delete a ticket_)

### Booking a ticket
