#!/usr/bin/env python3
import os

from aws_cdk import (
    core as cdk,
    aws_lambda,
    aws_lambda_python,
    aws_apigateway,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
)

environment = {
    'POSTGRES_USER': os.getenv('POSTGRES_USER'),
    'POSTGRES_PORT': os.getenv('POSTGRES_PORT'),
    'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'POSTGRES_DB': os.getenv('POSTGRES_DB'),
    'POSTGRES_SERVER': os.getenv('POSTGRES_SERVER'),
}

class LambdaHttpStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        migration_lambda = aws_lambda_python.PythonFunction(self, 'migration',
            entry="../app",
            index='run_migration.py',
            handler='handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout=cdk.Duration.seconds(60),
            environment=environment)

        task_handler_lambda = aws_lambda_python.PythonFunction(self, 'BackgroundTasks',
            entry="../app",
            index='tasks.py',
            handler='handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout=cdk.Duration.seconds(10),
            environment=environment)
           
        state_machine = aws_stepfunctions.StateMachine(self, "MyStateMachine",
            definition=aws_stepfunctions_tasks.LambdaInvoke(
                self, "MyLambdaTask", lambda_function=task_handler_lambda)
            .next(aws_stepfunctions.Succeed(self, "Done"))
        )
        http_handler_lambda = aws_lambda_python.PythonFunction(self, 'LambdaHttp',
            entry="../app",
            index='app.py',
            handler='handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout=cdk.Duration.seconds(10),
            environment={
                **environment,
                'STATE_MACHINE_ARN': state_machine.state_machine_arn,
            })

        aws_apigateway.LambdaRestApi(self, 'http-handler-lambda',
            handler=http_handler_lambda,
            proxy=True)

 
        state_machine.grant_start_execution(http_handler_lambda)


app = cdk.App()
LambdaHttpStack(app, "LambdaHttpStack")

app.synth()
