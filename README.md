# Food Connect
Final Master Project

## Group Members:

   ###### [ANANTH UPADHYA](https://www.linkedin.com/in/560085/)
   ###### [DEESHA DESAI](https://www.linkedin.com/in/deeshadesai/)
   ###### [PREETI PARIHAR](https://www.linkedin.com/in/preetiparihar/)
   ###### [PRIYANKA DEVENDRAN](https://www.linkedin.com/in/priyanka-devendran-76244479/)

### Pre-requisites Set Up:

###### Backend APIs

* Requirements:

    set following environment variables values:

    ```
        'ENGINE': os.getenv("AWS_AURORA_ENGINE", None),
        'NAME': os.getenv("AWS_RDS_DB_NAME", None),
        'USER': os.getenv("AWS_DB_USERNAME", None),
        'PASSWORD': os.getenv("AWS_DB_PASSWORD", None),
        'HOST': os.getenv("AURORA_CLUSTER_ENDPOINT", None),
        'PORT': os.getenv("AURORA_CLUSTER_PORT", None)
    ```

    ```pip install -r requirements.txt```

    ```python manage.py runserver ```