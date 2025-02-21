# EventManagement 🎉
## About the project
**EventManagement** - REST API for events control, where users can register for them, get info about them, update, create and delete them also

---
## Local start (without Docker)

 - ### 1️⃣ Install the dependencies
    Open cmd or terminal in working directory with the EventManagement project
    ```sh 
    python -m venv venv
    source venv/bin/activate # for Linux/Maс
    venv\Scripts\activate #for Windows
    pip install -r requirements.txt
    ```

 - ### 2️⃣ Set your dev.env file
    Create and go to your **dev.env** file and change your local settings for environment similar to **.env.sample** file (in local mode system takes your environment from **dev.env**)
 - ### 3️⃣ Apply the migrations
    ```sh
    python manage.py migrate
    ```
 - ### 4️⃣ Create superuser(optional)
    ```sh
    python manage.py createsuperuser
    ```
 - ### 5️⃣ Start the server
    Server will be available at http://127.0.0.1:8000.
---
## Start with Docker 🐳
- ### 1️⃣ Set your needed .env file:
    - If you wanna use docker-compose.prod.yml, then create and go to the **prod.env** file and configure it similar to **.env.sample** file, else do the same thing but with your **dev.env** file.
- ### 2️⃣ Docker start
    - Now you can start Docker smth like
    ```sh
    docker-compose -f docker-compose.{dev/prod}.yml up --build -d
    ```
    - Docker automatically starts all the needed services, apply all unapplied migrations and collects statis if it works in a production mode.
    - Docker also uses **NGinx** for **production mode**.
    - You can optionally create a superuser by using a command:
       ```sh
       docker-compose -f docker-compose.{dev/prod}.yml exec backend python manage.py createsuperuser
       ```
    - Server will be available at http://localhost:80 (or just http://localhost)

## 📝 API
🔗 Swagger-документация
---
 - After project started, you can see the full documentation by url-route **/swagger** (http://127.0.0.1:8000/swagger for *local development* and http://localhost/swagger/ in Docker)

--- 
## Using this API, you can:
- **Users**:
    - Register(if you wanna register as an admin, you need to input the additional password for admin)
    - Login (using **JWT** tokens)
    - Change your user's info
    - Change other users if you have an admin role
    
- **Events**:
    - Getting events
    - Creating events
    - Updating events
    - Registration for event(admins can also register other users)
    - Unregistration for event(admins can also unregister other users )
    - Deleting events

**!!! All of this is only possible for authorized users**

## Technologies
 - Django + Django REST Framework
 - PostgreSQL
 - Docker + Docker Compose
 - Swagger




    




    
