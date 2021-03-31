# Learning Goals App
Live  can be viewed at https://sleepy-springs-26346.herokuapp.com/

A website, which helps manage tasks or learning goals, made using Django. 
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is simple website, which help to store tasks or learning goals with to-do functionality. Features:
* Register and Login
* Learning Goals
  * View Learning Goals
  * Add Learning Goals
  * Edit Learning Goals
  * Delete Learning Goals
* Tasks:
  * View Tasks
  * Add Task 
  * Delete Task
	
## Technologies
Project is created with:
* Django
* Pytest
* HTML/CSS
* Bootstrap
* Docker

## Setup
To run this project:
1. Install Docker.
2. Clone repository. 
```
$ git clone https://github.com/rdubowski/Learning-Goals-App
```
3. Install frontend dependencies.
4. Build image with docker-compose
``` 
$ docker-compose build
```
5. Run image.
``` 
$ docker-compose up
``` 
