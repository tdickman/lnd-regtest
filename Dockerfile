# Prepare grpc client per https://dev.lightning.community/guides/python-grpc/
FROM        python:3.6
WORKDIR     /app
RUN         pip install grpcio grpcio-tools googleapis-common-protos
RUN         git clone https://github.com/googleapis/googleapis.git
RUN         curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
RUN         curl -o invoices.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/invoicesrpc/invoices.proto
RUN         python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto invoices.proto

FROM        python:3.6
ENV         PYTHONPATH=/app:/modules
RUN         mkdir -p /modules
WORKDIR     /app
RUN         pip install pipenv
COPY        --from=0 /app/rpc_pb2.py /modules
COPY        --from=0 /app/rpc_pb2_grpc.py /modules
COPY        --from=0 /app/invoices_pb2.py /modules
COPY        --from=0 /app/invoices_pb2_grpc.py /modules
ADD         manager/Pipfile* /tmp/
RUN         cd /tmp && pipenv install --system --deploy
COPY         ./manager/ /app/
COPY        config/config.yaml /

ENTRYPOINT  ["sleep", "400000"]
