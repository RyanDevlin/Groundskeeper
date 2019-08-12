<h1 align="center">Groundskeeper Network Hub</h1>
<p align="center">
  <b>A webserver and backend codebase for fully automating the care of house plants</b><br>
</p>
<br>
<p align="center">
    <img src="https://github.com/RyanDevlin/Groundskeeper/blob/master/groundskeeper_logo.png" alt="Master Private Key Embedded" width="100"/>
</p>

## What is this?

This repository conatins the code necessary to automate the tasks necessary for caring for house plants. With this repo you can build and fully deploy your own Django webserver running on a Raspberry Pi. The web server will act as an endpoint to allow you to check on the status of your houseplants from anywhere in the world. From within the web server you are able to monitor plant telemetry, trigger watering of the plants, set automatic schedules, and add/remove plants as you see fit. After deploying this codebase the only thing you should need to do to keep your plants alive is to refill their water reserves every few weeks when you recieve a notification on your phone from the webserver.

## **NOTE

This project is not currently complete and therefore relies on a number of assumptions to run. The end goal is to have this project be easily deployable through a simple build script.

## Built With

* [Python](https://www.python.org/) - Used as the backend scripts and web server
* [Django](https://www.djangoproject.com/) - Used as the framework for the web server
* [FusionCharts](https://www.fusioncharts.com/) - Used as the framework for displaying data in the web server
* [Celery](https://docs.celeryproject.org/en/latest/#) - Used to multithread the alerts backend
* [RabbitMQ](https://www.rabbitmq.com/) - Used as the message broker for Celery
* [Universal Tilt.js](https://jb1905.github.io/universal-tilt.js/) - For some fancy card animations!

## Authors

* **Ryan Devlin** - *Design, testing, debugging, staying up late at night thinking about plants* - [RyanDevlin](https://github.com/RyanDevlin)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/RyanDevlin/Groundskeeper/blob/master/LICENSE) file for details

