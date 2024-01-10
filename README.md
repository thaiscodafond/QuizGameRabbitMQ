# Quiz Game Using RabbitMQ: Enhancing Distributed Communication

## Table of Contents

1. Introduction
2. How to Use
3. Project Choices and Constraints
4. Architecture of the Project
5. Why RabbitMQ
6. Why a WebSocket
7. Project Specifications & Future Improvements

## Introduction

In the realm of the CAlC unit (Intensive Calculation: Data Distribution and Computation), a project harnessing the capabilities of RabbitMQ was conceived. This endeavor aimed to showcase the middleware's abilities in facilitating communicating distributed applications, emphasizing fault tolerance, dynamic reconfiguration, and more, through an illustrative case study.

Originally considering a distributed machine learning algorithm, inspired by a past course, the project's direction shifted during an online gaming session with friends, pondering the creation of an online game like UNO. This project not only serves as a platform to master the middleware but also endeavors to craft an engaging game for friends and potentially a wider audience.

## How to Use

### Starting the Project

Ensure Docker is installed. Initiate the gameplay by accessing the project and executing "docker compose up --remove-orphans --build". Access a web browser and navigate to the "localhost:80" website. Multiple pages can be opened, each representing a player.

### Game Rules

* Each player joining or leaving triggers the start of a new game.
* Player addition during gameplay is prohibited.
* A maximum of ten rounds is allotted for each game.

Enjoy the game!

## Project Choices and Constraints

### Choices Made

The project aimed to explore communication between two distinct programming languages using RabbitMQ. Additionally, it served as an avenue to refine JavaScript skills for an ongoing internship. Consequently, the project took shape as a website (utilizing HTML, CSS, CommonJS, & Node.js) with a Python3 server.

### Constraints Encountered

Adopting Node.js posed specific constraints, necessitating the use of a WebSocket to facilitate communication between HTML and Node.js due to JS's inherent limitations with amqpd.

## Architecture of the Project

Illustration or description of the project's architectural layout and interconnections.

## Why RabbitMQ

A detailed explanation highlighting the strengths and advantages of employing RabbitMQ as the chosen middleware for this project.

## Why a WebSocket

Insight into the necessity and advantages of incorporating a WebSocket within the project to enable seamless communication between HTML and Node.js.

## Project Specifications & Future Improvements

### Initial Project Specifications

- [x] Element 1: Completed
- [ ] Element 2: Pending
  - [x] Sub-element 2.1: Completed
  - [ ] Sub-element 2.2: Pending
- [ ] Element 3: Pending

### Future Improvements

Ideas and potential enhancements to expand and refine the project's functionality and experience.