FROM public.ecr.aws/lambda/python:3.11

# Install pg dependencies
RUN yum install -y gcc python27 python27-devel postgresql-devel

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py connection.py funcao_previsao.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]