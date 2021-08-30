FROM public.ecr.aws/lambda/python:3.8 AS base


FROM base as builder
WORKDIR ${LAMBDA_TASK_ROOT}
# Copy function code
COPY . ${LAMBDA_TASK_ROOT}
RUN pip3 install poetry \
    && poetry export --with-credentials --format requirements.txt --output requirements.txt \
    && pip3 install -r requirements.txt -t .

FROM base as app
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 