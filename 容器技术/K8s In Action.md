# Why k8s

- Big app are being broken down into smaller, independently running components called microservices.
- Many components is difficult to configure, manage, and keep whole system running smoothly.
- develop and deploy each microservice separately.
- many coponents, number of inter-dependencies between the components increases 

# Before k8s

Deal with increasing loads:

- vertically scale the server, adding more CPUs, Memory.
- Scale the shole system horizontally, setting additional servers, running multiple copies of app.

# K8s communicate

- through HTTP, or RESTful APIs, or AMQP.
