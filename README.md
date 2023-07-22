## Polars vs Pandas inside an AWS Lambda
### Data Processing

Read Full Blog Post Here
https://www.confessionsofadataguy.com/polars-vs-pandas-inside-an-aws-lambda/

This repo is part of a blog post covering the topic of using Pandas and Polars
inside an AWS Lambda to do data processing.

The idea is to just example how the code differs, and then inspect the
memory usage and runtime of those two Lambdas to see if one or the
other provides better performance. Since we pay for memory and runtime
of Lambdas.

We are using BackBlaze open source data set.
https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data

In this case we used `90`` files, about `6` GB worth of data.

Also, we are using `Docker` along with AWS `ECR` to store images for
each Polars and Pandas lambda. Here are the steps to `build` and 
`deploy` those Lambdas out to an ECR repository.

1. `cd src/{pandas} or src/{polars}`

2. `docker build -t confessions . --platform=linux/amd64`

3. Authenticate the Docker CLI to your Amazon ECR registry.
 `aws ecr get-login-password --profile confessions --region us-east-1 | docker login --username AWS --password-stdin 992921014520.dkr.ecr.us-east-1.amazonaws.com/confessions` or similar

4. Tag your image to match your repository name, and deploy the image to Amazon ECR using the docker push command.
`docker tag confessions:latest 992921014520.dkr.ecr.us-east-1.amazonaws.com/confessions:latest`
`docker push 992921014520.dkr.ecr.us-east-1.amazonaws.com/confessions:latest`

5. Trigger your lambda.
`aws lambda invoke --function-name arn:aws:lambda:us-east-1:992921014520:function:polarsLambda --region us-east-1 --profile confessions output.json`
