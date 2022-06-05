# Dictionary with images 

## Installation
First you need to pull the image using ```docker pull ismaildaoudi/dictionary:latest```

## Usage

Run a container for the image 

```sudo docker run -d -p 5000:5000 ismaildaoudi/dictionary:latest```

to check the database SSH into the container ```sudo docker exec -it CONTAINER_ID bash``` you can get your CONTAINER_ID using the command ```docker ps```

once in the container RUN ```apt update``` then ```apt upgrade``` then install sqlite3 using ```apt install sqlite3``` then Run ```sqlite3 dictionnary.db``` you will see 2 tables history and users if you run the command ```.tables;``` run  ```SELECT * FROM users;``` to show all the users. 

then open a browser using this URL : ```http://localhost:5000/```



then use the app but pay attention to the login (Username be careful on using spaces after or before the name)
