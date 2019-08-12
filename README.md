<h1 align="center">Groundskeeper Network Hub</h1>
<p align="center">
  <b>A webserver and backend codebase for fully automating the care of house plants</b><br>
</p>

<p align="center">
    <img src="https://lh3.googleusercontent.com/ySeIDGiyt16lE3YcWlBovOwys95JmM7jOcYWc7HdXuysO0bFb_nhStyq9ehvhKJbmQ3y3AlRJr0yTWjcFlK27jkPJtyqnhBGNiVENIMTIIB9BaVjaBHXjhxpq0MLY14WxWlDtojzGuk" alt="Master Private Key Embedded" width="400"/>
</p>

## What is this?

This repository conatins the code necessary to automate the tasks necessary for caring for house plants. With this repo you can build and fully deploy your own Django webserver running on a Raspberry Pi. The web server will act as an endpoint to allow you to check on the status of your houseplants from anywhere in the world. From within the web server you are able to monitor plant telemetry, trigger watering of the plants, set automatic schedules, and add/remove plants as you see fit. After deploying this codebase the only thing you should need to do to keep your plants alive is to refill their water reserves every few weeks when you recieve a notification on your phone from the webserver.

## **NOTE

This project is not currently complete and therefore relies on a number of assumptions to run. The end goal is to have this project be easily deployable through a simple build script.

## Built With

* [Python](https://www.python.org/) - Used as the backend scripts and web server
* [Django](https://www.djangoproject.com/) - Used as the framework for the web server
* [FusionCharts](https://www.fusioncharts.com/) - Used as the framework for displaying data in the web server

## Authors

* **Ryan Devlin** - *Design, testing, debugging, staying up late at night thinking about plants* - [RyanDevlin](https://github.com/RyanDevlin)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/RyanDevlin/Groundskeeper/blob/master/LICENSE) file for details

