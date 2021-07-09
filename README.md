# Food Connect
## Final Master Project

Group Members:

   #### [ANANTH UPADHYA](https://www.linkedin.com/in/560085/)
   #### [DEESHA DESAI](https://www.linkedin.com/in/deeshadesai/)
   #### [PREETI PARIHAR](https://www.linkedin.com/in/preetiparihar/)
   #### [PRIYANKA DEVENDRAN](https://www.linkedin.com/in/priyanka-devendran-76244479/)

<br>

## Backend APIs
### Pre-requisites Set Up:

* Requirements:

    set following environment variables values:

    ```
    export COGNITO_USER_POOL_ID="" 
    export COGNITO_APP_CLIENT_ID="" 
    export COGNITO_APP_CLIENT_SECRET="" 
    export AWS_ACCESS_KEY_ID="" 
    export AWS_SECRET_ACCESS_KEY="" 
    export AWS_REGION="" 
    export S3_BUCKET="" 
    export DB_NAME="" 
    export DB_USERNAME="" 
    export DB_PASSWORD="" 
    ```

    ```pip install -r requirements.txt```

    ```python manage.py runserver 0.0.0.0:9091```

<br>

## Note 
All api response will have ```HTTP_ACCESSTOKEN``` and ```HTTP_REFRESHTOKEN``` headers, set these headers for further api access

<br>


## Signup API
### Header
Authorization: Basic "base64 username:password"

### Request
```
{
    "user_attributes": [{
        "Name": "given_name",
        "Value": "ABC"
    },{
        "Name": "family_name",
        "Value": "XYZ"
    }]
}
```

<br>


## Login API
### Header
    Authorization: Basic "base64 username:password"

### Request - None
### Response
    ```
    {
        "msg": "Welcome <user email>"
    }
    ```

<br>



## LogOut API
### Header
    pass ```HTTP_ACCESSTOKEN``` and ```HTTP_REFRESHTOKEN``` headers


<br>


## Confirm Signup API
### Header
    pass ```HTTP_ACCESSTOKEN``` and ```HTTP_REFRESHTOKEN``` headers

### Request
```
{
    "username": "<user email>",
    "password": "<verification code>",
    "force_alias_creation": false
}
```

### Response
```
{
    "ResponseMetadata": {
        "RequestId": "2c8c55e8-9434-4685-a200-16c1c623e844",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Thu, 08 Jul 2021 22:09:05 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "2",
            "connection": "keep-alive",
            "x-amzn-requestid": "2c8c55e8-9434-4685-a200-16c1c623e844"
        },
        "RetryAttempts": 0
    }
}
```
<br>


## Forgot Password API
### Header
    pass ```HTTP_ACCESSTOKEN``` and ```HTTP_REFRESHTOKEN``` headers

### Request
```
{
    "email": "<user email>"
}
```
<br>


## Confirm Forgot Password APi
### Header
    pass ```HTTP_ACCESSTOKEN``` and ```HTTP_REFRESHTOKEN``` headers

### Request
```
{
    "email": "<user email>",
    "new_password": "",
    "code": "<confirmation code"
}
```