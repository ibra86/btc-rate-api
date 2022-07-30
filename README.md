# BTC Rate app

To run the app:

1. Define the following secrets as environment variables to pass them later on to the built docker container:

    - `api_key` - need to create a free account of this [API](https://apilayer.com/marketplace/category/conversion-apis)
    - `email_user` and `email_pass` - credentials of the correctly set-up smtp gmail account (in case of issues
      this [link](https://www.pythonfixing.com/2022/07/fixed-smtplibsmtpauthenticationerror.html) can help)

It can be done in a `.env` file, e.g.:

```
api_key=xxx
email_user=xxx
email_pass=xxx
```

2. Build and Run the container:

```bash
docker build -t flask_app .
docker run -p 5000:5000 --env-file ./.env flask_app
```

3. App is in a dev state and will be running on ```http://localhost:5000```.



